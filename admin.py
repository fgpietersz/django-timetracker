import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Client, Project, WorkCategory, Block


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'active']
    list_filter = ['active']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Project, ProjectAdmin)


class WorkCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}    

admin.site.register(WorkCategory, WorkCategoryAdmin)


class BlockAdmin(admin.ModelAdmin):
    list_display = ['project', 'cat', 'start', 'end', 'description', 'duration', 'user']
    list_filter = ['project', 'project__client', 'cat', 'user']
    date_hierarchy = 'start'
    actions = ["export_csv"]
    
    def export_csv(self, request, qs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=workblocks.csv'
        writer = csv.writer(response)
        writer.writerow(['Project', 'Category', 'Start', 'End', 'Duration', 'Done by'])
        for block in qs:
            writer.writerow([
                block.project, block.cat, block.start, block.end, block.duration().seconds / 3600, block.user
            ])
        return response

admin.site.register(Block, BlockAdmin)


class ClientAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Client, ClientAdmin)

