from django.views.generic import ListView
from congregations.models import Congregation
from congregations.forms import CongregationSearchForm

class IndexView(ListView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    context_object_name = 'congregations'
    model = Congregation
    template_name = 'index.html'

    def get_context_data(self,**kwargs):
        context  = super().get_context_data(**kwargs)
        congregation_search_form = CongregationSearchForm()
        context['congregation_search_form'] = congregation_search_form
        return context
