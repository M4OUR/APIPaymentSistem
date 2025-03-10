# Generated by Django 5.1.6 on 2025-03-05 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_discount_stripe_coupon_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='stripe_coupon_id',
        ),
        migrations.AlterField(
            model_name='order',
            name='discounts',
            field=models.ManyToManyField(blank=True, to='payments.discount'),
        ),
        migrations.AlterField(
            model_name='order',
            name='taxes',
            field=models.ManyToManyField(blank=True, to='payments.tax'),
        ),
    ]
