# Generated by Django 3.0.4 on 2022-05-07 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educative', '0002_auto_20220507_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(blank=True, to='educative.Course'),
        ),
    ]
