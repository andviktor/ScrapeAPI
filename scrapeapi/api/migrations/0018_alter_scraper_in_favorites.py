# Generated by Django 4.2.6 on 2023-11-15 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_scraper_in_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scraper',
            name='in_favorites',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
