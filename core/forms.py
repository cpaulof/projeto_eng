from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput
from .models import Atracacao


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={"placeholder": "Senha"}))


 
class AtracacaoForm(forms.ModelForm):
    data_entrada = forms.DateTimeField(
        widget=DateTimePickerInput(format='%m/%d/%Y %H:%M')
    )
    class Meta:
        model = Atracacao
        fields = ['data_entrada', 'data_saida', 'berco']
        widgets = {
            #'data_entrada': DateTimePickerInput(format='%m/%d/%Y %H:%M'), # default date-format %m/%d/%Y will be used
            'data_saida': DateTimePickerInput(), # specify date-frmat
        }

class ToDoForm(forms.Form):
    todo = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    date = forms.DateTimeField(
        widget=DateTimePickerInput(format='%m/%d/%Y %H:%M')
    )

class AtracacaoForm2(forms.Form):
    berco = forms.IntegerField()
    data_entrada = forms.DateTimeField(
        widget=DateTimePickerInput(format='%m/%d/%Y %H:%M')
    )
    data_saida = forms.DateTimeField(
        widget=DateTimePickerInput(format='%m/%d/%Y %H:%M')
    )






class ToDoForm2(forms.Form):
    todo = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    date = forms.DateField(
        widget=DatePickerInput(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    reminder = forms.DateTimeField(
        required=False,
        widget=DateTimePickerInput(options={"format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False}))






