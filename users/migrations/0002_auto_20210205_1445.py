# Generated by Django 3.1.5 on 2021-02-05 13:45

from django.db import migrations

def create_user_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.create(name='reader')
    Group.objects.create(name='librarian')
    Group.objects.create(name='admin')


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_user_groups)
    ]
