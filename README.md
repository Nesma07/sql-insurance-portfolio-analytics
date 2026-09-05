# Insurance Portfolio & Claims Analytics — SQL Project

A SQL project analyzing a synthetic insurance portfolio (policies, claims, payments,
agents, and customers) to answer real business questions an insurer's actuarial,
underwriting, and management teams would ask — profitability by product line, agent
performance, claim settlement times, high-risk customers, and renewal pipelines.

## Data model

Five related tables:

- **customers** — policyholders (demographics, signup date)
- **agents** — sales agents (region, hire date)
- **policies** — insurance contracts (product type: Auto, Habitation, Sante, Vie;
  premium, dates, status)
- **claims** — claims filed against policies (type, amount, status, settlement date)
- **payments** — premium installments paid by customers

```
customers ──< policies >── agents
                │
                ├──< claims
                └──< payments
```

Relationships: one customer can hold several policies; one agent manages several
policies; each policy can have several claims and several payment installments.

## Files

| File | Description |
|---|---|
| `schema.sql` | Table definitions, constraints, and indexes |
| `generate_data.py` | Generates 500 customers, 25 agents, 900 policies, 350 claims, and ~3,900 payments with realistic distributions (Faker-based) |
| `seed_data.sql` | Portable `INSERT` statements — no need to run Python to explore the data |
| `queries.sql` | 12 annotated business queries |
| `insurance_portfolio.db` | Ready-to-query SQLite database (schema + data already loaded) |

## Business questions answered

1. Total premiums collected and policy count by product line
2. Loss ratio by product line (claims paid ÷ premiums collected)
3. Top 10 agents by total premium sold
4. Agent ranking *within each region* (window function: `RANK() OVER (PARTITION BY ...)`)
5. Monthly trend of new policies and premium volume
6. Running total of premiums collected over time (window function)
7. Average claim settlement time by claim type
8. High-risk customers whose claims exceed the premiums they've paid (CTE + subquery)
9. Customers with multiple claims — a simple fraud/risk-review flag (`HAVING`)
10. Policies expiring in the next 30 days — renewal pipeline
11. Claim approval rate by product line
12. Customer lifetime value proxy, segmented into quartiles (`NTILE`)

## SQL techniques demonstrated

- Multi-table `JOIN`s (inner and left)
- Aggregation with `GROUP BY` / `HAVING`
- Window functions: `RANK()`, `SUM() OVER()`, `NTILE()`
- Common Table Expressions (CTEs) and correlated subqueries
- Conditional aggregation (`CASE WHEN` inside `SUM`/`COUNT`)
- Date arithmetic (`julianday`, `strftime`, `date(...)`)

## How to run it

**Option A — no setup, just explore:**
Open `insurance_portfolio.db` with [DB Browser for SQLite](https://sqlitebrowser.org/)
or the SQLite CLI and run any query from `queries.sql`.

```bash
sqlite3 insurance_portfolio.db
.read queries.sql
```

**Option B — regenerate the data from scratch:**

```bash
pip install faker
python generate_data.py
```

This recreates `insurance_portfolio.db` and rewrites `seed_data.sql` (data changes
slightly each run unless the random seed is kept fixed — it currently is, so output
is reproducible).

**Option C — load into PostgreSQL/MySQL:**
Run `schema.sql` then `seed_data.sql` on your engine of choice (minor type
adjustments may be needed, e.g. `NUMERIC` vs `DECIMAL`).

## Author

Nesma Yahia — M2 Recherche Opérationnelle, Management, Risque & Négociation (USTHB).
[LinkedIn](https://www.linkedin.com/in/nesma-yahia-801a92237/) · [GitHub](https://github.com/Nesma07)
