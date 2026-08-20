from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .database import run_query

def database_error_response(error):
    return Response(
        {"error": str(error)},
        status=status.HTTP_503_SERVICE_UNAVAILABLE,
    )


@api_view(["GET"])
def dashboard_summary(request):

    try:
        result = run_query(
            """
            MATCH (o:Order)
            RETURN
                count(o) AS total_orders,
                sum(CASE WHEN o.status = 'Delivered'
                         THEN 1 ELSE 0 END) AS delivered_orders,
                sum(CASE WHEN o.status = 'Cancelled'
                         THEN 1 ELSE 0 END) AS cancelled_orders,
                sum(o.total_amount) AS total_revenue
            """
        )

        return Response(result[0])

    except ConnectionError as error:
        return database_error_response(error)
    
@api_view(["GET"])
def orders_by_hour(request):

    result = run_query(
        """
        MATCH (o:Order)
        WITH datetime(o.order_time).hour AS hour, count(o) AS orders
        RETURN hour, orders
        ORDER BY hour
        """
    )

    return Response(result)


@api_view(["GET"])
def delivery_partners(request):

    result = run_query(
        """
        MATCH (d:DeliveryPartner)
        RETURN
            d.name AS name,
            d.status AS status
        ORDER BY name
        """
    )

    return Response(result)


@api_view(["GET"])
def feedback_categories(request):

    result = run_query(
        """
        MATCH (f:Feedback)
        WITH toLower(f.text) AS text

        RETURN
            CASE
                WHEN text CONTAINS 'delivery'
                  OR text CONTAINS 'delayed'
                  OR text CONTAINS 'late'
                  OR text CONTAINS 'driver'
                  OR text CONTAINS 'partner'
                THEN 'Delivery'

                WHEN text CONTAINS 'food'
                  OR text CONTAINS 'taste'
                  OR text CONTAINS 'quality'
                  OR text CONTAINS 'cold'
                THEN 'Food Quality'

                WHEN text CONTAINS 'package'
                  OR text CONTAINS 'packaging'
                  OR text CONTAINS 'damaged'
                  OR text CONTAINS 'spill'
                THEN 'Packaging'

                WHEN text CONTAINS 'wrong'
                  OR text CONTAINS 'missing'
                  OR text CONTAINS 'incorrect'
                THEN 'Order Issue'

                ELSE 'Other'
            END AS category,

            count(*) AS count

        ORDER BY count DESC
        """
    )

    return Response(result)

@api_view(["GET"])
def order_status(request):

    result = run_query(
        """
        MATCH (o:Order)
        RETURN
            o.status AS status,
            count(o) AS count
        ORDER BY count DESC
        """
    )

    return Response(result)


@api_view(["GET"])
def returns_summary(request):

    result = run_query(
        """
        MATCH (r:Return)
        RETURN
            r.type AS type,
            count(r) AS count
        ORDER BY count DESC
        """
    )

    return Response(result)

@api_view(["GET"])
def product_customer_analysis(request):

    result = run_query(
        """
        MATCH (c:Customer)-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product)

        RETURN
            p.name AS product,
            count(o) AS total_orders,
            count(DISTINCT c) AS unique_customers

        ORDER BY total_orders DESC
        """
    )

    return Response(result)

@api_view(["GET"])
def customer_feedback_analysis(request):

    result = run_query(
        """
        MATCH (c:Customer)-[:PLACED]->(o:Order)
              -[:HAS_FEEDBACK]->(f:Feedback)
              -[:HAS_CATEGORY]->(cat:Category)

        RETURN
            c.customer_id AS customer_id,
            cat.name AS feedback_category,
            count(f) AS feedback_count

        ORDER BY feedback_count DESC
        """
    )

    return Response(result)