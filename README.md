# Insurance Portfolio & Claims Analytics — SQL Project

## 📊 Overview

This project analyzes a **synthetic insurance portfolio** using **MySQL 8.0** to explore business questions related to portfolio performance, claims, customer risk, agent performance, payments, and policy renewals.

The project is designed around a relational insurance database containing **customers, agents, policies, claims, and payments**.

The analysis demonstrates how SQL can be used to transform relational data into meaningful business insights for areas such as **insurance operations, risk analysis, profitability, and customer management**.

---

## 🎯 Project Objectives

The main objectives are to:

- Analyze insurance portfolio performance across product lines
- Measure premiums and claims-related performance
- Evaluate agent sales performance
- Identify high-risk customers
- Analyze claim settlement and approval patterns
- Track premium collection over time
- Identify policies approaching expiration
- Segment customers based on their premium contribution

---

## 🗂️ Data Model

The database contains five related tables:

```text
                    ┌──────────────┐
                    │  customers   │
                    └──────┬───────┘
                           │
                           │
                    ┌──────▼───────┐
                    │   policies   │
                    └──┬────────┬──┘
                       │        │
             ┌─────────┘        └─────────┐
             ▼                            ▼
       ┌──────────┐                 ┌──────────┐
       │  claims  │                 │ payments │
       └──────────┘                 └──────────┘
                       ▲
                       │
                 ┌─────┴─────┐
                 │   agents  │
                 └───────────┘
```

### Tables

| Table | Description |
|---|---|
| `customers` | Customer information and demographics |
| `agents` | Insurance agents and their regions |
| `policies` | Insurance contracts, products, premiums and status |
| `claims` | Claims submitted against insurance policies |
| `payments` | Premium payments associated with policies |

### Main Relationships

- A customer can have multiple policies.
- An agent can manage multiple policies.
- A policy can have multiple claims.
- A policy can have multiple payment installments.

---

## 🛠️ Technologies & Tools

- **MySQL 8.0**
- **SQL**
- **Python**
- **Faker** for synthetic data generation
- **Git & GitHub**

---

## 📁 Repository Structure

```text
sql-insurance-portfolio-analytics/
│
├── schema_mysql.sql
│   └── Database creation, table definitions,
│       constraints and indexes
│
├── queries_mysql.sql
│   └── Business analysis queries
│
├── generate_data.py
│   └── Synthetic insurance data generation
│
├── customers.csv
├── agents.csv
├── policies.csv
├── claims.csv
└── payments.csv
```

---

## 🔎 Business Questions

The SQL analysis answers 12 business questions:

### 1. Portfolio Performance by Product

- How many policies does each product line have?
- How much premium is associated with each product?
- What is the average premium?

### 2. Loss Ratio by Product Line

Compare approved claims against collected premiums to identify products with higher loss exposure.

### 3. Top Performing Agents

Identify the top 10 agents based on total premium sold.

### 4. Agent Ranking by Region

Rank agents within their respective regions using SQL window functions.

### 5. Monthly Policy & Premium Trends

Analyze how the number of new policies and premium volume evolve over time.

### 6. Cumulative Premium Collection

Calculate a running total of collected premiums using a window function.

### 7. Claim Settlement Time

Measure the average number of days required to settle claims by claim type.

### 8. High-Risk Customers

Identify customers whose approved claims exceed the premiums they have paid.

### 9. Multiple-Claim Customers

Flag customers with multiple claims as candidates for additional risk review.

> This is an analytical flag, not a conclusion of fraudulent activity.

### 10. Upcoming Policy Renewals

Identify active policies approaching expiration to support renewal follow-up.

### 11. Claim Approval Rate

Compare claim approval rates across different insurance product lines.

### 12. Customer Value Segmentation

Use `NTILE()` to divide customers into quartiles according to their total premium contribution.

---

## 💻 SQL Techniques Demonstrated

This project applies several SQL techniques commonly used in data analytics:

### Joins

```sql
INNER JOIN
LEFT JOIN
```

Used to combine information across customers, policies, agents, claims and payments.

### Aggregations

```sql
COUNT()
SUM()
AVG()
GROUP BY
HAVING
```

Used to calculate portfolio metrics, premium totals, claim volumes and customer-level indicators.

### Conditional Aggregation

```sql
CASE WHEN
```

Used for metrics such as claim approval rates and approved claim amounts.

### Common Table Expressions

```sql
WITH ...
```

Used to structure multi-step analytical queries and improve readability.

### Window Functions

```sql
RANK()
SUM() OVER()
NTILE()
```

Used for:

- Regional agent rankings
- Running premium totals
- Customer value segmentation

### Subqueries

Used to build intermediate calculations and compare customer-level metrics.

### Date Analysis

MySQL date functions are used to analyze:

- Monthly trends
- Claim settlement duration
- Policy expiration
- Payment timelines

### Database Design

The schema also includes:

- Primary keys
- Foreign keys
- `CHECK` constraints
- Indexes

---

## 📈 Example Analysis

One example is the identification of high-risk customers by comparing the total premiums they have paid with the value of their approved claims.

The analysis uses multiple CTEs to separately calculate:

1. Total premiums paid by each customer
2. Total approved claims associated with each customer
3. The difference between claims and premiums

This allows customers with a negative contribution to be identified for further risk analysis.

---

## 🧪 Synthetic Data

The project uses synthetic data rather than real customer information.

The Python generation script creates realistic insurance records across:

- 500 customers
- 25 agents
- 900 policies
- 350 claims
- Multiple payment installments

The data covers several insurance products:

- Auto
- Habitation
- Sante
- Vie

Data generation uses fixed random seeds to make the dataset reproducible.

---

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/Nesma07/sql-insurance-portfolio-analytics.git
cd sql-insurance-portfolio-analytics
```

### 2. Create the database

Open `schema_mysql.sql` in MySQL 8.0 and execute it.

This creates the `insurance_portfolio` database and its tables.

### 3. Load the data

Import the CSV files into their corresponding tables.

Alternatively, generate a new synthetic dataset using:

```bash
python generate_data.py
```

### 4. Run the analysis

Open:

```text
queries_mysql.sql
```

and execute the queries in MySQL 8.0.

---

## 💡 Key Skills Demonstrated

This project demonstrates practical experience with:

**SQL**
- Relational database querying
- Multi-table joins
- CTEs
- Subqueries
- Window functions
- Aggregations
- Conditional logic
- Date analysis

**Data Analytics**
- KPI calculation
- Risk analysis
- Trend analysis
- Customer segmentation
- Performance analysis
- Business-oriented querying

**Database Concepts**
- Relational data modeling
- Primary and foreign keys
- Constraints
- Indexing

**Python**
- Synthetic data generation
- Reproducible datasets
- Data preparation

---

## 📌 Future Improvements

Potential extensions to the project include:

- Adding more insurance products and claim categories
- Building a Power BI dashboard on top of the SQL database
- Adding automated data-quality checks
- Creating stored procedures and views
- Adding more advanced risk indicators
- Developing profitability KPIs at customer and policy level
- Adding automated SQL testing

---

## 👤 Author

**Nesma Yahia**

Master's in Operational Research — USTHB

[LinkedIn](YOUR_LINKEDIN_URL) · [GitHub](https://github.com/Nesma07)

---

## 📄 License

This project is intended for educational and portfolio purposes.