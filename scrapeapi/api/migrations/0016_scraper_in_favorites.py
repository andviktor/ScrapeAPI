# Generated by Django 4.2.6 on 2023-11-15 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_element_concat_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='scraper',
            name='in_favorites',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
