# Generated by Django 4.2.7 on 2023-11-22 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SportFacility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True, verbose_name='nazwa')),
                ('latitude', models.IntegerField()),
                ('longitude', models.IntegerField()),
                ('street_name', models.CharField(max_length=100, verbose_name='nazwa ulicy')),
                ('building_number', models.PositiveIntegerField(verbose_name='numer budynku')),
                ('is_active', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SportFacilityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sportfacility')),
            ],
        ),
        migrations.AddField(
            model_name='sportfacility',
            name='type',
            field=models.ManyToManyField(to='main.sportfacilitytype'),
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('motivation', models.TextField(blank=True, null=True)),
                ('accepted', models.BooleanField(default=False)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sportfacility')),
                ('renting_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='timeslot',
            constraint=models.CheckConstraint(check=models.Q(('start__lte', models.F('end'))), name='timeslot_start_leq_end'),
        ),
        migrations.AddConstraint(
            model_name='reservation',
            constraint=models.CheckConstraint(check=models.Q(('start__lte', models.F('end'))), name='reservation_start_leq_end'),
        ),
    ]
