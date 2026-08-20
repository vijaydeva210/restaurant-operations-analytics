# Restaurant Operations & Relationship Analytics

A graph-powered web application for analyzing restaurant operations and exploring relationships between customers, orders, products, delivery partners, feedback, and returns.

## Problem Statement

Restaurants generate a large amount of operational data every day, including:

- Customer orders
- Products
- Delivery assignments
- Customer feedback
- Returns and replacements

Traditional dashboards can show individual statistics such as total orders, delivery status, or return counts.

However, understanding the relationships between these entities can provide deeper insights.

For example:

- Which delivery partners are associated with delivery-related complaints?
- Which products have the highest number of return requests?
- Which products are associated with quality-related feedback?
- What is the relationship between a customer, their orders, products, delivery partner, feedback, and returns?

This project uses a graph database to make these relationships easy to explore.

---

## Features

### Operations Dashboard

- Total orders
- Orders by time
- Order status breakdown
- Delivered orders
- Pending orders
- Cancelled orders
- Active delivery partners
- Inactive delivery partners

### Customer Feedback Analysis

- Total feedback received
- Feedback categorized by issue
- Food quality issues
- Delivery issues
- Packaging issues
- Wrong item issues
- Other issues

### Returns Analysis

- Return requests
- Replacement requests
- Return reasons
- Products associated with returns

### Relationship Explorer

Explore relationships between:

- Customers
- Orders
- Products
- Delivery partners
- Feedback
- Returns
- Feedback categories

### Graph-Based Insights

The application supports relationship-based analysis such as:

- Delivery Partner → Order → Feedback → Category
- Product → Order → Return
- Product → Order → Feedback → Category

---

## Why a Graph Database?

The main value of a graph database in this project is relationship exploration.

Restaurant data contains many interconnected entities.

For example:

```text
Delivery Partner
       |
       v
     Order
       |
       v
   Feedback
       |
       v
    Category