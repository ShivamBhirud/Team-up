# Generated by Django 3.0.8 on 2020-07-22 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logged_in_user', models.CharField(max_length=100, null=True)),
                ('requester', models.CharField(max_length=100, null=True)),
                ('teamup_advertisement', models.IntegerField(null=True)),
                ('status', models.CharField(default='NA', max_length=2, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('relevant_url', models.URLField(default='Not Provided')),
                ('pub_date', models.DateTimeField(blank=True, null=True)),
                ('short_description', models.TextField(default='Not Provided', max_length=200)),
                ('description', models.TextField(default='Not Provided', max_length=2000)),
                ('vacancy', models.IntegerField(default=1)),
                ('logged_in_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Extendeduser')),
            ],
        ),
        migrations.CreateModel(
            name='RecruitedTeammates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teammates', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teammates', to='accounts.Extendeduser')),
                ('teamup_advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Tup_Advertisement', to='team_up.Teams')),
            ],
        ),
    ]
