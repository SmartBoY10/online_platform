# Generated by Django 3.0.4 on 2022-05-09 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educative', '0005_auto_20220508_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnapprovedTeachers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher', models.ManyToManyField(to='educative.Teacher')),
            ],
        ),
    ]
