from gitanalyzer import GitAnalyzer
import argparse
import types
import asyncio

git_analyzer = GitAnalyzer()


class BaseConsoleRouter:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Git analyzer")
        self.parser.add_argument("command", help="Название команды")
        self.parser.add_argument("params", nargs="*", help="Параметры команды")

    def route(self):
        args = self.parser.parse_args()

        try:
            method = self.__getattribute__(args.command)
            if not isinstance(method, types.MethodType):
                raise AttributeError()
            method.__call__(*args.params)
        except AttributeError:
            print(f"Команда {args.command} не известна")


class ConsoleRouter(BaseConsoleRouter):
    def add_repo(self, name: str):
        git_analyzer.add_repo(name)

    def update_repo_stat(self, name: str):
        git_analyzer.update_repo_stat(name)

    def update_all_repos_stat(self):
        asyncio.run(git_analyzer.update_all_repos_stat())

    def update_db_schema(self):
        git_analyzer.update_db_schema()

    def get_data_frame(self):
        git_analyzer.get_data_frame()


if __name__ == '__main__':
    console_router = ConsoleRouter()
    console_router.route()
