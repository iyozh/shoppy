# Generated by Django 3.2.13 on 2022-05-19 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0003_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='code',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]