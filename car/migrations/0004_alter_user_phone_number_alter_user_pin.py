# Generated by Django 4.0.3 on 2022-03-16 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0003_alter_user_phone_number_alter_user_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='pin',
            field=models.CharField(max_length=10),
        ),
    ]
