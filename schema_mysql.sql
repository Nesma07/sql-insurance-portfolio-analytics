-- ============================================================
-- Insurance Portfolio & Claims Analytics — Schema (MySQL 8.0)
-- ============================================================

CREATE DATABASE IF NOT EXISTS insurance_portfolio;
USE insurance_portfolio;

DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS claims;
DROP TABLE IF EXISTS policies;
DROP TABLE IF EXISTS agents;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id     INT PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    birth_date      DATE NOT NULL,
    gender          CHAR(1) CHECK (gender IN ('M', 'F')),
    city            VARCHAR(50) NOT NULL,
    signup_date     DATE NOT NULL
);

CREATE TABLE agents (
    agent_id        INT PRIMARY KEY,
    agent_name      VARCHAR(100) NOT NULL,
    region          VARCHAR(50) NOT NULL,
    hire_date       DATE NOT NULL
);

CREATE TABLE policies (
    policy_id       INT PRIMARY KEY,
    customer_id     INT NOT NULL,
    agent_id        INT NOT NULL,
    product_type    VARCHAR(20) NOT NULL CHECK (product_type IN ('Auto', 'Habitation', 'Sante', 'Vie')),
    start_date      DATE NOT NULL,
    end_date        DATE NOT NULL,
    premium_amount  DECIMAL(10, 2) NOT NULL,
    status          VARCHAR(20) NOT NULL CHECK (status IN ('Active', 'Expired', 'Cancelled')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
);

CREATE TABLE claims (
    claim_id        INT PRIMARY KEY,
    policy_id       INT NOT NULL,
    claim_date      DATE NOT NULL,
    claim_type      VARCHAR(50) NOT NULL,
    claim_amount    DECIMAL(10, 2) NOT NULL,
    status          VARCHAR(20) NOT NULL CHECK (status IN ('Approved', 'Rejected', 'Pending')),
    settlement_date DATE,
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
);

CREATE TABLE payments (
    payment_id      INT PRIMARY KEY,
    policy_id       INT NOT NULL,
    payment_date    DATE NOT NULL,
    amount          DECIMAL(10, 2) NOT NULL,
    payment_method  VARCHAR(20) NOT NULL CHECK (payment_method IN ('Carte', 'Virement', 'Especes', 'Cheque')),
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
);

CREATE INDEX idx_policies_customer ON policies(customer_id);
CREATE INDEX idx_policies_agent ON policies(agent_id);
CREATE INDEX idx_claims_policy ON claims(policy_id);
CREATE INDEX idx_payments_policy ON payments(policy_id);
