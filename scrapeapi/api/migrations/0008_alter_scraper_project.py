# Generated by Django 4.2.6 on 2023-10-11 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_scraper_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scraper',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scrapers', to='api.project'),
        ),
    ]
