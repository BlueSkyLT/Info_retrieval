# Information Retrieval
NTU CI6226 Information Retrieval Assignment
### Group members

Cheng Hao, Guo Lanqing, Lan Tian, Li Ruibo, Yang Ze

## Introduction

`Information Search` is a information retrieval system. Apply Django for web program, Bootstrap for the front end, and this system includes two types of corpus: 1) Our *Novels* dataset 2) *HillaryEmails* dataset; three different search methods: 1)

### Program Structure

```
├── InforRetrieval
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py                         --entrance
├── search_web                        --a django app
│   ├── Info_retrieval
│   │   ├── HillaryEmails
│   │   │   └── index_cache.json
│   │   ├── Novels
│   │   │   └── index_cache.json
│   │   ├── components.py
│   │   └── main.py
│   ├── spider
│   │   ├── Conversion_encoding_to_utf_8.py
│   │   └── Renumber.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py                       --data require function
├── static														 --static resource
│   ├── css
│   ├── img
│   └── js
│       ├── bootstrap
│       ├── font-awesome
│       ├── jquery
│       └── simple-line-icons
└── templates														--html
    ├── content.html
    └── index.html
```

## Installation

- python 3.7
- nltk
- tqdm

## Dataset

Our *Novels* Dataset can be download [here](https://drive.google.com/open?id=1w3UlYICgyj6YP3QuZt2byIxYRkfHcSvz)

## Usage

- Clone this program to local path
- `python manage.py runserver` # run server in default port 8000
- Access Link:[http://127.0.0.1:8000/index](http://127.0.0.1:8000/index)



