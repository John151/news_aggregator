# Generated by Django 3.2 on 2021-05-11 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bestnews_site', '0002_auto_20210511_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]