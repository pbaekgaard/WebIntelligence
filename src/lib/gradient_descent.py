import math

import numpy as np


def make_rating_matrix(reviews):
    extracted_columns = reviews[["reviewerID", "asin", "overall"]]
    order_of_columns = [] # Column entries are "asin" values
    order_of_rows = [] # Row entries are "reviewerID" values

    for index, extracted_column in extracted_columns.iterrows():
        if extracted_column["asin"] not in order_of_columns: 
            order_of_columns.append(extracted_column["asin"]) 
        if extracted_column["reviewerID"] not in order_of_rows:
            order_of_rows.append(extracted_column["reviewerID"])

    
    rating_matrix = np.full(shape=(len(order_of_rows), len(order_of_columns)), fill_value=np.nan)
    rating_matrix = np.array([
        [np.nan,np.nan, np.nan, 1],
        [4, np.nan, 4, 1],
        [1,5,2,np.nan],
        [2,4,3,2]
        ])
    return rating_matrix

def preprocessing_of_rating_matrix(rating_matrix):
    observed_ratings_for_columns = np.sum(~np.isnan(rating_matrix), axis=0)
    observed_ratings_for_rows = np.sum(~np.isnan(rating_matrix), axis=1)
    observed_movie_user_pairs = np.sum(~np.isnan(rating_matrix))
    # preprocessed_rating_matrix = np.zeros(shape=rating_matrix.shape)
    preprocessed_rating_matrix = ((rating_matrix - (1/observed_ratings_for_columns * np.nansum(rating_matrix, axis=0))).T - 1/observed_ratings_for_rows * np.nansum(rating_matrix, axis=1)).T + 1/observed_movie_user_pairs * np.nansum(rating_matrix)

    # for column in range(rating_matrix.shape[1]):
    #     for row in range(rating_matrix.shape[0]):
    #         preprocessed_rating_matrix[row, column] = rating_matrix[row, column] - (1/observed_ratings_for_columns[column] * np.nansum(rating_matrix[:, column]) - 1/observed_ratings_for_rows[row] * np.nansum(rating_matrix[row]) + 1/observed_movie_user_pairs * np.nansum(rating_matrix))

    return preprocessed_rating_matrix
def calculate_A_B(rating_matrix):
    eta = 0.001
    k = 100
    none_nan_rating_matrix = np.nan_to_num(rating_matrix)
    number_of_rows, number_of_columns = rating_matrix.shape
    number_of_dims = math.ceil(np.log2(number_of_rows))
    a = np.random.rand(number_of_rows, number_of_dims)
    b = np.random.rand(number_of_dims, number_of_columns)

    

    for i in range(k):
        d_error_a = - np.dot((none_nan_rating_matrix - np.dot(a, b)), np.transpose(b))
        d_error_b = - np.dot(np.transpose(a), (none_nan_rating_matrix - np.dot(a,b)))
        a = a - eta * d_error_a
        b = b - eta * d_error_b

    return a, b

def update_rating_matrix(a, b, rating_matrix):
    updated_rating_matrix = np.dot(a, b)
    observed_ratings_for_columns = np.sum(~np.isnan(rating_matrix), axis=0)
    observed_ratings_for_rows = np.sum(~np.isnan(rating_matrix), axis=1)
    observed_movie_user_pairs = np.sum(~np.isnan(rating_matrix))
    updated_rating_matrix = ((updated_rating_matrix + (1/observed_ratings_for_columns * np.nansum(rating_matrix, axis=0))).T + 1/observed_ratings_for_rows * np.nansum(rating_matrix, axis=1)).T - 1/observed_movie_user_pairs * np.nansum(rating_matrix)
   
    return updated_rating_matrix

