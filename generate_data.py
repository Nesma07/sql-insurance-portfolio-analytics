"""
Generates synthetic data for the Insurance Portfolio & Claims Analytics project.

The script generates CSV files only:
    - customers.csv
    - agents.csv
    - policies.csv
    - claims.csv
    - payments.csv

The generated data is designed to be imported into MySQL 8.0.
"""

import csv
import random
from datetime import date, timedelta
from faker import Faker


# ============================================================
# Configuration
# ============================================================

random.seed(42)
Faker.seed(42)

fake = Faker("fr_FR")

OUTPUT_DIR = "."

N_CUSTOMERS = 500
N_AGENTS = 25
N_POLICIES = 900
N_CLAIMS = 350

TODAY = date(2026, 9, 5)

PRODUCTS = [
    "Auto",
    "Habitation",
    "Sante",
    "Vie",
]

REGIONS = [
    "Alger",
    "Blida",
    "Oran",
    "Constantine",
    "Annaba",
    "Setif",
]

CLAIM_TYPES = {
    "Auto": [
        "Collision",
        "Vol",
        "Bris de glace",
        "Incendie",
    ],
    "Habitation": [
        "Degat des eaux",
        "Incendie",
        "Vol",
        "Catastrophe naturelle",
    ],
    "Sante": [
        "Hospitalisation",
        "Consultation",
        "Pharmacie",
        "Chirurgie",
    ],
    "Vie": [
        "Deces",
        "Invalidite",
    ],
}

PAYMENT_METHODS = [
    "Carte",
    "Virement",
    "Especes",
    "Cheque",
]


# ============================================================
# Helper Functions
# ============================================================

def random_date(start_year=2021, end_year=2026):
    """Generate a random date between the given years."""

    start = date(start_year, 1, 1)
    end = date(end_year, 8, 31)

    delta = (end - start).days

    return start + timedelta(
        days=random.randint(0, delta)
    )


def write_csv(filename, fieldnames, rows):
    """Write rows to a CSV file."""

    filepath = f"{OUTPUT_DIR}/{filename}"

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {filename}: {len(rows)} rows")


# ============================================================
# Generate Customers
# ============================================================

customers = []

for customer_id in range(1, N_CUSTOMERS + 1):

    gender = random.choice(["M", "F"])

    first_name = (
        fake.first_name_male()
        if gender == "M"
        else fake.first_name_female()
    )

    last_name = fake.last_name()

    birth_date = fake.date_of_birth(
        minimum_age=19,
        maximum_age=75
    )

    city = random.choice(REGIONS)

    signup_date = random_date(2021, 2026)

    customers.append({
        "customer_id": customer_id,
        "first_name": first_name,
        "last_name": last_name,
        "birth_date": birth_date.isoformat(),
        "gender": gender,
        "city": city,
        "signup_date": signup_date.isoformat(),
    })


write_csv(
    "customers.csv",
    [
        "customer_id",
        "first_name",
        "last_name",
        "birth_date",
        "gender",
        "city",
        "signup_date",
    ],
    customers
)


# ============================================================
# Generate Agents
# ============================================================

agents = []

for agent_id in range(1, N_AGENTS + 1):

    agents.append({
        "agent_id": agent_id,
        "name": fake.name(),
        "region": random.choice(REGIONS),
        "hire_date": random_date(2018, 2025).isoformat(),
    })


write_csv(
    "agents.csv",
    [
        "agent_id",
        "name",
        "region",
        "hire_date",
    ],
    agents
)


# ============================================================
# Generate Policies
# ============================================================

policies = []

for policy_id in range(1, N_POLICIES + 1):

    customer_id = random.randint(
        1,
        N_CUSTOMERS
    )

    agent_id = random.randint(
        1,
        N_AGENTS
    )

    product = random.choice(PRODUCTS)

    start_date = random_date(2022, 2026)

    duration_days = random.choice([
        180,
        365,
        730,
    ])

    end_date = start_date + timedelta(
        days=duration_days
    )

    # Premium ranges depend on product type
    if product == "Auto":

        premium = round(
            random.uniform(15000, 60000),
            2
        )

    elif product == "Habitation":

        premium = round(
            random.uniform(8000, 35000),
            2
        )

    elif product == "Sante":

        premium = round(
            random.uniform(10000, 45000),
            2
        )

    else:  # Vie

        premium = round(
            random.uniform(20000, 80000),
            2
        )

    # Determine policy status
    if end_date < TODAY:

        status = random.choices(
            ["Expired", "Cancelled"],
            weights=[85, 15]
        )[0]

    else:

        status = random.choices(
            ["Active", "Cancelled"],
            weights=[92, 8]
        )[0]

    policies.append({
        "policy_id": policy_id,
        "customer_id": customer_id,
        "agent_id": agent_id,
        "product": product,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "premium": premium,
        "status": status,
    })


write_csv(
    "policies.csv",
    [
        "policy_id",
        "customer_id",
        "agent_id",
        "product",
        "start_date",
        "end_date",
        "premium",
        "status",
    ],
    policies
)


# ============================================================
# Generate Claims
# ============================================================

claims = []

# Map policy IDs to their records
policy_lookup = {
    policy["policy_id"]: policy
    for policy in policies
}

# Each selected policy receives one claim
claim_policy_ids = random.sample(
    range(1, N_POLICIES + 1),
    min(N_CLAIMS, N_POLICIES)
)

for claim_id, policy_id in enumerate(
    claim_policy_ids,
    start=1
):

    policy = policy_lookup[policy_id]

    product = policy["product"]

    policy_start = date.fromisoformat(
        policy["start_date"]
    )

    policy_end = date.fromisoformat(
        policy["end_date"]
    )

    policy_duration = (
        policy_end - policy_start
    ).days

    claim_date = (
        policy_start
        + timedelta(
            days=random.randint(
                1,
                max(policy_duration - 1, 1)
            )
        )
    )

    claim_type = random.choice(
        CLAIM_TYPES[product]
    )

    # Claim amount depends on product
    if product == "Vie":

        amount = round(
            random.uniform(200000, 1500000),
            2
        )

    elif product == "Sante":

        amount = round(
            random.uniform(3000, 150000),
            2
        )

    else:

        amount = round(
            random.uniform(5000, 300000),
            2
        )

    status = random.choices(
        [
            "Approved",
            "Rejected",
            "Pending",
        ],
        weights=[
            65,
            20,
            15,
        ]
    )[0]

    settlement_date = None

    if status in ["Approved", "Rejected"]:

        settlement_date = (
            claim_date
            + timedelta(
                days=random.randint(5, 60)
            )
        ).isoformat()

    claims.append({
        "claim_id": claim_id,
        "policy_id": policy_id,
        "claim_date": claim_date.isoformat(),
        "claim_type": claim_type,
        "amount": amount,
        "status": status,
        "settlement_date": settlement_date,
    })


write_csv(
    "claims.csv",
    [
        "claim_id",
        "policy_id",
        "claim_date",
        "claim_type",
        "amount",
        "status",
        "settlement_date",
    ],
    claims
)


# ============================================================
# Generate Payments
# ============================================================

payments = []

payment_id = 1

for policy in policies:

    policy_id = policy["policy_id"]

    start_date = date.fromisoformat(
        policy["start_date"]
    )

    end_date = date.fromisoformat(
        policy["end_date"]
    )

    premium = policy["premium"]

    n_installments = random.choice([
        1,
        2,
        4,
        12,
    ])

    installment_amount = round(
        premium / n_installments,
        2
    )

    policy_duration = max(
        (end_date - start_date).days,
        1
    )

    for installment_number in range(
        n_installments
    ):

        payment_date = (
            start_date
            + timedelta(
                days=int(
                    policy_duration
                    * installment_number
                    / n_installments
                )
            )
        )

        # Do not generate future payments
        if payment_date > TODAY:
            continue

        payments.append({
            "payment_id": payment_id,
            "policy_id": policy_id,
            "payment_date": payment_date.isoformat(),
            "amount": installment_amount,
            "payment_method": random.choice(
                PAYMENT_METHODS
            ),
        })

        payment_id += 1


write_csv(
    "payments.csv",
    [
        "payment_id",
        "policy_id",
        "payment_date",
        "amount",
        "payment_method",
    ],
    payments
)


# ============================================================
# Summary
# ============================================================

print("\nData generation completed successfully.")
print(f"Customers : {len(customers)}")
print(f"Agents    : {len(agents)}")
print(f"Policies  : {len(policies)}")
print(f"Claims    : {len(claims)}")
print(f"Payments  : {len(payments)}")
print("\nCSV files are ready to import into MySQL.")
```
