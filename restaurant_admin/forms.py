from __future__ import unicode_literals
from django import forms
from . import models


class InputForm(forms.Form):
    input = forms.CharField(max_length=10)


class CostForm(forms.ModelForm):
    class Meta:
        model=models.Cost
        fields='__all__'


class TableForm(forms.ModelForm):
    class Meta:
        model=models.Table
        fields='__all__'


class WorkerForm(forms.ModelForm):
    class Meta:
        model=models.Worker
        fields='__all__'


class FoodCategoryForm(forms.ModelForm):
    class Meta:
        model=models.FoodCategory
        fields='__all__'


class FoodForm(forms.ModelForm):
    class Meta:
        model=models.Food
        fields='__all__'


class PollForm(forms.ModelForm):
    class Meta:
        model=models.Poll
        fields=('question',)

class LoginForm(forms.Form):
    username = forms.CharField(required = True,max_length=156)
    password = forms.CharField(required= True, max_length= 16,widget=forms.PasswordInput)
