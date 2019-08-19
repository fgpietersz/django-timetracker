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
    if block is not None:
        return block, not bool(block.end)
    return None, False

def get_recent_blocks(user):
    start = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    return Block.objects.filter(user=user, start__gte=start).select_related(
        'project', 'project__client')
    
    

@login_required
def control(request):
    block, current = current_block(request.user)
    recent_blocks = get_recent_blocks(request.user)
    if not block:
        start_form = BlockForm()
    elif block.end:
        start_form = BlockForm(
            initial={'project': block.project, 'cat': block.cat})
    else:
        start_form = None
    print('recent_blocks:', type(block))
    return render(request, 'worktracker/control.html', {
        'start_form': start_form,
        'time_block': block if current else None})


@login_required
def start(request):
    block, current = current_block(request.user)
    if current:
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
    block, _ = current_block(request.user)
    if not block:
        messages.error(request, 'No current work to stop')
        return redirect('worktracker:control')
    if not request.POST:
        return redirect('worktracker:control')
    block.end = timezone.now()
    block.save()
    return redirect('worktracker:control')


# TODO replace below with queries with annotations
# TODO abstract out - not DRY
def blocks_by_client(user, start, end):
    clients = Client.objects.all()
    for client in clients:
        blocks = Block.objects.filter(start__range=(
            datetime.datetime.combine(start, datetime.time.min),
            datetime.datetime.combine(end, datetime.time.max)),
            project__client=client
        )
        if user:
            blocks = blocks.filter(user=user)
        client.total_time = sum((b.duration() for b in blocks),
                                datetime.timedelta(0))
    grand_total = sum((c.total_time for c in clients), datetime.timedelta(0)) 
    return clients, grand_total


def blocks_by_project(user, start, end):
    projects = Project.objects.all()
    for project in projects:
        blocks = Block.objects.filter(start__range=(
            datetime.datetime.combine(start, datetime.time.min),
            datetime.datetime.combine(end, datetime.time.max)),
            project=project
        )
        if user:
            blocks = blocks.filter(user=user)
        project.total_time = sum ((b.duration() for b in blocks),
                                  datetime.timedelta(0))
    grand_total = sum((c.total_time for c in projects), datetime.timedelta(0)) 
    return projects, grand_total


@login_required
def report(request):
    today = datetime.date.today()
    form = ReportForm(request.POST or None,
                      initial = {'user': request.user, 'start': today, 'end': today})
    if form.is_valid():
        clients, grand_total = blocks_by_client(
            form.cleaned_data['user'],
            form.cleaned_data['start'], form.cleaned_data['end'],
        )
    else:
        clients, grand_total = blocks_by_client(request.user, today, today)
    return render(request, 'worktracker/report.html',
                  {'form': form, 'clients': clients, 'grand_total': grand_total})
    

@login_required
def reportproject(request):
    today = datetime.date.today()
    form = ReportForm(request.POST or None,
                      initial = {'user': request.user, 'start': today, 'end': today})
    if form.is_valid():
        projects, grand_total = blocks_by_project(
            form.cleaned_data['user'], form.cleaned_data['start'],
            form.cleaned_data['end'])
    else:
        projects, grand_total = blocks_by_project(request.user, today, today)
    return render(request, 'worktracker/reportproject.html',
                  {'form': form, 'projects': projects, 'grand_total': grand_total})
