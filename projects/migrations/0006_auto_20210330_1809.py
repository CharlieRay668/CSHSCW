# Generated by Django 3.1.7 on 2021-03-31 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_project_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='deadline',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='title',
            field=models.CharField(default='Default Title', max_length=50),
            preserve_default=False,
        ),
    ]
