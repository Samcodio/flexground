from django.forms import forms
from django.contrib.auth.forms import UserCreationForm
from take_app.models import CustomUser


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

        def save(self, commit=True):
            user = super(CreateUserForm, self).save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.password1 = self.cleaned_data['password1']
            user.password2 = self.cleaned_data['password2']

            if commit:
                user.save()
                return user



