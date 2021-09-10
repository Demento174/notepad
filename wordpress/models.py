from django.db import models

# Create your models here.


class Types(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    slug = models.SlugField(verbose_name='Slug', max_length=150)
    # thumbnail=''

class Entities(models.Model):
    type = models.ForeignKey(Types, verbose_name='Тип записи',related_name='Type', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    slug = models.SlugField(verbose_name='Slug', max_length=150)
    content = models.TextField(verbose_name='Контент', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)

class Terms(models.Model):
    type=[]
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    slug = models.SlugField(verbose_name='Slug', max_length=150)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    postTypes = models.ManyToManyField(Types,related_name='Type', blank=True, null=True)
    parent = models.ForeignKey('self',related_name='Parent',blank=True, null=True, on_delete=models.SET_NULL)
    fields = models.ManyToManyField('Fields', related_name='Field', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)

class Fields(models.Model):
    type = models.ForeignKey(Types, verbose_name='Тип записи', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    selector = models.CharField(verbose_name='Селектор', max_length=150)
    key = models.SlugField(verbose_name='Key', max_length=150)
    entityType = models.ForeignKey(Types, verbose_name='Тип записи',related_name='Type', on_delete=models.CASCADE)


class FieldsValues(models.Model):
    value=models.JSONField(verbose_name='Value', blank=True,null=True)
    field = models.ForeignKey(Fields, verbose_name='Поле',related_name='Type', on_delete=models.CASCADE)
    post = models.ForeignKey(Types, verbose_name='Запись', on_delete=models.CASCADE, blank=True)
    term = models.ForeignKey(Terms, verbose_name='Таксономия', on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)