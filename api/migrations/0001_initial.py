# Generated by Django 2.1.7 on 2019-03-12 03:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('index', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('company', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('food_type', models.CharField(choices=[('F', 'Fruit'), ('V', 'Vegetable'), ('U', 'Unknown')], default='U', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('index', models.IntegerField(primary_key=True, serialize=False)),
                ('_id', models.CharField(blank=True, max_length=64, null=True, unique=True)),
                ('guid', models.CharField(blank=True, max_length=64, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('has_died', models.BooleanField(blank=True, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True)),
                ('picture', models.URLField(blank=True, null=True)),
                ('eye_color', models.CharField(blank=True, max_length=10, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('phone', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('address', models.TextField(blank=True, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('registered', models.DateField(blank=True, null=True)),
                ('greeting', models.TextField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='api.Company')),
                ('favourite_food', models.ManyToManyField(to='api.Food')),
                ('friends', models.ManyToManyField(blank=True, to='api.People')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='people',
            name='tags',
            field=models.ManyToManyField(to='api.Tags'),
        ),
    ]
