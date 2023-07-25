# Generated by Django 4.2.1 on 2023-07-21 02:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.CharField(max_length=255)),
                ('rota', models.CharField(max_length=255)),
                ('ip', models.CharField(max_length=255)),
                ('latitude', models.CharField(blank=True, max_length=255, null=True)),
                ('longitude', models.CharField(blank=True, max_length=255, null=True)),
                ('metodo', models.CharField(max_length=10)),
                ('content', models.JSONField()),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
