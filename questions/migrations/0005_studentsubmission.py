# Generated by Django 2.0.2 on 2018-02-15 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20180215_0649'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('email', models.TextField(default='')),
                ('data', models.TextField(default='')),
            ],
        ),
    ]
