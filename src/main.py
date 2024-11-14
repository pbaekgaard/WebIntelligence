import argparse
import gzip
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from lib import evaluate, gradient_descent, make_user_profiles

projectRoot : str = str(Path(sys.modules['__main__'].__file__).parent.parent)
parser = argparse.ArgumentParser()

parser.add_argument('-m', '--mock', help="Use mock instead of real data. Specify a size (md, lite)", type=str)
args = parser.parse_args()

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

def main(mockData = True, mockSize='md'):
    if mockData:
        reviews = getDF(projectRoot+f"/db/test/{mockSize}/products_{mockSize}.json.gz")
        products = getDF(projectRoot+f"/db/test/{mockSize}/meta_products_{mockSize}.json.gz")
    else:
        reviews = getDF(projectRoot+"/db/real/Software.json.gz")
        products = getDF(projectRoot+"/db/real/meta_Software.json.gz")

    split = gradient_descent.make_rating_matrix(reviews)
    groundTruth = np.array([
        [5,2,3,1],
        [4,np.nan,4,1],
        [1,5,2,np.nan],
        [2,4,3,2]
        ])
    preprocessed_rating_matrix = gradient_descent.preprocessing_of_rating_matrix(split)
    a, b = gradient_descent.calculate_A_B(preprocessed_rating_matrix)
    updated_rating_matrix = gradient_descent.update_rating_matrix(a, b, split)
    prediction = np.where(np.isnan(split), updated_rating_matrix, split)
    print(type(groundTruth))
    evaluation = evaluate(groundTruth=groundTruth, prediction=prediction)







if __name__ == "__main__":
    """
    mockSize: 'md', 'lite'
    """
    if args.mock:
        if args.mock == 'md':
            main(mockData=True, mockSize='md')
        elif args.mock == 'lite':
            main(mockData=True, mockSize='lite')
        else:
            parser.error("invalid argument for argument -m/--mock!")
    
    else:
        main(mockData=False)

