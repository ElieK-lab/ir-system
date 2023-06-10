# IR System Project

This is an Information Retrieval (IR) system project coded in Python. The system has several services that interact with each other to provide search functionality.

## Endpoints

The main application connects with the following endpoints:

- Data preprocessing service
- Indexing service
- Similarity service

## Services

The following services are included in the system:

- Cluster service: This service performs clustering on the feature vectors of the documents.
- Indexing service: This service creates an index of the documents.
- Data service: This service provides access to the documents.
- Similarity service: This service computes the similarity between a query and the documents.
- Data preprocessing service: This service preprocesses the raw data to make it suitable for indexing and searching.

## Objects

The following pickle files are included in the system:

- `docs_index.pkl`: This file contains the index of the documents.
- `kmeans_clustered_features.pkl`: This file contains the clustered feature vectors of the documents.
- `svd.pkl`: This file contains the svd for clustering .
- `vectorizer.pkl`: This file contains the vectorizer object.
- `vectorized_docs.pkl`: This file contains the vectorized documents.

## JSON Files

The following JSON files are included in the system:

- `abbreviations.json`: This file contains a list of abbreviations and their expansions.
- `dataset_names.json`: This file contains a list of dataset names and their descriptions.

## Dataset Folder

The `dataset` folder contains all the data sets used in the system.

## Usage

To use the system, run the following command:

python main.py


This will start the main application, which can be accessed at `http://localhost:5000`.

## Dependencies

The following Python packages are required to run the system:

- Flask
- NumPy
- Pandas
- Scikit-learn
- NLTK

To install these packages, run the following command:

pip install -r requirements.txt

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

- This project was inspired by the book "Information Retrieval: Implementing and Evaluating Search Engines" by Stefan Büttcher, Charles L. A. Clarke, and Gordon V. Cormack.
- The dataset used in this project was obtained from [INSERT DATASET SOURCE].
"""

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

- This project was inspired by the book "Information Retrieval: Implementing and Evaluating Search Engines" by Stefan Büttcher, Charles L. A. Clarke, and Gordon V. Cormack.
- The dataset used in this project was obtained from [INSERT DATASET SOURCE].
"""