# Generated by Django 4.2.1 on 2023-06-05 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('traits', '0003_trait_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trait',
            name='pet',
        ),
    ]