# Generated by Django 3.1.5 on 2021-03-02 21:21

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210205_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mobile_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True),
        ),
    ]