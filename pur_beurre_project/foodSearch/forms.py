from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.forms.utils import ErrorList

from  django.contrib.auth.models import User


class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {

            'username': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
        }
