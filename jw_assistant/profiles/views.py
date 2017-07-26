from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404
from . import forms
from . import models
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView, FormView)

from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.models import User

# extra for profiles deletion
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

from django.core.exceptions import ObjectDoesNotExist

def sign_up_view(request):

    registered = False

    user_form_errors = []
    profile_form_errors = []

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = forms.UserForm(data=request.POST) #To get validated data --> form.cleaned_data['subject']..
        profile_form = forms.UserProfileForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)
            for error in user_form.errors:
                user_form_errors.append(error)
            for error in profile_form_errors:
                profile_form_errors.append(error)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = forms.UserForm()
        profile_form = forms.UserProfileForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'profiles/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered,
                           'user_form_errors':user_form_errors,
                           'profile_form_errors':profile_form_errors})

class ProfileDetailView(DetailView):
    #context_object_name = 'profile_details'
    model = User
    template_name = 'profiles/profile_details.html'

    def get_context_data(self,**kwargs):
        context  = super().get_context_data(**kwargs)
        try:
            profile_details = models.UserProfile.objects.get(user=self.request.user)
            context['profile_details'] = profile_details
        except ObjectDoesNotExist:
            profile_details = User.objects.get(pk=self.request.user.pk)
            context['profile_details'] = profile_details
        return context

class UserProfileUpdateView(UpdateView):
    #fields = '__all__'
    template_name = 'profiles/profile_form.html'
    form_class = forms.UserForm
    model = User

class ProfileDeleteView(DeleteView):
    model = models.UserProfile
    success_url = reverse_lazy("profiles:logout")

def profile_confirm_delete_view(request, pk):
    return render(request, 'profiles/userprofile_confirm_delete.html',
                  {'pk':pk})

def profile_delete_view(request, pk):
    profile_to_delete = get_object_or_404(User, pk=pk)
    profile_to_delete.delete()
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))
