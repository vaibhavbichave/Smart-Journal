# Generated by Django 4.1.6 on 2023-03-10 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='music',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='anger',
            field=models.FloatField(default=16.666666666666668),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fear',
            field=models.FloatField(default=16.666666666666668),
        ),
        migrations.AlterField(
            model_name='profile',
            name='joy',
            field=models.FloatField(default=16.666666666666668),
        ),
        migrations.AlterField(
            model_name='profile',
            name='love',
            field=models.FloatField(default=16.666666666666668),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sadness',
            field=models.FloatField(default=16.666666666666668),
        ),
        migrations.AlterField(
            model_name='profile',
            name='surpise',
            field=models.FloatField(default=16.666666666666668),
        ),
    ]