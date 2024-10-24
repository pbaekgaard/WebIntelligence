import json


def make_user_profiles(reviews, meta):
    user_profiles = {}
    for index, review in reviews.iterrows():
        product = [prod for index, prod in meta.iterrows() if prod["asin"] == review["asin"]][0]
        if product is not None:
            if review["reviewerID"] not in user_profiles:
                user_profiles[review["reviewerID"]] = []
                make_user_profile(review, product, user_profiles)
            else:
                make_user_profile(review, product, user_profiles)
    return user_profiles

def make_user_profile(review, product, user_profiles):
    profile = {"overall": review["overall"]}
    profile.update(product)
    user_profiles[review["reviewerID"]].append(profile)

def save_user_profile(user_profiles):
    with open("./Recommender-System/User-profiles/user_profiles.json", "w") as file:
        file.write(json.dumps(user_profiles, indent=4))