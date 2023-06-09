# Generated by Django 4.2 on 2023-04-09 03:36

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0004_alter_tag_id_alter_taggeditem_content_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tabi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='タイトル(32文字まで)')),
                ('text', models.TextField(verbose_name='この旅の簡単な説明文')),
                ('money', models.TextField(verbose_name='一人当たりの費用')),
                ('date', models.CharField(max_length=8, verbose_name='日数 (例)二泊三日、日帰り...')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='', verbose_name='サムネイル写真')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('daylooked', models.IntegerField(default=0)),
                ('weeklylooked', models.IntegerField(default=0)),
                ('looked', models.PositiveIntegerField(default=0)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
