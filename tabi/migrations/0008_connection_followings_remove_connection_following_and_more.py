# Generated by Django 4.2 on 2023-04-14 02:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tabi', '0007_delete_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='followings',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='followings', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='connection',
            name='following',
        ),
        migrations.AlterField(
            model_name='tabi',
            name='text',
            field=models.TextField(verbose_name='この旅の簡単な説明文、目標など'),
        ),
        migrations.AddField(
            model_name='connection',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
