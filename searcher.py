from pathlib import Path
from pandas import DataFrame
from pandas.io.json._json import JsonReader
import pandas
from progress.spinner import Spinner
from typing import List

ARXIV_JSON: Path = Path("arxiv.json")
QUERY: str = "cs.CV"
DF_LIST: List[DataFrame] = []


def dfIDQuery(df: DataFrame, query: str) -> DataFrame:
    """Code from: https://github.com/NicholasSynovic/dnn-dependencies"""

    mask = df["categories"].apply(lambda x: query in x)
    return df[mask]


def main()  ->  None:
    jr: JsonReader = pandas.read_json(path_or_buf=ARXIV_JSON, lines=True, chunksize=1000,)
   
    with Spinner(f"Finding all documents with category: {QUERY}... ") as spinner:
        df: DataFrame
        for df in jr:
            output: DataFrame = dfIDQuery(df=df, query="cs.CV")
            DF_LIST.append(output)
            spinner.next()

    df: DataFrame = pandas.concat(objs=DF_LIST, ignore_index=True)
    df.T.to_json(path_or_buf=f"{QUERY}.json", indent=4)


if __name__ == "__main__":
    main()
