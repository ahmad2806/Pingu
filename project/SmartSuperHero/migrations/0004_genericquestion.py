# Generated by Django 2.1.5 on 2019-01-21 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartSuperHero', '0003_delete_genericquestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
                ('keyword', models.CharField(max_length=100)),
            ],
        ),
    ]
