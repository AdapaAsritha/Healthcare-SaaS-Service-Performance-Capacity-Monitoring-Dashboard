-- Query 1: Overall uptime percentage per service for the last 12 months
SELECT 
    s.service_name,
    AVG(a.uptime_pct) AS overall_uptime_pct
FROM availability a
JOIN services s ON a.service_id = s.service_id
GROUP BY s.service_name
ORDER BY overall_uptime_pct ASC;

-- Query 2: Monthly SLA breach count by service (flag months where sla_met = False)
SELECT 
    s.service_name,
    COUNT(t.sla_id) AS total_breaches
FROM sla_tracking t
JOIN services s ON t.service_id = s.service_id
WHERE t.sla_met = 0
GROUP BY s.service_name
ORDER BY total_breaches DESC;

-- Query 3: Top 5 services by total downtime minutes in the last 12 months
SELECT 
    s.service_name,
    SUM(i.downtime_minutes) AS total_downtime_minutes
FROM incidents i
JOIN services s ON i.service_id = s.service_id
GROUP BY s.service_name
ORDER BY total_downtime_minutes DESC
LIMIT 5;

-- Query 4: Incident count by severity and category (pivot-style summary)
SELECT 
    category,
    SUM(CASE WHEN severity = 'P1' THEN 1 ELSE 0 END) AS p1_count,
    SUM(CASE WHEN severity = 'P2' THEN 1 ELSE 0 END) AS p2_count,
    SUM(CASE WHEN severity = 'P3' THEN 1 ELSE 0 END) AS p3_count,
    SUM(CASE WHEN severity = 'P4' THEN 1 ELSE 0 END) AS p4_count,
    COUNT(incident_id) AS total_incidents
FROM incidents
GROUP BY category
ORDER BY total_incidents DESC;

-- Query 5: Mean Time to Resolve (MTTR) in hours per service and severity level
SELECT 
    s.service_name,
    i.severity,
    AVG(i.downtime_minutes)/60.0 AS mttr_hours
FROM incidents i
JOIN services s ON i.service_id = s.service_id
GROUP BY s.service_name, i.severity
ORDER BY s.service_name, i.severity;

-- Query 6: Month-over-month change in P1 incident count per service
WITH monthly_p1 AS (
    SELECT 
        s.service_name,
        strftime('%Y-%m', i.incident_date) AS month_year,
        COUNT(i.incident_id) AS p1_count
    FROM incidents i
    JOIN services s ON i.service_id = s.service_id
    WHERE i.severity = 'P1'
    GROUP BY s.service_name, strftime('%Y-%m', i.incident_date)
)
SELECT 
    service_name,
    month_year,
    p1_count,
    LAG(p1_count) OVER (PARTITION BY service_name ORDER BY month_year) AS prev_month_p1_count,
    p1_count - LAG(p1_count) OVER (PARTITION BY service_name ORDER BY month_year) AS mom_change
FROM monthly_p1
ORDER BY service_name, month_year;

-- Query 7: Services currently at risk — where average CPU or memory utilization in the last 30 days exceeds 75%
SELECT 
    s.service_name,
    AVG(c.cpu_utilization_pct) AS avg_cpu_last_30d,
    AVG(c.memory_utilization_pct) AS avg_memory_last_30d
FROM capacity c
JOIN services s ON c.service_id = s.service_id
WHERE date(c.date) >= date((SELECT MAX(date) FROM capacity), '-30 days')
GROUP BY s.service_name
HAVING avg_cpu_last_30d > 75 OR avg_memory_last_30d > 75;

-- Query 8: SLA breach rate (%) per service = (months breached / total months) * 100
SELECT 
    s.service_name,
    SUM(CASE WHEN t.sla_met = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(t.sla_id) AS breach_rate_pct
FROM sla_tracking t
JOIN services s ON t.service_id = s.service_id
GROUP BY s.service_name
ORDER BY breach_rate_pct DESC;

-- Query 9: Peak incident day of week analysis — which day has most incidents
-- strftime('%w', incident_date): 0=Sunday, 1=Monday, ..., 6=Saturday
SELECT 
    CASE CAST(strftime('%w', incident_date) AS INTEGER)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_of_week,
    COUNT(incident_id) AS total_incidents
FROM incidents
GROUP BY day_of_week
ORDER BY total_incidents DESC;

-- Query 10: Availability trend — rolling 30-day average uptime per service
-- Uses a self join or correlated subquery approach, but simpler using window function if sqlite version supports it
-- However, just extracting daily uptime and a 30-day moving avg is easier in code, but here is a SQL approach:
SELECT 
    s.service_name,
    a.date,
    AVG(a.uptime_pct) OVER (
        PARTITION BY a.service_id 
        ORDER BY a.date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS rolling_30d_uptime_pct
FROM availability a
JOIN services s ON a.service_id = s.service_id
ORDER BY s.service_name, a.date;
