# Generated by Django 4.2.6 on 2023-11-17 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_alter_scraper_in_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scraper',
            name='source_json_url_field',
        ),
        migrations.AddField(
            model_name='scraper',
            name='source_scraper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.scraper'),
        ),
    ]
