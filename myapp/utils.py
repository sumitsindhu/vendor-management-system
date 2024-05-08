from datetime import timedelta
from django.db.models import Count, Avg
from .models import HistoricalPerformance
from .models import models

def update_performance_metrics(vendor):
    completed_pos = vendor.purchase_orders.filter(status='completed')
    total_completed_pos = completed_pos.count()

    if total_completed_pos > 0:
        on_time_delivery_rate = completed_pos.filter(delivery_date__lte=models.F('expected_delivery_date')).count() / total_completed_pos
        quality_rating_avg = completed_pos.exclude(quality_rating__isnull=True).aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
        average_response_time = completed_pos.exclude(acknowledgment_date__isnull=True).aggregate(avg_response=Avg(models.F('acknowledgment_date') - models.F('issue_date')))['avg_response']
        fulfillment_rate = completed_pos.filter(issues__isnull=True).count() / total_completed_pos
    else:
        on_time_delivery_rate = quality_rating_avg = average_response_time = fulfillment_rate = 0

    HistoricalPerformance.objects.update_or_create(
        vendor=vendor,
        defaults={
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time.total_seconds() / total_completed_pos if total_completed_pos > 0 else 0,
            'fulfillment_rate': fulfillment_rate,
        }
    )
