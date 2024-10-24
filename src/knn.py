import math
import re


def k_nearest_neighbors(k, meta):
    k_nearest = {}
    for index, product in meta.iterrows():
        distances = []
        for index, compare_product in meta.iterrows():
            diff_in_price = compare_price(product, compare_product)
            diff_in_category = compare_category(product, compare_product)
            distances.append({ 
                "product": compare_product["asin"],
                "distance": math.sqrt(sum([math.pow(diff_in_price, 2), math.pow(diff_in_category, 2)]))
            })
        distances = sorted(distances, key=lambda x: x["distance"], reverse=True)
        if product["asin"] not in k_nearest:
            k_nearest[product["asin"]] = distances[:k]
    return k_nearest

def compare_price(product, compare_product):
    try:
        product_price = float(re.sub("[$]", "", product["price"]))
    except:
        product_price = 0.0
    try:
        compare_product_price = float(re.sub("[$]", "", compare_product["price"]))
    except:
        compare_product_price = 0.0
    return abs(product_price - compare_product_price)

def compare_category(product, compare_product):
    if product["category"] or compare_product["category"]:
        diff_in_category = len([category for category in product["category"] if category in compare_product["category"]]) / len(list(set(product["category"]).union(set(compare_product["category"]))))
    else:
        diff_in_category = 0.0

    return diff_in_category * 10
