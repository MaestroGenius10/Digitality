# Generated by Django 4.2.18 on 2025-01-27 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_paymentcard_card_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentcard',
            name='cvv',
            field=models.CharField(max_length=3),
        ),
    ]
