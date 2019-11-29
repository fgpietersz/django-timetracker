from django.db import models
from django.conf import settings
from django.utils import timezone


class Client(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT,
                               related_name='projects')
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    class Meta:
        ordering = ['client__name', 'name']

    def __str__(self):
        return '%s - %s' % (self.client.name, self.name)


class WorkCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'work categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Block(models.Model):
    start = models.DateTimeField(default=timezone.now, db_index=True)
    end = models.DateTimeField(null=True, blank=True, db_index=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT,
                                related_name='blocks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                             related_name='work_blocks', db_index=True)
    cat = models.ForeignKey(WorkCategory, on_delete=models.PROTECT,
                            related_name='blocks', db_index=True)
    description = models.TextField(blank=True)
    class Meta:
        ordering = ['-start']

    def __str__(self):
        return '{self.project} - {self.start:%Y-%m-%d %H:%M}'.format(**locals())

    def duration(self):
        if self.end:
            return self.end - self.start
        else:
            return timezone.now() - self.start
