import json
from pathlib import Path

projectRoot : str = str(Path(__file__).parent.parent.absolute()) 

def main(mockData=True):
    reviews = None
    products = None
    if mockData:
        reviews = json.load(open(projectRoot + "/data/test/products.json"))
        products = json.load(open(projectRoot + '/data/test/meta_products.json'))
    else:
        reviews = json.load(open(projectRoot + '/data/real/Software.json'))
        products = json.load(open(projectRoot + '/data/real/meta_Software.json'))

    print(reviews)
    print(products)
