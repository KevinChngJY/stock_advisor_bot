# Generated by Django 3.1.2 on 2021-09-06 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasa_chatbot', '0005_option1_selection'),
    ]

    operations = [
        migrations.CreateModel(
            name='option3_stock_monitoring',
            fields=[
                ('auto_increment_id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('company_official', models.CharField(max_length=100)),
                ('company_tickname', models.CharField(max_length=100)),
                ('exchange', models.CharField(max_length=100)),
            ],
        ),
    ]