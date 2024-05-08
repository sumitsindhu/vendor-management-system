# Generated by Django 4.2.11 on 2024-05-06 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0003_purchaseorder"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalPerformance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField()),
                ("on_time_delivery_rate", models.FloatField(default=0)),
                ("quality_rating_avg", models.FloatField(default=0)),
                ("average_response_time", models.FloatField(default=0)),
                ("fulfillment_rate", models.FloatField(default=0)),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="myapp.vendor"
                    ),
                ),
            ],
        ),
    ]
