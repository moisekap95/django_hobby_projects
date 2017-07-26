from django.conf.urls import url
from congregations import views

# SET THE NAMESPACE!
app_name = 'congregations'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^list/$',views.CongregationListView.as_view(),name='list'),
    url(r'^(?P<pk>\d+)/$',views.CongregationDetailView.as_view(),name='detail'),
    url(r'^create/$',views.CongregationCreateView.as_view(),name='create'),
    url(r'^update/(?P<pk>\d+)/$',views.CongregationUpdateView.as_view(),name='update'),
    url(r'^delete/(?P<pk>\d+)/$',views.CongregationDeleteView.as_view(),name='delete'),
    url(r'^mylist/$',views.MyCongregationListView.as_view(),name='mylist'),
    url(r'^search/$',views.CongregationSearchView.as_view(),name='search'),
]
