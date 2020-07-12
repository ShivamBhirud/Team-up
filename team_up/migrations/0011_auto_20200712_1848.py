# Generated by Django 3.0.8 on 2020-07-12 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200623_2033'),
        ('team_up', '0010_auto_20200712_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruited_teammates',
            name='teammates',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teammates', to='accounts.Extendeduser'),
        ),
        migrations.AlterField(
            model_name='teams',
            name='logged_in_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Extendeduser'),
        ),
    ]
