# Generated by Django 3.2 on 2023-12-16 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='reviews',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='titles',
            options={'ordering': ('id',)},
        ),
    ]
