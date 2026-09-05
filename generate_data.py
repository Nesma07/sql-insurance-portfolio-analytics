"""
Generates synthetic data for the Insurance Portfolio & Claims Analytics project.
Populates a SQLite database (insurance_portfolio.db) and writes a portable
seed_data.sql file with plain INSERT statements for any SQL engine.
"""
import sqlite3
import random
from datetime import date, timedelta
from faker import Faker

random.seed(42)
fake = Faker("fr_FR")
Faker.seed(42)

DB_PATH = "insurance_portfolio.db"
SCHEMA_PATH = "schema.sql"
SEED_PATH = "seed_data.sql"

N_CUSTOMERS = 500
N_AGENTS = 25
N_POLICIES = 900
N_CLAIMS = 350
PRODUCTS = ["Auto", "Habitation", "Sante", "Vie"]
REGIONS = ["Alger", "Blida", "Oran", "Constantine", "Annaba", "Setif"]
CLAIM_TYPES = {
    "Auto": ["Collision", "Vol", "Bris de glace", "Incendie"],
    "Habitation": ["Degat des eaux", "Incendie", "Vol", "Catastrophe naturelle"],
    "Sante": ["Hospitalisation", "Consultation", "Pharmacie", "Chirurgie"],
    "Vie": ["Deces", "Invalidite"],
}
PAYMENT_METHODS = ["Carte", "Virement", "Especes", "Cheque"]

def random_date(start_year=2021, end_year=2026):
    start = date(start_year, 1, 1)
    end = date(end_year, 8, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def sql_str(v):
    if v is None:
        return "NULL"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
with open(SCHEMA_PATH) as f:
    cur.executescript(f.read())
conn.commit()

seed_lines = ["-- Auto-generated seed data for Insurance Portfolio & Claims Analytics\n"]

# --- Customers ---
customers = []
for cid in range(1, N_CUSTOMERS + 1):
    gender = random.choice(["M", "F"])
    first = fake.first_name_male() if gender == "M" else fake.first_name_female()
    last = fake.last_name()
    birth = fake.date_of_birth(minimum_age=19, maximum_age=75)
    city = random.choice(REGIONS)
    signup = random_date(2021, 2026)
    customers.append((cid, first, last, birth.isoformat(), gender, city, signup.isoformat()))

cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?,?)", customers)
seed_lines.append("\n-- customers")
for c in customers:
    seed_lines.append(f"INSERT INTO customers VALUES ({', '.join(sql_str(v) for v in c)});")

# --- Agents ---
agents = []
for aid in range(1, N_AGENTS + 1):
    name = fake.name()
    region = random.choice(REGIONS)
    hire = random_date(2018, 2025)
    agents.append((aid, name, region, hire.isoformat()))

cur.executemany("INSERT INTO agents VALUES (?,?,?,?)", agents)
seed_lines.append("\n-- agents")
for a in agents:
    seed_lines.append(f"INSERT INTO agents VALUES ({', '.join(sql_str(v) for v in a)});")

# --- Policies ---
policies = []
today = date(2026, 9, 5)
for pid in range(1, N_POLICIES + 1):
    customer_id = random.randint(1, N_CUSTOMERS)
    agent_id = random.randint(1, N_AGENTS)
    product = random.choice(PRODUCTS)
    start = random_date(2022, 2026)
    duration_days = random.choice([180, 365, 730])
    end = start + timedelta(days=duration_days)
    if product == "Auto":
        premium = round(random.uniform(15000, 60000), 2)
    elif product == "Habitation":
        premium = round(random.uniform(8000, 35000), 2)
    elif product == "Sante":
        premium = round(random.uniform(10000, 45000), 2)
    else:
        premium = round(random.uniform(20000, 80000), 2)
    if end < today:
        status = random.choices(["Expired", "Cancelled"], weights=[85, 15])[0]
    else:
        status = random.choices(["Active", "Cancelled"], weights=[92, 8])[0]
    policies.append((pid, customer_id, agent_id, product, start.isoformat(), end.isoformat(), premium, status))

cur.executemany("INSERT INTO policies VALUES (?,?,?,?,?,?,?,?)", policies)
seed_lines.append("\n-- policies")
for p in policies:
    seed_lines.append(f"INSERT INTO policies VALUES ({', '.join(sql_str(v) for v in p)});")

# --- Claims ---
claims = []
policy_lookup = {p[0]: p for p in policies}
claim_policy_ids = random.sample(range(1, N_POLICIES + 1), min(N_CLAIMS, N_POLICIES))
for i, cid in enumerate(claim_policy_ids, start=1):
    pol = policy_lookup[cid]
    product = pol[3]
    pol_start = date.fromisoformat(pol[4])
    pol_end = date.fromisoformat(pol[5])
    claim_date = pol_start + timedelta(days=random.randint(1, max((pol_end - pol_start).days - 1, 1)))
    claim_type = random.choice(CLAIM_TYPES[product])
    if product == "Vie":
        amount = round(random.uniform(200000, 1500000), 2)
    elif product == "Sante":
        amount = round(random.uniform(3000, 150000), 2)
    else:
        amount = round(random.uniform(5000, 300000), 2)
    status = random.choices(["Approved", "Rejected", "Pending"], weights=[65, 20, 15])[0]
    settlement = None
    if status in ("Approved", "Rejected"):
        settlement = (claim_date + timedelta(days=random.randint(5, 60))).isoformat()
    claims.append((i, cid, claim_date.isoformat(), claim_type, amount, status, settlement))

cur.executemany("INSERT INTO claims VALUES (?,?,?,?,?,?,?)", claims)
seed_lines.append("\n-- claims")
for c in claims:
    seed_lines.append(f"INSERT INTO claims VALUES ({', '.join(sql_str(v) for v in c)});")

# --- Payments ---
payments = []
pay_id = 1
for p in policies:
    pid, _, _, _, start, end, premium, status = p
    start_d = date.fromisoformat(start)
    end_d = date.fromisoformat(end)
    n_installments = random.choice([1, 2, 4, 12])
    installment_amount = round(premium / n_installments, 2)
    span_days = max((end_d - start_d).days, 1)
    for k in range(n_installments):
        pay_date = start_d + timedelta(days=int(span_days * k / n_installments))
        if pay_date > today:
            continue
        method = random.choice(PAYMENT_METHODS)
        payments.append((pay_id, pid, pay_date.isoformat(), installment_amount, method))
        pay_id += 1

cur.executemany("INSERT INTO payments VALUES (?,?,?,?,?)", payments)
seed_lines.append("\n-- payments")
for pay in payments:
    seed_lines.append(f"INSERT INTO payments VALUES ({', '.join(sql_str(v) for v in pay)});")

conn.commit()
conn.close()

with open(SEED_PATH, "w") as f:
    f.write("\n".join(seed_lines) + "\n")

print(f"Generated {len(customers)} customers, {len(agents)} agents, {len(policies)} policies, "
      f"{len(claims)} claims, {len(payments)} payments.")
