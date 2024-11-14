import numpy as np
import pandas as pd


def evaluate(groundTruth : np.ndarray, prediction: np.ndarray, topk=2, relevancyTreshold=4):
    userRatings = pd.DataFrame(prediction) 
    print(f"User Ratings: {userRatings}")
    print(f"Ground Truth: {groundTruth}")
    for i, (user_truth, user_pred) in enumerate(zip(groundTruth, prediction)):
        ratings = pd.Series(user_pred)
        # Get topK indexes
        topk_indexes = ratings.nlargest(topk).index.tolist()
        print(topk_indexes)
        relevant_indexes = np.where(user_truth >= relevancyTreshold)[0].tolist()
        print(f"relevant for user {i}: {relevant_indexes}")
         

