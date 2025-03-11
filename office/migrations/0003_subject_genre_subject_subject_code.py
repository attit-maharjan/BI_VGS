# Generated by Django 5.1.5 on 2025-03-08 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0002_alter_person_role_alter_classsubject_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='genre',
            field=models.CharField(choices=[('COMP', 'Compulsory'), ('ELEC', 'Elective')], default='COMP', max_length=4),
        ),
        migrations.AddField(
            model_name='subject',
            name='subject_code',
            field=models.CharField(choices=[('MATH', 'Mathematics'), ('SCI', 'Science'), ('ENG', 'English'), ('HIST', 'History'), ('ART', 'Art'), ('MUS', 'Music'), ('CS', 'Computer Science'), ('LANG', 'Foreign Language')], default='DEFAULT', max_length=4, unique=True),
        ),
    ]
