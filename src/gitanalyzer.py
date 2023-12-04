import re
import subprocess
import os
from datetime import datetime, timedelta, date
from sqlalchemy import select, insert, update, func
from sqlalchemy.orm import Session
from entities import Base, Repo, RepoStat
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from typing import Sequence
import pandas as pd
from githubapi import GithubAPI
from functools import reduce
from dotenv import load_dotenv

load_dotenv(os.path.abspath(os.path.dirname(__file__) + "/../.env"))

GITHUB_API_TOKEN = os.environ["GITHUB_API_TOKEN"]

POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_CONTAINER_PORT = os.environ["POSTGRES_CONTAINER_PORT"]
POSTGRES_DSN =\
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_CONTAINER_PORT}/{POSTGRES_DB}"


class GitAnalyzer:

    __slots__ = ('engine', )

    def __init__(self):
        postgres_dsn = POSTGRES_DSN
        self.engine = create_engine(postgres_dsn, echo=True)

    def update_db_schema(self):
        pass

    def get_data_frame(self) -> pd.DataFrame:

        query = """
            select r.name as repo_name, rs.stat_date, rs.new_lines
            from repo_stat rs
            join repo r
            on rs.repo_id = r.id
            order by rs.stat_date
        """
        df = pd.read_sql(query, self.engine)

        return df

    async def add_repo(self, name: str):
        with Session(self.engine) as session:
            try:
                repo = session.scalars(select(Repo).filter_by(name=name)).one()
            except NoResultFound:
                repo = Repo(
                    name=name
                )
                session.add(repo)
                session.commit()
        await self.update_repo_stat(name)

    async def update_all_repos_stat(self):

        with Session(self.engine) as session:
            repos: Sequence[Repo] = session.scalars(select(Repo)).all()

        for repo in repos:
            await self.update_repo_stat(repo.name)

    async def update_repo_stat(self, name: str, date_from=None, date_to=None):

        with Session(self.engine) as session:
            try:
                repo: Repo = session.scalars(
                    select(Repo)
                    .where(Repo.name == name)
                ).one()
            except NoResultFound:
                return  # TODO: переделать

            # перебираем за месяц от крайнего дня + 1 (чтобы на графике удобно отображалось)
            current_date: date = date.today() + timedelta(days=1)
            begin_date: date = current_date - timedelta(days=40)

            print(f"{current_date = }, {begin_date = }")

            while current_date >= begin_date:

                new_lines = await self.get_new_lines_count_from_github(
                    repo_name=name,
                    since=current_date,
                    until=current_date + timedelta(days=1)
                )
                try:
                    stat: RepoStat = session.scalars(
                        select(RepoStat)
                        .where((RepoStat.stat_date == current_date) & (RepoStat.repo_id == repo.id))
                    ).one()
                    print(f"EXISTING ROW: {stat = }")
                except NoResultFound:
                    stat = RepoStat()
                    print(f"NEW ROW: {stat = }")

                session.add(stat)

                stat.stat_date = current_date
                stat.repo = repo
                stat.new_lines = new_lines

                print(f"{stat = }, {stat.id = }")

                current_date -= timedelta(days=1)

            session.commit()

    def get_new_lines_count_from_local(self, repo_name: str, since: date, until: date) -> int:
        """
        Анализирует git log через следующие строки:
         _types.py | 3 +--
         _class_slots.py | 18 ++++++++++++++++++
        """

        command = 'git log --since="{since}" --until="{until}" --stat --pretty'.format(
            since=since.isoformat() + "T00:00:00Z",
            until=until.isoformat() + "T00:00:00Z"
        )

        result = subprocess.run(command,
                                cwd=f"/var/www/{repo_name}",
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True
                                )

        if result.returncode == 0:
            pattern = r'\s+\|\s+(\d+)\s+(\++)[^\+]'
            matches = re.findall(pattern, result.stdout)
            # генератор списка (list comprehension)
            added_strings = sum(len(match[1]) for match in matches)
            return added_strings
        else:
            raise Exception(result.stderr)

    async def get_new_lines_count_from_github(self, repo_name: str, since: date, until: date):

        gh_api = GithubAPI(GITHUB_API_TOKEN, echo=True)
        r = await gh_api.query("""
            query (
                $owner: String!,
                $repo_name: String!,
                $since: GitTimestamp,
                $until: GitTimestamp
                )
                {
                    repository(owner: $owner, name: $repo_name) {
                        defaultBranchRef {
                            target {
                                ... on Commit {
                                    history(since: $since, until: $until) {
                                        nodes {
                                            # id
                                            additions
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
        """, {
            "owner": "mikeziminio",
            "repo_name": repo_name,
            "since": since.isoformat() + "T00:00:00Z",
            "until": until.isoformat() + "T00:00:00Z"
        })
        commits = r["data"]["repository"]["defaultBranchRef"]["target"]["history"]["nodes"]
        new_lines = reduce(lambda acc, c: acc + c["additions"], commits, 0)
        return new_lines
