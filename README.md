# AI-Powered E-Commerce Data Pipeline & Analytics Platform

## Project Overview

This project is an end-to-end **Data Engineering and Business Intelligence** portfolio project built using a real API-based workflow.

The goal of this project is to simulate how an e-commerce company can collect data from an external API, transform raw nested JSON into analytics-ready tables, load the data into PostgreSQL, create SQL analytics views, and build a Power BI dashboard for business insights.

The project combines:

- REST API extraction
- Python ETL pipeline
- JSON data processing
- PostgreSQL data warehouse
- SQL analytics views
- Power BI dashboard
- AI-assisted business insight concept

---

## Architecture

Project Architecture

```text
DummyJSON API
    ↓
Python Extraction
    ↓
Raw JSON Layer
    ↓
Python Transformation
    ↓
Processed CSV Layer
    ↓
PostgreSQL
    ↓
SQL Analytics Views
    ↓
Power BI Dashboard
```

---

## Tech Stack

| Area | Tools |
|---|---|
| Programming | Python |
| API Extraction | requests |
| Data Processing | pandas, json, pathlib |
| Database | PostgreSQL |
| Database Loading | SQLAlchemy, psycopg2 |
| Environment Variables | python-dotenv |
| Analytics | SQL |
| Visualization | Power BI |
| Version Control | Git, GitHub |

---

## Data Source

The project uses the **DummyJSON API** as the data source.

API resources used:

```text
https://dummyjson.com/products
https://dummyjson.com/users
https://dummyjson.com/carts
```

The API data includes:

- Product information
- User/customer information
- Cart/order information
- Nested product items inside carts

Each cart is treated as an order for analytics purposes.

---

## Project Structure

```text
ecommerce-ai-analytics/
│
├── data/
│   ├── raw/
│   │   └── api/
│   │       └── .gitkeep
│   └── processed/
│       └── .gitkeep
│
├── dashboard/
│   └── powerbi_screenshots/
│       └── architecture.png
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
│
├── sql/
│   └── create_views.sql
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ETL Pipeline

### 1. Extract

The extraction script connects to the DummyJSON API and downloads data from:

- `products`
- `users`
- `carts`

The script uses **limit-skip pagination** to extract all available records.

Output files:

```text
data/raw/api/products.json
data/raw/api/users.json
data/raw/api/carts.json
```

Script:

```bash
python src/extract.py
```

---

### 2. Transform

The transformation script reads the raw JSON files and converts nested API data into clean relational tables.

Created datasets:

```text
dim_customers.csv
dim_products.csv
fact_orders.csv
fact_order_items.csv
```

The transformation step includes:

- Flattening nested JSON data
- Renaming columns into clean snake_case format
- Creating dimension and fact tables
- Removing duplicate records
- Preparing data for SQL and Power BI analysis

Script:

```bash
python src/transform.py
```

---

### 3. Load

The loading script loads the processed CSV files into PostgreSQL.

PostgreSQL tables created:

```text
dim_customers
dim_products
fact_orders
fact_order_items
```

Script:

```bash
python src/load.py
```

---

## Data Model

This project follows a simple star-schema style model.

### Dimension Tables

#### `dim_customers`

Contains customer-related information such as:

- customer_id
- first_name
- last_name
- email
- phone
- age
- gender
- city
- state
- country
- company
- job_title

#### `dim_products`

Contains product-related information such as:

- product_id
- product_name
- category
- brand
- price
- discount_percentage
- rating
- stock
- availability_status

### Fact Tables

#### `fact_orders`

Contains order-level metrics such as:

- order_id
- customer_id
- total_products
- total_quantity
- total_amount
- discounted_total

#### `fact_order_items`

Contains product-level order details such as:

- order_id
- customer_id
- product_id
- product_name
- quantity
- unit_price
- total_amount
- discount_percentage
- discounted_total

---

## SQL Analytics Views

After loading the data into PostgreSQL, SQL views are created for business analysis.

Views created:

```text
vw_kpi_overview
vw_top_products
vw_revenue_by_category
vw_revenue_by_location
vw_customer_summary
vw_high_value_customers
```

These views are used as the reporting layer for Power BI.

### Example KPIs

- Total revenue
- Total orders
- Total customers
- Average order value
- Total items sold
- Total discount amount
- Top products by revenue
- Revenue by product category
- Revenue by customer location
- High-value customers

Run SQL views from:

```text
sql/create_views.sql
```

---

## Power BI Dashboard

The Power BI dashboard connects directly to PostgreSQL and uses the SQL views as reporting tables.

Dashboard pages:

### 1. Executive Overview

Includes:

- Total revenue
- Total orders
- Total customers
- Average order value
- Total items sold
- Total discount amount
- Revenue by category
- Top products by revenue
- Revenue by location
- High-value customers

### 2. Product Performance

Includes:

- Top 10 products by revenue
- Revenue by product category
- Quantity sold by product
- Product ranking

### 3. Customer & Location Insights

Includes:

- High-value customers
- Revenue by city/country
- Customer order behavior
- Average order value by customer

---

## How to Run This Project

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ecommerce-ai-analytics
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create PostgreSQL database

Create a database named:

```text
ecommerce_ai_db
```

### 5. Create `.env` file

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_ai_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

A sample file is provided as:

```text
.env.example
```

### 6. Run the ETL pipeline

```bash
python src/extract.py
python src/transform.py
python src/load.py
```

### 7. Create SQL views

Open `sql/create_views.sql` in pgAdmin Query Tool and execute it inside the `ecommerce_ai_db` database.

### 8. Connect Power BI

In Power BI Desktop:

```text
Get Data → PostgreSQL Database
```

Use:

```text
Server: localhost
Database: ecommerce_ai_db
```

Load the SQL views and build the dashboard.

---

## GitHub Note

Raw and processed data files are intentionally not uploaded to GitHub.

The following files are excluded:

```text
data/raw/api/*.json
data/processed/*.csv
.env
venv/
```

This is because the data can be regenerated by running the ETL scripts.

```bash
python src/extract.py
python src/transform.py
python src/load.py
```

This keeps the repository clean, secure, and professional.

---

## Key Learnings

Through this project, I practiced:

- Extracting data from a REST API
- Handling API pagination with limit and skip
- Saving raw JSON data in a raw data layer
- Transforming nested JSON into relational tables
- Building dimension and fact tables
- Loading CSV files into PostgreSQL
- Creating SQL analytics views
- Connecting PostgreSQL to Power BI
- Designing a business-focused analytics dashboard
- Structuring a Data Engineering portfolio project for GitHub

---

## Business Value

This project shows how an e-commerce company can use data engineering and analytics to understand:

- Which products generate the most revenue
- Which categories perform best
- Which customers have the highest value
- How revenue differs by customer location
- How discounts affect overall sales performance

The final Power BI dashboard helps business users monitor key sales KPIs and make better decisions.

---

## Future Improvements

Possible next improvements:

- Add Apache Airflow for pipeline orchestration
- Store raw and processed files in Azure Blob Storage
- Load data into Azure SQL Database
- Add automated data quality checks
- Add AI-generated business insight summaries
- Schedule the pipeline to run daily
- Add Docker support for local deployment

---

## Project Status

Current status:

- API extraction completed
- Data transformation completed
- PostgreSQL loading completed
- SQL analytics views completed
- Power BI dashboard in progress

---

## Author

**Prajwal Tamang**  
MSc Data Science Student  
Aspiring Data Engineer / Data Analyst
