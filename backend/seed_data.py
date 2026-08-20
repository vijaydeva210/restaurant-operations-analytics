import os
import random
from datetime import datetime, timedelta

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

uri = os.getenv("COGNODB_URI")
username = os.getenv("COGNODB_USERNAME")
password = os.getenv("COGNODB_PASSWORD")

driver = GraphDatabase.driver(
    uri,
    auth=(username, password)
)


def run_query(query, parameters=None):
    with driver.session() as session:
        result=session.run(query, parameters)
        return result.data()


# --------------------------------------------------
# Clear existing graph
# --------------------------------------------------

run_query("MATCH (n) DETACH DELETE n")


# --------------------------------------------------
# Categories
# --------------------------------------------------

categories = [
    "Food Quality",
    "Delivery",
    "Packaging",
    "Wrong Item",
    "Other"
]

for category in categories:
    run_query(
        """
        MERGE (c:Category {name: $name})
        """,
        {"name": category}
    )


# --------------------------------------------------
# Customers
# --------------------------------------------------

customers = [
    ("C001", "Rahul", "Hyderabad"),
    ("C002", "Priya", "Hyderabad"),
    ("C003", "Arjun", "Secunderabad"),
    ("C004", "Sneha", "Kukatpally"),
    ("C005", "Vikram", "Madhapur"),
    ("C006", "Anjali", "Gachibowli"),
    ("C007", "Kiran", "Ameerpet"),
    ("C008", "Neha", "Hitech City"),
    ("C009", "Rohit", "Kondapur"),
    ("C010", "Divya", "Begumpet"),
]

for customer_id, name, location in customers:
    run_query(
        """
        MERGE (c:Customer {customer_id: $customer_id})
        SET c.name = $name,
            c.location = $location
        """,
        {
            "customer_id": customer_id,
            "name": name,
            "location": location
        }
    )


# --------------------------------------------------
# Products
# --------------------------------------------------

products = [
    ("P001", "Chicken Biryani", "Main Course", 280),
    ("P002", "Veg Biryani", "Main Course", 220),
    ("P003", "Paneer Butter Masala", "Main Course", 240),
    ("P004", "Chicken 65", "Starter", 210),
    ("P005", "Paneer Tikka", "Starter", 190),
    ("P006", "Masala Dosa", "Breakfast", 120),
    ("P007", "Chicken Fried Rice", "Main Course", 230),
    ("P008", "Veg Noodles", "Main Course", 180),
    ("P009", "Gulab Jamun", "Dessert", 90),
    ("P010", "Lime Soda", "Beverage", 70),
]

for product_id, name, category, price in products:
    run_query(
        """
        MERGE (p:Product {product_id: $product_id})
        SET p.name = $name,
            p.category = $category,
            p.price = $price
        """,
        {
            "product_id": product_id,
            "name": name,
            "category": category,
            "price": price
        }
    )


# --------------------------------------------------
# Delivery Partners
# --------------------------------------------------

delivery_partners = [
    ("D001", "Amit", "Active"),
    ("D002", "Suresh", "Active"),
    ("D003", "Manoj", "Active"),
    ("D004", "Ravi", "Active"),
    ("D005", "Naveen", "Inactive"),
    ("D006", "Imran", "Active"),
    ("D007", "Sai", "Inactive"),
    ("D008", "Varun", "Active"),
]

for partner_id, name, status in delivery_partners:
    run_query(
        """
        MERGE (d:DeliveryPartner {partner_id: $partner_id})
        SET d.name = $name,
            d.status = $status
        """,
        {
            "partner_id": partner_id,
            "name": name,
            "status": status
        }
    )


# --------------------------------------------------
# Orders
# --------------------------------------------------

random.seed(42)

order_statuses = [
    "Confirmed",
    "Preparing",
    "Out for Delivery",
    "Delivered",
    "Cancelled"
]

start_time = datetime(2026, 8, 20, 8, 0)

orders = []

for i in range(1, 101):
    order_id = f"O{i:03d}"

    order_time = start_time + timedelta(
        minutes=random.randint(0, 840)
    )

    customer_id = random.choice(customers)[0]
    product_id = random.choice(products)[0]
    partner_id = random.choice(delivery_partners)[0]

    status = random.choices(
        order_statuses,
        weights=[15, 15, 15, 45, 10]
    )[0]

    product_price = next(
        p[3] for p in products if p[0] == product_id
    )

    total_amount = product_price + random.choice([20, 30, 40, 50])

    orders.append(
        (
            order_id,
            order_time,
            customer_id,
            product_id,
            partner_id,
            status,
            total_amount
        )
    )

    run_query(
        """
        MATCH (c:Customer {customer_id: $customer_id})
        MATCH (p:Product {product_id: $product_id})
        MATCH (d:DeliveryPartner {partner_id: $partner_id})

        MERGE (o:Order {order_id: $order_id})

        SET o.order_time = $order_time,
            o.status = $status,
            o.total_amount = $total_amount

        MERGE (c)-[:PLACED]->(o)
        MERGE (o)-[:CONTAINS]->(p)
        MERGE (o)-[:ASSIGNED_TO]->(d)
        """,
        {
            "order_id": order_id,
            "order_time": order_time.isoformat(),
            "customer_id": customer_id,
            "product_id": product_id,
            "partner_id": partner_id,
            "status": status,
            "total_amount": total_amount
        }
    )


# --------------------------------------------------
# Feedback
# --------------------------------------------------

feedback_templates = {
    "Food Quality": [
        "Food was not fresh",
        "Food quality was poor",
        "Taste was not good",
        "Food arrived cold"
    ],
    "Delivery": [
        "Delivery was very late",
        "Delivery partner was delayed",
        "Order took too long to arrive"
    ],
    "Packaging": [
        "Packaging was damaged",
        "Food container was leaking",
        "Packaging was not secure"
    ],
    "Wrong Item": [
        "Received the wrong item",
        "One item was missing",
        "Order did not match what I requested"
    ],
    "Other": [
        "Overall experience was average",
        "Service could be improved"
    ]
}

feedback_count = 1

for order in orders:
    order_id = order[0]

    if random.random() < 0.65:
        category = random.choice(categories)
        text = random.choice(feedback_templates[category])

        feedback_id = f"F{feedback_count:03d}"
        feedback_count += 1

        created_at = order[1] + timedelta(
            minutes=random.randint(10, 120)
        )

        run_query(
            """
            MATCH (o:Order {order_id: $order_id})
            MATCH (c:Category {name: $category})

            CREATE (f:Feedback {
                feedback_id: $feedback_id,
                text: $text,
                created_at: $created_at
            })

            CREATE (o)-[:HAS_FEEDBACK]->(f)
            CREATE (f)-[:HAS_CATEGORY]->(c)
            """,
            {
                "order_id": order_id,
                "category": category,
                "feedback_id": feedback_id,
                "text": text,
                "created_at": created_at.isoformat()
            }
        )


# --------------------------------------------------
# Returns / Replacements
# --------------------------------------------------

return_reasons = [
    "Food quality issue",
    "Wrong item",
    "Damaged packaging",
    "Missing item"
]

return_types = ["Return", "Replacement"]
return_statuses = [
    "Requested",
    "Approved",
    "Completed",
    "Rejected"
]

return_count = 1

for order in orders:
    order_id = order[0]
    product_id = order[3]

    if random.random() < 0.20:
        return_id = f"R{return_count:03d}"
        return_count += 1

        reason = random.choice(return_reasons)
        return_type = random.choice(return_types)
        return_status = random.choice(return_statuses)

        requested_at = order[1] + timedelta(
            minutes=random.randint(30, 180)
        )

        run_query(
            """
            MATCH (o:Order {order_id: $order_id})
            MATCH (p:Product {product_id: $product_id})

            CREATE (r:Return {
                return_id: $return_id,
                reason: $reason,
                type: $return_type,
                status: $return_status,
                requested_at: $requested_at
            })

            CREATE (o)-[:HAS_RETURN]->(r)
            CREATE (r)-[:FOR_PRODUCT]->(p)
            """,
            {
                "order_id": order_id,
                "product_id": product_id,
                "return_id": return_id,
                "reason": reason,
                "return_type": return_type,
                "return_status": return_status,
                "requested_at": requested_at.isoformat()
            }
        )


# --------------------------------------------------
# Summary
# --------------------------------------------------

result = run_query(
    """
    MATCH (n)
    RETURN labels(n)[0] AS type, count(n) AS count
    ORDER BY type
    """
)

print("\nDatabase seeded successfully!\n")

for record in result:
    print(f"{record['type']}: {record['count']}")


driver.close()