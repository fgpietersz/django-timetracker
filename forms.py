# -*- coding: utf-8 -*-

from django import forms
from django.utils import timezone
from datetime import timedelta

from .models import Block, Client


class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ('project', 'cat', 'description')


class ReportForm(forms.Form):
    start = forms.DateField(initial=timezone.now())
    end = forms.DateField(initial=timezone.now())
    #clients = forms.ModelChoiceField(Client.objects.all())
