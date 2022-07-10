# Generated by Django 4.0.3 on 2022-07-10 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config_name', models.CharField(db_index=True, max_length=128)),
                ('config_value', models.CharField(max_length=1024)),
            ],
        ),
    ]
