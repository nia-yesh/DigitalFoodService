from django import forms
from django.core import validators
from restaurant_admin.models import Table


class FormOrder(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FormOrder, self).__init__(*args, **kwargs)
        self.fields['tables'] = forms.ChoiceField(label="شماره میز",
                                                  choices=[(table.pk, str(table.table_number)) for table in
                                                           Table.objects.filter(table_availability=True)])

    tables = forms.ChoiceField()
    details = forms.CharField(label="جزئیات", widget=forms.Textarea, required=False)
    takeaway = forms.BooleanField(label="بیرون بر", required=False,
                                  widget=forms.CheckboxInput(
                                      attrs={'onclick': "myFunction()"}))
    botCatcher = forms.CharField(required=False, widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])
