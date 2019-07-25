import datetime
from collections import defaultdict

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from .models import Client, Project, WorkCategory, Block
from .forms import BlockForm, ReportForm


def current_block(user):
    block = Block.objects.filter(user=user).order_by('-start').first()
    if (block is not None) and (block.end is None):
        print('returning:', block)
        return block
    print('returning:', None)
    return None


@login_required
def control(request):
    block = current_block(request.user)
    print('block:', type(block))
    if not block:
        start_form = BlockForm()
    else:
        start_form = None
    return render(request, 'worktracker/control.html', {
        'start_form': start_form, 'time_block': block})


@login_required
def start(request):
    block = current_block(request.user)
    if block:
        messages.error(request, 'Already running block')
        return redirect('worktracker:control')
    start_form = BlockForm(request.POST or None)
    if start_form.is_valid():
        block = start_form.save(commit=False)
        block.user = request.user
        block.save()
        return redirect('worktracker:control')
    return render(request, 'worktracker/control.html', {
        'start_form': start_form})


@login_required
def stop(request):
    block = current_block(request.user)
    if not block:
        messages.error(request, 'No current work to stop')
        return redirect('worktracker:control')
    if not request.POST:
        return redirect('worktracker:control')
    block.end = timezone.now()
    block.save()
    return redirect('worktracker:control')


def blocks_by_client(start, end):
    clients = Client.objects.all()
    for client in clients:
        blocks = Block.objects.filter(start__range=(
            datetime.datetime.combine(start, datetime.time.min),
            datetime.datetime.combine(end, datetime.time.max)),
            project__client=client
        )
        client.total_time = sum(b.duration() for b in blocks) / 60
    grand_total = sum((c.total_time for c in clients)) 
    return clients, grand_total

def blocks_by_project(start, end):
    projects = Project.objects.all()
    for project in projects:
        blocks = Block.objects.filter(start__range=(
            datetime.datetime.combine(start, datetime.time.min),
            datetime.datetime.combine(end, datetime.time.max)),
            project=project
        )
        project.total_time = sum(b.duration() for b in blocks) / 60
    grand_total = sum((c.total_time for c in projects)) 
    return projects, grand_total


@login_required
def report(request):
    today = datetime.date.today()
    form = ReportForm(request.POST or None, inital= {'start': today, 'end': today})
    if form.is_valid():
        clients, grand_total = blocks_by_client(form.cleaned_data['start'],
                                                form.cleaned_data['end'])
    else:
        clients, grand_total = blocks_by_client(today, today)
    return render(request, 'worktracker/report.html',
                  {'form': form, 'clients': clients, 'grand_total': grand_total})
    


@login_required
def reportproject(request):
    today = datetime.date.today()
    form = ReportForm(request.POST or None, inital= {'start': today, 'end': today)
    if form.is_valid():
        projects, grand_total = blocks_by_project(form.cleaned_data['start'],
                                                form.cleaned_data['end'])
    else:
        projects, grand_total = blocks_by_project(today, today)
    return render(request, 'worktracker/reportproject.html',
                  {'form': form, 'projects': projects, 'grand_total': grand_total})
