from django.core.urlresolvers import reverse_lazy
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView, FormView)
from . import models
from . import forms

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render

#MIXINS
from django.views.generic.edit import FormMixin

# Create your views here.

#CRUD Views

class CongregationListView(ListView):
    # If you don't pass in this attribute,
    # Django will auto create a context name
    # for you with object_list!
    # Default would be 'school_list'

    # Example of making your own:
    context_object_name = 'congregations'
    model = models.Congregation

class CongregationDetailView(DetailView):
    context_object_name = 'congregation_details'
    model = models.Congregation
    template_name = 'congregations/congregation_details.html'


class CongregationCreateView(CreateView):
    #fields = ("name","street","city","zip_code","state","country","phone","email","circuit_overseer","circuit","language","access_key")
    #fields = '__all__' #Generate a form with all fields from the model
    model = models.Congregation
    form_class = forms.CongregationForm #Choosing the form I wanna use

    def get_initial(self):
        initial = super().get_initial()
        initial['added_by'] = self.request.user.username
        return initial


class CongregationUpdateView(UpdateView):
    #fields = ("name","principal")
    #fields = '__all__' #Generate a form with all fields from the model
    form_class = forms.CongregationForm #Choosing the form I wanna use
    model = models.Congregation

class CongregationDeleteView(DeleteView):
    model = models.Congregation
    success_url = reverse_lazy("index")

class MyCongregationListView(ListView):
    model = models.Congregation
    context_object_name = 'congregations'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(added_by=self.request.user.username)

class CongregationSearchView(ListView):
    template_name = 'congregations/search_result.html'
    model = models.Congregation
    context_object_name = 'congregations'
    fieldsData = {}

    def get_queryset(self):
        #add fieldData to context dictionary
        self.fieldsData['name'] = self.request.GET['name']
        self.fieldsData['city'] = self.request.GET['city']
        self.fieldsData['state'] = self.request.GET['state']
        self.fieldsData['country'] = self.request.GET['country']

        name = self.request.GET['name']
        city = self.request.GET['city']
        state = self.request.GET['state']
        country = self.request.GET['country']

        if not self.model.objects.filter(city__icontains=city):
            city = ''
        if not self.model.objects.filter(state__icontains=state):
            state = ''
        if not self.model.objects.filter(country__icontains=country):
            country = ''

        return self.model.objects.filter(name__icontains=name, city__icontains=city, state__icontains=state, country__icontains=country)

    def get_context_data(self,**kwargs):
        context  = super().get_context_data(**kwargs)
        congregation_search_form = forms.CongregationSearchForm()
        context['congregation_search_form'] = congregation_search_form
        context['fieldsData'] = self.fieldsData
        return context
