# Generated by Django 5.1.2 on 2024-10-22 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_filemeta_chunk_number_filemeta_chunks_processed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemeta',
            name='chunks_processed',
            field=models.IntegerField(default=0),
        ),
    ]
