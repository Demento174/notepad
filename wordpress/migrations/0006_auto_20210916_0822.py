# Generated by Django 3.2.7 on 2021-09-16 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordpress', '0005_entities_terms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fields',
            name='key',
        ),
        migrations.AddField(
            model_name='fieldsvalues',
            name='key',
            field=models.SlugField(default=0, max_length=150, verbose_name='Ключ-внешний ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fields',
            name='type',
            field=models.CharField(choices=[('int', 'Числовой'), ('string', 'Строковый'), ('wysiwyg', 'Редактор'), ('textArea', 'Текстовое поле'), ('text', 'текст'), ('link', 'Ссылка')], default='int', max_length=150, verbose_name='Тип поля'),
        ),
        migrations.AlterField(
            model_name='fieldsvalues',
            name='value',
            field=models.JSONField(blank=True, null=True, verbose_name='Значение'),
        ),
    ]
