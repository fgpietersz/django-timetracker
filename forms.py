# -*- coding: utf-8 -*-

from django import forms
from datetime import timedelta

from .models import Block, Client


class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ('project', 'cat')


class ReportForm(forms.Form):
    start = forms.DateField()
    end = forms.DateField()
    #clients = forms.ModelChoiceField(Client.objects.all())
