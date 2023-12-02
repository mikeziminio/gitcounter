import plotly.express as px
import plotly.offline as po
import plotly.graph_objects as go
import pandas as pd
from gitanalyzer import GitAnalyzer
from datetime import datetime, date, timedelta
from helpers import format_number


page_template = """
    <html>
        <head>
            <script type="text/javascript">{plotlyjs}</script>
        </head>
        <body>
            Общее кол-во дней: <b>{days_count}</b>.
            Общее кол-во строк кода: <b>{new_lines_count} ({new_lines_count_percentage}% от {target_lines_count})</b>.
            Среднее кол-во строк кода в день: <b>{avg_new_lines_count}</b>.<br>
           {div}
        </body>
    </html>
"""


def get_all_stat() -> str:

    git_analyzer = GitAnalyzer()
    df: pd.DataFrame = git_analyzer.get_data_frame()

    sum_df = (
        df[["stat_date", "new_lines"]]
        .groupby(["stat_date"])
        .agg({"new_lines": "sum"})
        .assign(repo_name="Все репозитории")
        .reset_index()
    )

    days_count: int = (date.today() - date(2023, 10, 29)).days

    new_lines_count = (
        df[["new_lines"]]
        .sum()
        .loc["new_lines"]
    )

    print(f"{new_lines_count = }", type(new_lines_count))

    fig_df = pd.concat([sum_df, df])

    fig = px.line(
        fig_df,
        x='stat_date',
        y='new_lines',
        color="repo_name",
        line_shape="spline"
    )
    fig.update_layout(
        xaxis={
            "title": "Дата",
            "tickmode": "linear",
        },
        yaxis={
            "title": "Строк нового кода",
        },
        legend={
            "title_text": "Репозиторий",
        }
    )

    fig.update_traces(
        selector={
            "name": "Все репозитории"
        },
        line={
            "width": 5,
            "color": "#cccccc",
            "dash": "solid"
        },
        mode="lines+text",
        text=sum_df[["new_lines"]]
    )

    target_lines_count = 50000

    div_code = po.plot(fig, output_type='div')
    page_html = page_template.format(
        plotlyjs=po.get_plotlyjs(),
        div=div_code,
        days_count=days_count,
        new_lines_count=format_number(new_lines_count),
        target_lines_count=format_number(target_lines_count),
        new_lines_count_percentage=round(100 * new_lines_count / target_lines_count, 1),
        avg_new_lines_count=round(new_lines_count / days_count)
    )

    return page_html


def get_repo_stat(repo_name: str) -> str:
    git_analyzer = GitAnalyzer()
    df: pd.DataFrame = git_analyzer.get_data_frame()

    repo_df = df.query('repo_name == @repo_name')

    print(repo_df)

    days_count: int = (datetime.today().date() - date(2023, 10, 29)).days

    new_lines_count = (
        df[["new_lines"]]
        .sum()
        .loc["new_lines"]
    )

    fig = px.line(
        repo_df,
        x='stat_date',
        y='new_lines',
        color="repo_name",
        line_shape="spline"
    )
    fig.update_layout(
        xaxis={
            "title": "Дата",
            "tickmode": "linear",
        },
        yaxis={
            "title": "Строк нового кода",
        },
        legend={
            "title_text": "Репозиторий",
        }
    )

    target_lines_count = 50000

    div_code = po.plot(fig, output_type='div')
    page_html = page_template.format(
        plotlyjs=po.get_plotlyjs(),
        div=div_code,
        days_count=days_count,
        new_lines_count=format_number(new_lines_count),
        target_lines_count=format_number(target_lines_count),
        new_lines_count_percentage=round(100 * new_lines_count / target_lines_count),
        avg_new_lines_count=round(new_lines_count / days_count)
    )

    return page_html
