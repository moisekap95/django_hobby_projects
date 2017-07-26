from django import forms
from django.contrib.auth.models import User
from profiles.models import UserProfile
from congregations.models import Congregation
from django.contrib.auth.password_validation import MinimumLengthValidator, UserAttributeSimilarityValidator, CommonPasswordValidator, NumericPasswordValidator
from django.core.exceptions import ValidationError
from django.conf import settings

def DomainValidator(value):
    if '*' not in settings.ALLOWED_SIGNUP_DOMAINS:
        try:
            domain = value[value.index("@"):]
            if domain not in settings.ALLOWED_SIGNUP_DOMAINS:
                raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(','.join(settings.ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501

        except Exception:
            raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(','.join(settings.ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501

def ReservedWordsValidator(value):
    reserved_words = ['admin', 'settings', 'news', 'about', 'help',
                           'signin', 'signup', 'signout', 'terms', 'privacy',
                           'cookie', 'new', 'login', 'logout', 'administrator',
                           'join', 'account', 'username', 'root', 'blog',
                           'user', 'users', 'billing', 'subscribe', 'reviews',
                           'review', 'blog', 'blogs', 'edit', 'mail', 'email',
                           'home', 'job', 'jobs', 'contribute', 'newsletter',
                           'shop', 'profile', 'register', 'auth',
                           'authentication', 'campaign', 'config', 'delete',
                           'remove', 'forum', 'forums', 'download',
                           'downloads', 'contact', 'blogs', 'feed', 'feeds',
                           'faq', 'intranet', 'log', 'registration', 'search',
                           'explore', 'rss', 'support', 'status', 'static',
                           'media', 'setting', 'css', 'js', 'follow',
                           'activity', 'questions', 'articles', 'network', ]

    if value.lower() in reserved_words:
        raise ValidationError('This is a reserved word.')


def UsernameValidator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username. Please avoid using "@" "+" "-" in your username.')


def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')

def UniqueUsernameIgnoreCaseValidator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this Username already exists.')

class UserForm(forms.ModelForm):
    username = forms.CharField(label='', help_text=' ', widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), error_messages={'error_name':'error_messages'})
    confirm_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), error_messages={'error_name':'error_messages'})
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder':'Email address'}))
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'First name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Last name'}))

    class Meta():
        model = User
        fields = ('username', 'password', 'confirm_password', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(ReservedWordsValidator)
        self.fields['username'].validators.append(UsernameValidator)
        self.fields['username'].validators.append(UniqueUsernameIgnoreCaseValidator)
        self.fields['email'].validators.append(UniqueEmailValidator)
        self.fields['email'].validators.append(DomainValidator)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError("The two password fields must match.")
                widgets = {
                    'password': PasswordInput(attrs={'style': 'border-color:red;'}),
                    'confirm_password': PasswordInput(attrs={'class': 'error'}),
                }
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    phone = forms.CharField(label='', widget=forms.NumberInput(attrs={'placeholder':'Phone'}), required=False)
    congregation = forms.ModelChoiceField(label='', queryset=Congregation.objects.all(), empty_label="Select your congregation or add it later.", required=False)
    street = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Street'}), required=False)
    city = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'City'}), required=False)
    zip_code = forms.CharField(label='', widget=forms.NumberInput(attrs={'placeholder':'Zip code or Postal code'}), required=False)
    state = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'State'}), required=False)
    country = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Country'}), required=False)

    class Meta():
        model = UserProfile
        fields = ('profile_pic', 'congregation', 'phone', 'street', 'city', 'zip_code', 'state', 'country')

class LoginForm(forms.Form):
    username = forms.CharField(label='', help_text=' ', widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), error_messages={'error_name':'error_messages'})
