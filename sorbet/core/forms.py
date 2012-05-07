from random import choice
from string import letters

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Invitation

_ = lambda x: x


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_("E-mail"), max_length=75)


class EmailUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    
    It's a copy-paste from django.contrib.auth.models.UserCreationForm.
    """
    error_messages = {
        'duplicate_email': _("A user with that E-mail already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    email = forms.RegexField(label=_("E-mail"), max_length=75,
        regex=r'^[\w.@+-]+$',
        error_messages = {
            'invalid': _("This has to be a valid E-mail.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(EmailUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # username is required so we put some random data into it
        user.username = ''.join([choice(letters) for i in xrange(30)])
        if commit:
            user.save()
        return user


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email']