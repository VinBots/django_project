# Generated by Django 2.2.12 on 2022-02-20 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('input', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ghgquant',
            name='status',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
