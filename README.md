![Format python code](https://github.com/Agnes-Ha/enron_network_analysis/workflows/Format%20python%20code/badge.svg)

# Enron Network Analysis

Network analysis of the Enron e-mail corpus dataset using Networkx.

## Dataset
The Enron corpus dataset used for this project is the Kaggle verion (source: https://www.kaggle.com/wcukierski/enron-email-dataset). The Kaggle version is based on the May 7, 2015 version of the dataset, as published at https://www.cs.cmu.edu/~./enron/.

**Dataset information**:
- file size: 1.32 GB
- number of unique email accounts: 259
- number of emails: 517,401

## Focus of Network Analysis
Due to the size of the dataset, preliminary analysis focused on the largest e-mail account of the dataset from the employee Vincent J. Kaminski.

### Network of Vincent Kaminski's outgoing emails
![](./docs/assets/kaminski_network.png?raw=true)

**Top 10 Correspondents**
![](./docs/assets/kaminski_network_top10.png?raw=true)

**Top 10 Degree Centrality Scores**
![](./docs/assets/kaminski_centrality.png?raw=true)