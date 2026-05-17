-- 1. Revenue by product category
CREATE OR REPLACE VIEW vw_revenue_by_category AS
SELECT
    p.category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    SUM(oi.quantity) AS total_quantity_sold,
    ROUND(SUM(oi.discounted_total)::numeric, 2) AS total_revenue,
    ROUND(AVG(oi.unit_price)::numeric, 2) AS avg_unit_price
FROM fact_order_items oi
LEFT JOIN dim_products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- 2. Top 10 products by revenue
CREATE OR REPLACE VIEW vw_top_products AS
SELECT
    oi.product_id,
    oi.product_name,
    p.category,
    SUM(oi.quantity) AS total_quantity_sold,
    ROUND(SUM(oi.discounted_total)::numeric, 2) AS total_revenue,
    RANK() OVER (ORDER BY SUM(oi.discounted_total) DESC) AS revenue_rank
FROM fact_order_items oi
LEFT JOIN dim_products p
    ON oi.product_id = p.product_id
GROUP BY
    oi.product_id,
    oi.product_name,
    p.category
ORDER BY total_revenue DESC
LIMIT 10;


-- 3. Customer order summary
CREATE OR REPLACE VIEW vw_customer_summary AS
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.gender,
    c.age,
    c.city,
    c.state,
    c.country,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.discounted_total)::numeric, 2) AS customer_revenue,
    ROUND(AVG(o.discounted_total)::numeric, 2) AS avg_order_value
FROM dim_customers c
LEFT JOIN fact_orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.gender,
    c.age,
    c.city,
    c.state,
    c.country
ORDER BY customer_revenue DESC;


-- 4. Revenue by customer location
CREATE OR REPLACE VIEW vw_revenue_by_location AS
SELECT
    c.country,
    c.state,
    c.city,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    ROUND(SUM(o.discounted_total)::numeric, 2) AS total_revenue,
    ROUND(AVG(o.discounted_total)::numeric, 2) AS avg_order_value
FROM fact_orders o
LEFT JOIN dim_customers c
    ON o.customer_id = c.customer_id
GROUP BY
    c.country,
    c.state,
    c.city
ORDER BY total_revenue DESC;


-- 5. Main KPI overview
CREATE OR REPLACE VIEW vw_kpi_overview AS
SELECT
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS total_customers,
    SUM(o.total_quantity) AS total_items_sold,
    ROUND(SUM(o.discounted_total)::numeric, 2) AS total_revenue,
    ROUND(AVG(o.discounted_total)::numeric, 2) AS avg_order_value,
    ROUND(SUM(o.total_amount - o.discounted_total)::numeric, 2) AS total_discount_amount
FROM fact_orders o;


-- 6. High-value customers
CREATE OR REPLACE VIEW vw_high_value_customers AS
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.gender,
    c.age,
    c.city,
    c.country,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.discounted_total)::numeric, 2) AS total_spent,
    RANK() OVER (ORDER BY SUM(o.discounted_total) DESC) AS customer_rank
FROM dim_customers c
JOIN fact_orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.gender,
    c.age,
    c.city,
    c.country
ORDER BY total_spent DESC;
