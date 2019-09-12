# Generated by Django 2.2.5 on 2019-09-09 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroVehiculos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehiculo', models.IntegerField()),
                ('hora', models.CharField(max_length=4)),
                ('day', models.IntegerField()),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Vehiculo',
        ),
    ]
