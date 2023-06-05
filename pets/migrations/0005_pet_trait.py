# Generated by Django 4.2.1 on 2023-06-05 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traits', '0004_remove_trait_pet'),
        ('pets', '0004_alter_pet_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='trait',
            field=models.ManyToManyField(related_name='pets', to='traits.trait'),
        ),
    ]
