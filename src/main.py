import gzip
import json
import os
import sys
from pathlib import Path

import pandas as pd

projectRoot : str = str(Path(sys.modules['__main__'].__file__).parent)

def parse(path):
    g = gzip.open(path, 'rb')
    for l in g:
        yield json.loads(l)

def getDF(path):
    i = 0
    df = {}
    for d in parse(path):
      df[i] = d
      i += 1
    return pd.DataFrame.from_dict(df, orient='index')


def load_mock_file(file_path):
    with open(file_path, "r") as file:
        content = json.load(file)
    return content

def main():

    pass

if __name__ == "__main__":
    main()
