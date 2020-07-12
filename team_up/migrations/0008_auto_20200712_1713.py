# Generated by Django 3.0.8 on 2020-07-12 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200623_2033'),
        ('team_up', '0007_auto_20200712_1356'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recruited_teammates',
            old_name='teamup_id',
            new_name='teamup_advertisement',
        ),
        migrations.AlterField(
            model_name='teams',
            name='logged_in_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Extendeduser'),
        ),
    ]
