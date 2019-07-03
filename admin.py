from django.contrib import admin

from .models import Client, Project, WorkCategory, Block


admin.site.register(Client)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'client']

admin.site.register(Project, ProjectAdmin)


admin.site.register(WorkCategory)


class BlockAdmin(admin.ModelAdmin):
    list_display = ['project', 'cat', 'start', 'end', 'duration']
    list_filter = ['project', 'project__client', 'cat', 'user']
    date_hierarchy = 'start'

admin.site.register(Block, BlockAdmin)
