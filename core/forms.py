from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput
from .models import Atracacao, Solicitacao


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={"placeholder": "Senha"}))


 
class AtracacaoForm(forms.ModelForm):
    class Meta:
        model = Atracacao
        fields = ['data_entrada', 'data_saida', 'berco']
        widgets = {
            'data_entrada': DateTimePickerInput(format='%m/%d/%Y %H:%M'), # default date-format %m/%d/%Y will be used
            'data_saida': DateTimePickerInput(format='%m/%d/%Y %H:%M'), # specify date-frmat
        }


        





