from django.contrib import admin

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

admin.site.register(Block, BlockAdmin)


class ClientAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Client, ClientAdmin)

