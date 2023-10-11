# Generated by Django 4.2.6 on 2023-10-11 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_project_description_scraper'),
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('xpath', models.TextField()),
                ('regex_sub', models.TextField(blank=True)),
                ('regex_search', models.TextField(blank=True)),
                ('concat_result', models.CharField(blank=True, max_length=10)),
                ('scraper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.scraper')),
            ],
        ),
    ]