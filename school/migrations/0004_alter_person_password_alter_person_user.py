# Generated by Django 5.2a1 on 2025-04-11 15:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_person_user_alter_person_password'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$1000000$rXMOfnvQ5y3Md5ZnRwlvO3$tESOV8MM6DEsQ1E08gIeMw+xwMAqYY8XOiptIfU8BSE=', max_length=128),
        ),
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
