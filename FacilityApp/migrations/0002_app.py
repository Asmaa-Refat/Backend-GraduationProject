# Generated by Django 4.1.7 on 2023-04-11 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FacilityApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('facility_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FacilityApp.facility')),
                ('rate', models.IntegerField()),
            ],
            bases=('FacilityApp.facility',),
        ),
    ]
