from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List

import pandas
from pandas import DataFrame
from pandas.io.json._json import JsonReader
from progress.spinner import Spinner

QUERY: str = "cs.CV"
DF_LIST: List[DataFrame] = []


def getArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="ArXiv Document Searcher",
        description="Using the Kaggle export of the ArXiv repository, search for documents of a particular category",
        epilog="Created by Nicholas M. Synovic",
    )
    parser.add_argument(
        "-i",
        "--input",
        nargs=1,
        default="arxiv.json",
        type=str,
        required=False,
        help="Kaggle ArXiv export file location",
    )
    parser.add_argument(
        "-q",
        "--query",
        nargs=1,
        default="cs.CV",
        required=False,
        help="Category query to search for",
    )
    return parser.parse_args()


def dfQuery(df: DataFrame, query: str) -> DataFrame:
    mask = df["categories"].apply(lambda x: query in x)
    return df[mask]


def main() -> None:
    args: Namespace = getArgs()

    arxivPath: Path
    if type(args.input) is list:
        arxivPath = Path(args.input[0])
    else:
        arxivPath = Path(args.input)

    query: str
    if type(args.query) is list:
        query = args.query[0]
    else:
        query = args.query

    jr: JsonReader = pandas.read_json(
        path_or_buf=arxivPath,
        lines=True,
        chunksize=1000,
    )

    with Spinner(f"Finding all documents with category: {query}... ") as spinner:
        df: DataFrame
        for df in jr:
            output: DataFrame = dfQuery(df=df, query=query)
            DF_LIST.append(output)
            spinner.next()

    df: DataFrame = pandas.concat(objs=DF_LIST, ignore_index=True)
    df.T.to_json(path_or_buf=Path(f"{query}.json"), indent=4)


if __name__ == "__main__":
    main()
