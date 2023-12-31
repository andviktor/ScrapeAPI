# Generated by Django 4.2.6 on 2023-10-11 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, max_length=300),
        ),
        migrations.CreateModel(
            name='Scraper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=300)),
                ('output_json', models.TextField(blank=True)),
                ('exec_datetime', models.DateTimeField()),
                ('headers', models.TextField(blank=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.project')),
            ],
        ),
    ]
