def start_ranker_v1(scores):
    return sorted(scores.items(), key=lambda x:x[1], reverse=True)
