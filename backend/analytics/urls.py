from django.urls import path
from . import views

from .views import (dashboard_summary,
                    orders_by_hour,
                    delivery_partners,
                    feedback_categories,
                    order_status,
                    returns_summary,)


urlpatterns = [
    path("summary/", dashboard_summary),
    path('orders-by-hour/',orders_by_hour),
    path('delivery-partners/',delivery_partners),
    path('feedback-categories/',feedback_categories),
    path('order-status/',order_status),
    path('returns/',returns_summary),
    path('product-customer-analysis/',views.product_customer_analysis,),
    path('customer-feedback-analysis/',views.customer_feedback_analysis,),
]