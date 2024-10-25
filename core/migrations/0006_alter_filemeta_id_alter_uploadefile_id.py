# Generated by Django 5.1.2 on 2024-10-25 07:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_filemeta_chunks_processed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemeta',
            name='id',
            field=models.UUIDField(default=uuid.UUID('a0da98d6-177a-4198-b014-1ee21afde43a'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='uploadefile',
            name='id',
            field=models.UUIDField(default=uuid.UUID('d9620407-1438-4689-b7c4-519403533aa4'), editable=False, primary_key=True, serialize=False),
        ),
    ]
