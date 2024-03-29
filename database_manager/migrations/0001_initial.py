# Generated by Django 4.1.6 on 2023-02-05 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('user', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('link', models.URLField()),
                ('time', models.DateTimeField()),
                ('tweet_id', models.BigIntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]
