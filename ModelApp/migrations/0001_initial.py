# Generated by Django 4.2 on 2023-04-11 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AuthApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('ReviewId', models.AutoField(primary_key=True, serialize=False)),
                ('Destination', models.CharField(max_length=300)),
                ('Description', models.CharField(max_length=300)),
                ('State', models.CharField(max_length=100)),
                ('Source', models.ForeignKey(max_length=300, null=True, on_delete=django.db.models.deletion.CASCADE, to='AuthApp.citizen')),
            ],
        ),
    ]
