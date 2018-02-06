# Generated by Django 2.0 on 2018-01-18 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picName', models.CharField(blank=True, default='', max_length=100)),
                ('picNumType', models.CharField(blank=True, default='', max_length=50)),
                ('picTypeName', models.CharField(blank=True, default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SystemPic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('systemName', models.CharField(blank=True, default='', max_length=100)),
                ('picName', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
    ]
