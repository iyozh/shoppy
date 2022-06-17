# Generated by Django 3.2.13 on 2022-05-28 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
