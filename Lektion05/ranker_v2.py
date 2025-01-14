import json

def start_ranker_v2(scores):
    with open("inverted_index.json", "r") as file:
        inverted_index = json.load(file)

    with open("crawled_data.json", "r") as file:
        crawled_data = json.load(file)
    
    new_scores = {}
    
    # 3 * score
    for page_rank in inverted_index["page_rankings"]:
        link = page_rank[0]
        if link in crawled_data and str(crawled_data[link][0]) in scores:
            new_scores.update({
                link: 3 * scores[str(crawled_data[link][0])] + page_rank[1]
            })
        else:
            new_scores.update({
                link: 3 * 0 + page_rank[1]
            })
    
    ranked_scores = get_ranked_scores(new_scores)

    return ranked_scores

def get_ranked_scores(scores):
    return sorted(scores.items(), key=lambda x:x[1], reverse=True)
    