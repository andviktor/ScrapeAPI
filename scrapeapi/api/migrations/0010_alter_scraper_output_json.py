# Generated by Django 4.2.6 on 2023-10-13 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_element_title_alter_scraper_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scraper',
            name='output_json',
            field=models.JSONField(null=True),
        ),
    ]
