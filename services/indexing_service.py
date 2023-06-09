import pickle
import os
import services.data_service as ds


def create_docs_index():
    global docs_index
    try:
        docs_index = pickle.load(
            open(os.path.join("C:\\Users\\Elie\\Desktop\\testpython\\objects\\" + ds.dataset_name + "_docs_index.pkl"),
                 'rb'))
    except FileNotFoundError:
        docs_index2 = {}
        itr = 0
        for doc in ds.get_docs_clean().values:
            for word in str(doc[2]).split():
                if word not in docs_index2:
                    docs_index2[word] = []
                docs_index2[word].append(itr)
            itr = itr + 1
        pickle.dump(docs_index2,
                    open(os.path.join(os.getcwd(), "objects", ds.dataset_name + "_docs_index.pkl"), 'wb'))
        docs_index = docs_index2
    print("Docs Index for " + ds.dataset_name + " has been loaded Successfully ..!")
    return docs_index


def create_query_index():
    global queries_index

    index = 0
    queries_clean = ds.get_queries_clean()

    for qr in queries_clean.values:
        for word in str(qr[2]).split():
            if word not in queries_index:
                queries_index[word] = []
            queries_index[word].append(index)
        index = index + 1
    return queries_index


def get_docs_index():
    return docs_index


def get_queries_index():
    return queries_index


def get_query_related_docs_ids(query):
    relevant_docs_idx = set()
    for word in query.split():
        if word in docs_index:
            for idx in docs_index[word]:
                relevant_docs_idx.add(idx)
    return relevant_docs_idx


def get_query_related_ids(query):
    relevant_queries_ids = set()
    for word in query.split():
        if word in queries_index:
            for idq in queries_index[word]:
                relevant_queries_ids.add(idq)
    return relevant_queries_ids
