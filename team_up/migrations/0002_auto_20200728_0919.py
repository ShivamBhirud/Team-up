# Generated by Django 3.0.8 on 2020-07-28 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_up', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationstatus',
            name='comments',
            field=models.CharField(default='Not Provided', max_length=1000),
        ),
        migrations.AddField(
            model_name='applicationstatus',
            name='signal',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
