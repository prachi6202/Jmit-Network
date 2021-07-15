from django import forms
from django.forms import ModelForm

from .models import event
import datetime

class DateInput(forms.DateInput):
    input_type = 'date'


class eventForm(ModelForm):
    class Meta:
        model = event
        fields = ['event_name','description','event_date','link']

        widgets = {
            'event_date': DateInput(),
        }
