# Generated by Django 4.1.6 on 2023-02-06 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_id',
            field=models.BigIntegerField(),
        ),
    ]
