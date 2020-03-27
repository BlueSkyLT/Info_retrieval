# Information Retrieval
NTU CI6226 Information Retrieval Assignment 1

### Group members

Chen Hao

Guo Lanqing

Lan Tian

Li Ruibo

Yang Ze

# Installation

Python 3.7

**packages**

- Whoosh 2.7.4
- nltk
- tqdm

# Dataset

# Usage

place the *DATASET_DIRECTORY* under ```Infor_retrieval/```

```cd Info_retrieval```

```python indexing.py DATASET_DIRECTORY```


to search the first *NUMBER_OF_RESULTS* documents containing *QUERY_TERM* in *title*, *author* or *content*:

```python search.py QUERY_TERM title NUMBER_OF_RESULTS```

```python search.py QUERY_TERM author NUMBER_OF_RESULTS```

```python search.py QUERY_TERM content NUMBER_OF_RESULTS```
