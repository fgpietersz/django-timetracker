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
        messages.success(request, 'Block started')
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
    messages.success(request, 'Block %s ended' % block)
    return redirect('worktracker:control')


@login_required
def report(request):
    form = ReportForm(request.POST or None)
    if form.is_valid():
        clients = Client.objects.all()
    else:
        clients = []
    print(clients)
    # annotate instead!
    for client in clients:
        blocks = Block.objects.filter(start__range=(
            datetime.datetime.combine(form.cleaned_data['start'], datetime.time.min),
            datetime.datetime.combine(form.cleaned_data['end'], datetime.time.max)),
            project__client=client
        )
        client.total_time = sum(b.duration() for b in blocks) / 60
    grand_total = sum((c.total_time for c in clients)) 
    return render(request, 'worktracker/report.html',
                  {'form': form, 'clients': clients, 'grand_total': grand_total})

