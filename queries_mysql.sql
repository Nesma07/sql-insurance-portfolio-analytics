-- ============================================================
-- Insurance Portfolio & Claims Analytics — Business Queries (MySQL 8.0)
-- ============================================================
USE insurance_portfolio;

-- 1) TOTAL PREMIUMS COLLECTED AND POLICY COUNT BY PRODUCT LINE
SELECT
    product_type,
    COUNT(*)                       AS nb_policies,
    ROUND(SUM(premium_amount), 2)  AS total_premium,
    ROUND(AVG(premium_amount), 2)  AS avg_premium
FROM policies
GROUP BY product_type
ORDER BY total_premium DESC;


-- 2) LOSS RATIO BY PRODUCT LINE (claims paid / premiums collected)
SELECT
    p.product_type,
    ROUND(SUM(pay.amount), 2) AS premiums_collected,
    ROUND(COALESCE(SUM(CASE WHEN c.status = 'Approved' THEN c.claim_amount END), 0), 2) AS claims_paid,
    ROUND(
        COALESCE(SUM(CASE WHEN c.status = 'Approved' THEN c.claim_amount END), 0)
        / NULLIF(SUM(pay.amount), 0) * 100, 2
    ) AS loss_ratio_pct
FROM policies p
LEFT JOIN payments pay ON pay.policy_id = p.policy_id
LEFT JOIN claims c ON c.policy_id = p.policy_id
GROUP BY p.product_type
ORDER BY loss_ratio_pct DESC;


-- 3) TOP 10 AGENTS BY TOTAL PREMIUM SOLD
SELECT
    a.agent_id,
    a.agent_name,
    a.region,
    COUNT(p.policy_id)              AS nb_policies_sold,
    ROUND(SUM(p.premium_amount), 2) AS total_premium_sold
FROM agents a
JOIN policies p ON p.agent_id = a.agent_id
GROUP BY a.agent_id, a.agent_name, a.region
ORDER BY total_premium_sold DESC
LIMIT 10;


-- 4) AGENT RANKING WITHIN EACH REGION (WINDOW FUNCTION)
SELECT
    region,
    agent_name,
    total_premium_sold,
    RANK() OVER (PARTITION BY region ORDER BY total_premium_sold DESC) AS rank_in_region
FROM (
    SELECT
        a.region,
        a.agent_name,
        ROUND(SUM(p.premium_amount), 2) AS total_premium_sold
    FROM agents a
    JOIN policies p ON p.agent_id = a.agent_id
    GROUP BY a.region, a.agent_name
) AS agent_totals
ORDER BY region, rank_in_region;


-- 5) MONTHLY TREND OF NEW POLICIES AND PREMIUM VOLUME
SELECT
    DATE_FORMAT(start_date, '%Y-%m') AS month,
    COUNT(*)                         AS new_policies,
    ROUND(SUM(premium_amount), 2)    AS premium_volume
FROM policies
GROUP BY month
ORDER BY month;


-- 6) RUNNING TOTAL OF PREMIUMS COLLECTED OVER TIME (WINDOW FUNCTION)
SELECT
    payment_month,
    monthly_amount,
    SUM(monthly_amount) OVER (ORDER BY payment_month) AS running_total
FROM (
    SELECT
        DATE_FORMAT(payment_date, '%Y-%m') AS payment_month,
        ROUND(SUM(amount), 2)              AS monthly_amount
    FROM payments
    GROUP BY payment_month
) AS monthly
ORDER BY payment_month;


-- 7) AVERAGE CLAIM SETTLEMENT TIME BY CLAIM TYPE
SELECT
    claim_type,
    COUNT(*) AS nb_settled_claims,
    ROUND(AVG(DATEDIFF(settlement_date, claim_date)), 1) AS avg_days_to_settle
FROM claims
WHERE settlement_date IS NOT NULL
GROUP BY claim_type
ORDER BY avg_days_to_settle DESC;


-- 8) HIGH-RISK CUSTOMERS: CLAIMS PAID EXCEED PREMIUMS COLLECTED (CTE + SUBQUERY)
WITH customer_premiums AS (
    SELECT p.customer_id, SUM(pay.amount) AS total_paid
    FROM policies p
    JOIN payments pay ON pay.policy_id = p.policy_id
    GROUP BY p.customer_id
),
customer_claims AS (
    SELECT p.customer_id, SUM(c.claim_amount) AS total_claimed
    FROM policies p
    JOIN claims c ON c.policy_id = p.policy_id
    WHERE c.status = 'Approved'
    GROUP BY p.customer_id
)
SELECT
    cu.customer_id,
    CONCAT(cu.first_name, ' ', cu.last_name) AS customer_name,
    ROUND(cp.total_paid, 2)                  AS premiums_paid,
    ROUND(cc.total_claimed, 2)               AS claims_received,
    ROUND(cc.total_claimed - cp.total_paid, 2) AS net_loss
FROM customer_claims cc
JOIN customer_premiums cp ON cp.customer_id = cc.customer_id
JOIN customers cu ON cu.customer_id = cc.customer_id
WHERE cc.total_claimed > cp.total_paid
ORDER BY net_loss DESC;


-- 9) CUSTOMERS WITH MULTIPLE CLAIMS (POTENTIAL FRAUD / RISK FLAG)
SELECT
    cu.customer_id,
    CONCAT(cu.first_name, ' ', cu.last_name) AS customer_name,
    COUNT(c.claim_id)             AS nb_claims,
    ROUND(SUM(c.claim_amount), 2) AS total_claimed
FROM customers cu
JOIN policies p ON p.customer_id = cu.customer_id
JOIN claims c ON c.policy_id = p.policy_id
GROUP BY cu.customer_id, customer_name
HAVING COUNT(c.claim_id) >= 2
ORDER BY nb_claims DESC, total_claimed DESC;


-- 10) POLICIES EXPIRING IN THE NEXT 30 DAYS (RENEWAL PIPELINE)
SELECT
    p.policy_id,
    CONCAT(cu.first_name, ' ', cu.last_name) AS customer_name,
    p.product_type,
    p.end_date,
    p.premium_amount
FROM policies p
JOIN customers cu ON cu.customer_id = p.customer_id
WHERE p.status = 'Active'
  AND p.end_date BETWEEN '2026-09-05' AND DATE_ADD('2026-09-05', INTERVAL 30 DAY)
ORDER BY p.end_date;


-- 11) CLAIM APPROVAL RATE BY PRODUCT LINE
SELECT
    p.product_type,
    COUNT(*) AS total_claims,
    SUM(CASE WHEN c.status = 'Approved' THEN 1 ELSE 0 END) AS approved,
    ROUND(SUM(CASE WHEN c.status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS approval_rate_pct
FROM claims c
JOIN policies p ON p.policy_id = c.policy_id
GROUP BY p.product_type
ORDER BY approval_rate_pct;


-- 12) CUSTOMER LIFETIME VALUE PROXY: TOTAL PREMIUM PAID PER CUSTOMER, RANKED
SELECT
    cu.customer_id,
    CONCAT(cu.first_name, ' ', cu.last_name) AS customer_name,
    cu.city,
    ROUND(SUM(pay.amount), 2) AS lifetime_premium,
    NTILE(4) OVER (ORDER BY SUM(pay.amount) DESC) AS value_quartile
FROM customers cu
JOIN policies p ON p.customer_id = cu.customer_id
JOIN payments pay ON pay.policy_id = p.policy_id
GROUP BY cu.customer_id, customer_name, cu.city
ORDER BY lifetime_premium DESC;
