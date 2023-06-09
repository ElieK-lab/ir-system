from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import services.data_service as ds
from services.indexing_service import get_query_related_docs_ids
from datetime import datetime
from services.clustered_service import get_documents_from_clusters

vectorizer = TfidfVectorizer()
active_cluster = False


def get_qurey_results(query):
    clean_query_sentence = query
    docs_clean = ds.get_docs_clean()
    docs = ds.get_docs()
    last_result = []
    similarity_ranked = get_documents_from_clusters(query)
    for _, doc in similarity_ranked.iterrows():
        if doc['score'] > 0.6:
            last_result.append({
                'score': doc['score'],
                'doc_id': doc['doc_id'],
                'text': docs['text'][[doc['id']]].tolist()[0]
            })
    # if not active_cluster:
    #     related_docs_idx = get_query_related_docs_ids(str(clean_query_sentence))
    #     related_docs = list(related_docs_idx)
    #     if len(related_docs) == 0:
    #         return []
    #
    #     vector_model_docs = vectorizer.fit_transform(docs_clean['text'][related_docs])
    #
    #     ###############################        QUERY REPRESENTATION       ##################
    #     ####################################################################################
    #     vector_model_query = vectorizer.transform([clean_query_sentence])
    #
    #     ###############################             MATCHING              ##################
    #     ####################################################################################
    #
    #     similarity = cosine_similarity(vector_model_query, vector_model_docs)
    #     ###############################  RANKING THE RESULTS AND SORT IT   ##################
    #     ####################################################################################
    #
    #     results = list(enumerate(similarity[0]))
    #     sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    #     for (i, score) in sorted_results:
    #         if score > 0.6:
    #             last_result.append({
    #                 'score': score,
    #                 'doc_id': docs['doc_id'][related_docs[i]],
    #                 'text': docs['text'][related_docs[i]],
    #             })
    # else:

    return last_result


def calculate_precision_at_k(relevant_docs, retrieved_docs, k):
    retrieved_docs_at_k = retrieved_docs[:k]
    relevant_and_retrieved = set(relevant_docs).intersection(set(retrieved_docs_at_k))
    precision = len(relevant_and_retrieved) / k
    return precision


def calculate_recall(relevant_docs, retrieved_docs):
    relevant_and_retrieved = set(relevant_docs).intersection(set(retrieved_docs))
    if len(relevant_docs) == 0:
        return 0
    recall = len(relevant_and_retrieved) / len(relevant_docs)
    return recall


def calculate_precision(relevant_retrieved, not_relevant_retrieved):
    if relevant_retrieved == 0 and not_relevant_retrieved == 0:
        return 0
    return relevant_retrieved / (relevant_retrieved + not_relevant_retrieved)


def calculate_average_precision(relevant_docs, retrieved_docs):
    average_precision = 0.0
    num_relevant_docs = len(relevant_docs)
    num_correct = 0
    precision_at_rank = []

    for i, doc in enumerate(retrieved_docs):
        if doc in relevant_docs:
            num_correct += 1
            precision = num_correct / (i + 1)
            precision_at_rank.append(precision)

    if num_correct > 0:
        average_precision = sum(precision_at_rank) / num_relevant_docs

    return average_precision


def calculate_mrr(relevant_docs, retrieved_docs):
    for i, doc in enumerate(retrieved_docs):
        if doc in relevant_docs:
            return 1 / (i + 1)
    return 0


def get_evaluation_values():
    fs = 0
    count = 0

    precision_at_10_list = []
    recall_list = []
    precision_list = []
    average_precision_list = []
    mrr_list = []
    cur = datetime.now()
    queries_clean = ds.get_queries_clean()
    qrels = ds.get_qrels()
    docs_clean = ds.get_docs_clean()
    docs = ds.get_docs()

    for query in queries_clean.values:  # queries_clean.sample(n=10).values:
        query_id = list(query)[1]
        query_text = list(query)[2]
        retrieved_docs_ids, not_retrieved_docs_ids = [], []
        relevant_docs_ids = qrels.loc[qrels['query_id'] == query_id, 'doc_id'].tolist()
        not_relevant_docs_ids = []

        for doc in docs_clean.values:
            if doc[1] not in relevant_docs_ids:
                not_relevant_docs_ids.append(doc[1])
        # print(f"query_text : {query_text}")
        retrieved_docs = get_qurey_results(query_text)
        # print(retrieved_docs)
        # if len(relevant_docs_ids) > 0:
        #     retrieved_docs = retrieved_docs[:len(relevant_docs_ids)]
        if retrieved_docs is not None and len(retrieved_docs) > 0:
            retrieved_docs_ids = [doc['doc_id'] for doc in retrieved_docs]
            not_retrieved_docs_ids = list(set(docs['doc_id'].values) - set(retrieved_docs_ids))

        relevant_retrieved = len(set(relevant_docs_ids).intersection(set(retrieved_docs_ids)))
        relevant_not_retrieved = len(set(relevant_docs_ids).intersection(set(not_retrieved_docs_ids)))
        not_relevant_retrieved = len(set(not_relevant_docs_ids).intersection(set(retrieved_docs_ids)))
        not_relevant_not_retrieved = len(set(not_relevant_docs_ids).intersection(set(not_retrieved_docs_ids)))

        ############################# ######################################
        precision_at_10 = calculate_precision_at_k(relevant_docs_ids, retrieved_docs_ids, k=10)
        precision_at_10_list.append(precision_at_10)

        recall = calculate_recall(relevant_docs_ids, retrieved_docs_ids)
        recall_list.append(recall)

        precision = calculate_precision(relevant_retrieved, not_relevant_retrieved)
        precision_list.append(precision)

        average_precision = calculate_average_precision(relevant_docs_ids, retrieved_docs_ids)
        average_precision_list.append(average_precision)

        mrr = calculate_mrr(relevant_docs_ids, retrieved_docs_ids)
        mrr_list.append(mrr)
        # print(f" relevant_docs_ids         : {len(relevant_docs_ids)}")
        # print(f" not_relevant_docs_ids     : {len(not_relevant_docs_ids)}")
        # print(f" retrieved_docs_ids        : {len(retrieved_docs_ids)}")
        # print(f" not_retrieved_docs_ids    : {len(not_retrieved_docs_ids)}")
        #
        # print(f"relevant_retrieved         : {relevant_retrieved}")
        # print(f"relevant_not_retrieved     : {relevant_not_retrieved}")
        # print(f"not_relevant_retrieved     : {not_relevant_retrieved}")
        # print(f"not_relevant_not_retrieved : {not_relevant_not_retrieved}")
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        f = 0
        if precision == 0 or recall == 0:
            f = 0
        else:
            f = 2 * ((precision * recall) / (precision + recall))
        fs = fs + f
        count = count + 1

    map_score = sum(average_precision_list) / len(average_precision_list)
    avg_precision_at_10 = sum(precision_at_10_list) / len(precision_at_10_list)
    avg_recall = sum(recall_list) / len(recall_list)
    avg_precision = sum(precision_list) / len(precision_list)
    avg_mrr = sum(mrr_list) / len(mrr_list)
    mean_f_measure = fs / count

    print(f"Average Precision@10: {avg_precision_at_10}")
    print(f"Average Recall: {avg_recall}")
    print(f"Average Precision: {avg_precision}")
    print(f"Mean Average Precision (MAP): {map_score}")
    print(f"Average MRR: {avg_mrr}")
    print(f"Mean F Measure: {mean_f_measure}")
    print(f"Queries Len : {count}")

    cur2 = datetime.now()
    print(cur2 - cur)
    return {
        'average_precision_@10': avg_precision_at_10,
        'average_recall': avg_recall,
        'mean_average_precision': map_score,
        'average_mrr': avg_mrr,
        'mean_f_measure': mean_f_measure,
        'queries_count': count
    }
