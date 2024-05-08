# Generated by Django 4.2.11 on 2024-05-07 12:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0004_historicalperformance"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="purchaseorder",
            name="vendor_reference",
        ),
        migrations.AddField(
            model_name="purchaseorder",
            name="acknowledgment_date",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="purchaseorder",
            name="delivery_date",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="purchaseorder",
            name="issue_date",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="purchaseorder",
            name="quality_rating",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="purchaseorder",
            name="vendor",
            field=models.ForeignKey(
                default=django.utils.timezone.now,
                on_delete=django.db.models.deletion.CASCADE,
                to="myapp.vendor",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="vendor",
            name="average_response_time",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="vendor",
            name="fulfillment_rate",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="vendor",
            name="on_time_delivery_rate",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="vendor",
            name="quality_rating_avg",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="items",
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="order_date",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="po_number",
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="address",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="contact_details",
            field=models.TextField(),
        ),
    ]
