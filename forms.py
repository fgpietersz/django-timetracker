# -*- coding: utf-8 -*-

from django import forms
from datetime import timedelta
from django.contrib.auth import get_user_model

from .models import Block, Project


class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ('project', 'cat', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(active=True)


class ReportForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        empty_label='All', required=False)
    start = forms.DateField()
    end = forms.DateField()
    #clients = forms.ModelChoiceField(Client.objects.all())
