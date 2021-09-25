from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class Types(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    slug = models.SlugField(verbose_name='Slug', max_length=150)
    # thumbnail=''

    # def get_absolute_url(self):
    #     return reverse('single_news', kwargs={'pk': self.pk})
    #
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип записи'
        verbose_name_plural = 'Типы записей'
        ordering = ['title']

class Entities(models.Model):
    type = models.ForeignKey(Types,related_name='entities_type', verbose_name='Тип записи', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    slug = models.SlugField(verbose_name='Slug', max_length=150)
    content = RichTextField(config_name='default', verbose_name='Контент', blank=True, null=True)
    terms =  models.ManyToManyField('Terms',related_name='entities_terms',verbose_name='Категории,теги')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)

    def __str__(self):
        return f'{self.type.title} : {self.title}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['title']

class Terms(models.Model):
    TaxonomiesTypes = [
        ('category', 'Категория'),
        ('tag', 'Тег'),
    ]

    type = models.CharField(max_length=8, verbose_name='Тип таксономии', choices=TaxonomiesTypes, default='category')
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    slug = models.SlugField(verbose_name='Slug', max_length=150)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    postTypes = models.ManyToManyField(Types,related_name='terms_types', blank=True)
    parentTerm = models.ForeignKey('self', related_name='parent',blank=True, null=True, on_delete=models.SET_NULL)
    fields = models.ManyToManyField('Fields', related_name='terms_fields', blank=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)

    def __str__(self):
        return f'{self.type} : {self.title}'

    class Meta:
        verbose_name = 'Таксономия'
        verbose_name_plural = 'Таксономии'
        ordering = ['title']

class Fields(models.Model):
    FieldsTypes = [
        ('int', 'Числовой'),
        ('string', 'Строковый'),
        ('wysiwyg', 'Редактор'),
        ('textArea', 'Текстовое поле'),
        ('text', 'текст'),
        ('link', 'Ссылка'),
    ]

    type = models.CharField(max_length=150, verbose_name='Тип поля', choices=FieldsTypes, default='int')
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    selector = models.CharField(verbose_name='Селектор', max_length=150)

    entityType = models.ForeignKey(Types, verbose_name='Тип записи',related_name='fields_type',blank=True, null=True, on_delete=models.CASCADE)
    termType = models.ForeignKey(Terms, verbose_name='Тип Таксономии', related_name='fields_term',blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.title} <{self.type}>'

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'
        ordering = ['title', 'type']

class FieldsValues(models.Model):
    value = models.JSONField(verbose_name='Значение', blank=True,null=True)
    key = models.SlugField(verbose_name='Ключ-внешний ID', max_length=150)
    field = models.ForeignKey(Fields, verbose_name='Поле',related_name='fieldsValues_field', on_delete=models.CASCADE)
    post = models.ForeignKey(Types, verbose_name='Запись',related_name='fieldsValues_post', on_delete=models.CASCADE, blank=True, null=True)
    term = models.ForeignKey(Terms, verbose_name='Таксономия',related_name='fieldsValues_term', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)

    def save(self,*args, **kwargs):
        self.key=f'{self.field.selector}_{self.pk}'
        super().save(*args,**kwargs)


    def __str__(self):
        return f'Значение {self.field.title}'

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'
        ordering = ['field', 'post', 'term']