from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'profiles'

urlpatterns = [
    url(r"login/$", auth_views.LoginView.as_view(template_name="profiles/login.html"), name='login'),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r"signup/$", views.sign_up_view, name="signup"),
    url(r'^(?P<pk>\d+)/$', views.ProfileDetailView.as_view(), name='detail'),
    url(r'^update/(?P<pk>\d+)/$', views.UserProfileUpdateView.as_view(), name='update'),
    #url(r'^delete/(?P<pk>\d+)/$', views.ProfileDeleteView.as_view(), name='delete'),
    url(r'^confirm_delete/(?P<pk>\d+)/$', views.profile_confirm_delete_view, name="confirm_delete"),
    url(r'^delete/(?P<pk>\d+)/$', views.profile_delete_view, name="delete"),
]
