# Generated by Django 3.0.6 on 2020-05-30 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FictionRead', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='t_like',
            old_name='art',
            new_name='book',
        ),
        migrations.AlterField(
            model_name='t_book',
            name='pic',
            field=models.FileField(default='book/default.png', upload_to='book/'),
        ),
    ]
