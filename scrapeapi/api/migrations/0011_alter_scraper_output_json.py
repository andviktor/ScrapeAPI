# Generated by Django 4.2.6 on 2023-10-17 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_scraper_output_json'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scraper',
            name='output_json',
            field=models.JSONField(blank=True, null=True),
        ),
    ]