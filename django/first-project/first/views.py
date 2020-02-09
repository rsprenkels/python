import operator
from collections import defaultdict

from django.http import HttpRequest
from django.shortcuts import render

def home(request):
    params = {'yourname':'My name has changed'}
    return render(request, 'home.html', params)


def about(request):
    return render(request, 'about.html')


def count(request : HttpRequest):
    fulltext = request.GET['fulltext']
    wordlist = fulltext.split()
    words = defaultdict(int)
    for word in wordlist:
        words[word] += 1
    sortedwordlist = sorted(words.items(),
        key=operator.itemgetter(1), reverse=True)
    return render(request, 'count.html', {
        'fulltext':fulltext,
        'sortedwordlist':sortedwordlist,
        'count':len(wordlist),})

