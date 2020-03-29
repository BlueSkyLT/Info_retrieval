from django.shortcuts import render
from django.shortcuts import render
from django.db import connection
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import time
# Create your views here.
from search_web.Info_retrieval import components

dataset_novel = components.Dataset('Novels')
dataset_email = components.Dataset('HillaryEmails')


def index(request):
    return render(request, 'index.html')


def search(request):
    if 'title' in request.GET and request.GET['title']:
        keyword = request.GET['title']
        method = request.GET['method']
        corpus = request.GET['corpus']
        if corpus == 'Novels':
            if method == 'Method1':
                output, runtime = dataset_novel.query(keyword, 'merge_baseline')
            elif method == 'Method2':
                output, runtime = dataset_novel.query(keyword, 'merge_linear')
            else:
                output, runtime = dataset_novel.query(keyword, 'merge_linear_skip')
        elif corpus == 'Emails':
            if method == 'Method1':
                output, runtime = dataset_email.query(keyword, 'merge_baseline')
            elif method == 'Method2':
                output, runtime = dataset_email.query(keyword, 'merge_linear')
            else:
                output, runtime = dataset_email.query(keyword, 'merge_linear_skip')
        else:
            output = []
            runtime = 0
        limit = 20
        paginator = Paginator(output, limit)
        try:
            num = request.GET.get('index', 1)
            number = paginator.get_page(num)
        except:
            number = 1
        return render(request, 'index.html',
                      {'corpus': corpus, 'method': method, 'runtime': runtime, 'keyword': keyword, 'page': number,
                       'paginator': paginator})

    else:
        runtime = 0
        return render(request, 'index.html', {'runtime': runtime})


def getContent(request):
    docid = request.GET['docid']
    corpus = request.GET['corpus']
    if corpus == 'Novels':
        title = request.GET['title']
        content = dataset_novel.get(docid)
    else:
        title=''
        content = dataset_email.get(docid)
    return render(request, 'content.html', {'title': title, 'content': content})
    # def list(request,page):
    #     dataset = components.Dataset('search_web/Info_retrieval/Novels/')
    #     if 'title' in request.GET and request.GET['title']:
    #         output = dataset.query(request.GET['title'])
    #         limit=3
    #         paginator = Paginator(output, limit)
    #         try:
    #             num=request.GET.get('index',1)
    #             number=paginator.get_page(num)
    #         except PageNotAnInteger:
    #             number=paginator.page(1)
    #         except EmptyPage:
    #             number=paginator.page(paginator.num_pages)
    #
    #         return render(request, 'index.html', {'page':number,'paginator':paginator})
    #
    #     else:
    #         return render(request, 'index.html')
