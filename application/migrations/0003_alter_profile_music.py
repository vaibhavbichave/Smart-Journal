# Generated by Django 4.1.6 on 2023-03-10 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_profile_music_alter_profile_anger_alter_profile_fear_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='music',
            field=models.CharField(default='1999', max_length=100),
        ),
    ]