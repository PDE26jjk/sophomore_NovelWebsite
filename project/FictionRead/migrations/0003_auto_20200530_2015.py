# Generated by Django 3.0.6 on 2020-05-30 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FictionRead', '0002_auto_20200530_2001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='t_coll',
            old_name='art',
            new_name='book',
        ),
    ]
