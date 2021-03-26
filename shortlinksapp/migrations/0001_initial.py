# Generated by Django 3.1.7 on 2021-03-25 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orig_link', models.URLField()),
                ('short_link', models.URLField()),
                ('datetime', models.DateTimeField()),
                ('clicks', models.IntegerField()),
            ],
        ),
    ]
