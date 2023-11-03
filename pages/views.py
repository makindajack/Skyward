from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    ''' template view for home page'''
    template_name = "home.html"
