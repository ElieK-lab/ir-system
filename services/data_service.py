import pandas as pd
import json

dataset_path = "C:\\Users\\Elie\\Desktop\\testpython\\datasets\\"
dataset_name = ''


def initiate_data():
    global docs_clean, docs, qrels, queries, queries_clean, dataset_name

    with open('C:\\Users\\Elie\\Desktop\\testpython\\data_set_name.json') as json_file:
        dataset_name = json.load(json_file)['name']
    print("current dataset name :" + dataset_name)

    docs_clean = pd.read_csv(dataset_path + dataset_name + '_docs_clean.csv')
    docs = pd.read_csv(dataset_path + dataset_name + '_docs.csv')
    qrels = pd.read_csv(dataset_path + dataset_name + '_qrels.csv')
    queries = pd.read_csv(dataset_path + dataset_name + '_queries.csv')
    queries_clean = pd.read_csv(dataset_path + dataset_name + '_queries_clean.csv')
    print(dataset_name + " docs has been read")
    print(dataset_name + " docs_clean has been read")
    print(dataset_name + " queries has been read")
    print(dataset_name + " queries clean has been read")
    print(dataset_name + " qrels has been read")

    docs = docs.fillna('')
    queries = queries.fillna('')
    docs_clean = docs_clean.fillna('')
    queries_clean = queries_clean.fillna('')
    qrels = qrels.fillna('')


def get_docs():
    return docs


def get_docs_clean():
    return docs_clean


def get_queries():
    return queries


def get_queries_clean():
    return queries_clean


def get_qrels():
    return qrels


def get_dataset_name():
    return dataset_name
