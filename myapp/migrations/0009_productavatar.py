# Generated by Django 4.2.18 on 2025-02-04 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_product_product_picture_productimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAvatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_avatars/')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='avatar', to='myapp.product')),
            ],
        ),
    ]
