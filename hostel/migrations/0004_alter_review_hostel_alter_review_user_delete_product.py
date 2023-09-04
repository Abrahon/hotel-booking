# Generated by Django 4.2.4 on 2023-09-04 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0003_product_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='hostel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hostel_reviews', to='hostel.hotel'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to='hostel.hotel'),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]