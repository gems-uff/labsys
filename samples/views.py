from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

class IndexView(generic.ListView):
    def get(self, request):
        return HttpResponse("result")
