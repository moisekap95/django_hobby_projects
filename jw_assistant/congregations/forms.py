from django import forms
from django.contrib.auth.models import User
from congregations.models import Congregation
from django.contrib.auth.password_validation import MinimumLengthValidator, UserAttributeSimilarityValidator, CommonPasswordValidator, NumericPasswordValidator

class CongregationForm(forms.ModelForm):
    name = forms.CharField(label='', help_text='', widget=forms.TextInput({'placeholder':'Congregation Name'}))
    street = forms.CharField(label='', help_text='', widget=forms.TextInput({'placeholder':'Street'}))
    city = forms.CharField(label='', help_text='', widget=forms.TextInput({'placeholder':'City'}))
    zip_code = forms.CharField(label='', help_text='', widget=forms.NumberInput({'placeholder':'Zip code or Postal code'}))
    state = forms.CharField(label='', help_text='', widget=forms.TextInput({'placeholder':'State'}))
    country = forms.CharField(label='', help_text='', widget=forms.TextInput({'placeholder':'Country'}))
    phone = forms.CharField(label='', help_text='', widget=forms.NumberInput({'placeholder':'Phone Number'}))
    email = forms.EmailField(label='', help_text='', widget=forms.EmailInput({'placeholder':'Email'}))
    circuit_overseer = forms.CharField(label='', help_text='', widget=forms.TextInput({'placeholder':'Circuit overseer'}))
    circuit = forms.CharField(label='', help_text='', widget=forms.TextInput({'placeholder':'Circuit'}))
    language = forms.CharField(label='', help_text='', widget=forms.TextInput({'placeholder':'Language'}))
    access_key = forms.CharField(label='', help_text='', widget=forms.TextInput({'placeholder':'Access Key'}))
    added_by = forms.CharField(label='', help_text='', widget=forms.TextInput({'readonly':'readonly'}))

    class Meta():
        model = Congregation
        #exclude = ['added_by']
        fields = '__all__'

class CongregationSearchForm(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter the name of your congregation (required)'}))
    city = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'City (optional)'}), required=False)
    state = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'State (optional)'}), required=False)
    country = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Country (optional)'}), required=False)
