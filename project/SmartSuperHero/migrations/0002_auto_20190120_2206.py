# Generated by Django 2.1.5 on 2019-01-20 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SmartSuperHero', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SmartSuperHero.Doctor'),
        ),
    ]
