# Generated by Django 4.1.7 on 2023-04-11 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ModelApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='Polarity',
            field=models.CharField(default='positive', max_length=20),
            preserve_default=False,
        ),
    ]
