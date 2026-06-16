import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Create output directory
OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define Services
services_data = [
    {"service_id": "SRV-001", "service_name": "Patient Portal", "service_tier": "standard", "team_owner": "Patient Experience", "sla_uptime_target_pct": 99.5},
    {"service_id": "SRV-002", "service_name": "Claims Processing", "service_tier": "critical", "team_owner": "Revenue Cycle", "sla_uptime_target_pct": 99.9},
    {"service_id": "SRV-003", "service_name": "EHR", "service_tier": "critical", "team_owner": "Clinical Systems", "sla_uptime_target_pct": 99.9},
    {"service_id": "SRV-004", "service_name": "Appointment Scheduling", "service_tier": "standard", "team_owner": "Patient Experience", "sla_uptime_target_pct": 99.5},
    {"service_id": "SRV-005", "service_name": "Billing Engine", "service_tier": "critical", "team_owner": "Revenue Cycle", "sla_uptime_target_pct": 99.9},
    {"service_id": "SRV-006", "service_name": "Lab Results API", "service_tier": "standard", "team_owner": "Integration", "sla_uptime_target_pct": 99.5},
    {"service_id": "SRV-007", "service_name": "Notification Service", "service_tier": "low", "team_owner": "Platform", "sla_uptime_target_pct": 99.0},
    {"service_id": "SRV-008", "service_name": "Authentication Service", "service_tier": "critical", "team_owner": "Security", "sla_uptime_target_pct": 99.9},
]
df_services = pd.DataFrame(services_data)
df_services.to_csv(os.path.join(OUTPUT_DIR, "services.csv"), index=False)

# Setup dates for 12 months (365 days back from today)
end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
start_date = end_date - timedelta(days=365)
date_range = pd.date_range(start=start_date, end=end_date - timedelta(days=1))

# Generate Incidents
incidents = []
for i in range(500):
    incident_id = f"INC-{1000 + i}"
    # Pick a random date
    # Weekdays have higher chance
    is_weekday = random.random() < 0.8
    if is_weekday:
        date = fake.date_time_between(start_date=start_date, end_date=end_date)
        while date.weekday() > 4:
            date = fake.date_time_between(start_date=start_date, end_date=end_date)
    else:
        date = fake.date_time_between(start_date=start_date, end_date=end_date)
        while date.weekday() <= 4:
            date = fake.date_time_between(start_date=start_date, end_date=end_date)
            
    # Business hours have more incidents
    hour = int(np.random.normal(loc=14, scale=4)) # peak around 2 PM
    hour = max(0, min(23, hour))
    date = date.replace(hour=hour, minute=random.randint(0, 59))
    
    # Severity distribution
    sev_choice = random.choices(["P1", "P2", "P3", "P4"], weights=[5, 20, 50, 25])[0]
    
    # Critical services have higher chance of P1
    if sev_choice == "P1":
        srv = random.choices(services_data, weights=[1 if s["service_tier"] != "critical" else 4 for s in services_data])[0]
    else:
        srv = random.choice(services_data)
        
    category = random.choices(["Network", "Application", "Infrastructure", "Database"], weights=[15, 50, 15, 20])[0]
    
    # Downtime duration based on severity
    if sev_choice == "P1":
        downtime = random.randint(60, 480) # 1 to 8 hours
    elif sev_choice == "P2":
        downtime = random.randint(30, 240)
    elif sev_choice == "P3":
        downtime = random.randint(10, 120)
    else:
        downtime = random.randint(5, 60)
        
    start_time = date
    end_time = start_time + timedelta(minutes=downtime)
    
    incidents.append({
        "incident_id": incident_id,
        "service_id": srv["service_id"],
        "incident_date": start_time.strftime("%Y-%m-%d"),
        "severity": sev_choice,
        "category": category,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "downtime_minutes": downtime,
        "resolution_notes": fake.sentence(),
        "status": "Resolved"
    })

df_incidents = pd.DataFrame(incidents)
# Ensure sorted by date
df_incidents = df_incidents.sort_values("start_time").reset_index(drop=True)
df_incidents.to_csv(os.path.join(OUTPUT_DIR, "incidents.csv"), index=False)

# Generate Availability
availability = []
avail_id = 1
for d in date_range:
    date_str = d.strftime("%Y-%m-%d")
    daily_incidents = df_incidents[df_incidents["incident_date"] == date_str]
    
    for srv in services_data:
        srv_id = srv["service_id"]
        # calculate downtime for this day and service
        srv_incidents = daily_incidents[daily_incidents["service_id"] == srv_id]
        downtime_mins = srv_incidents["downtime_minutes"].sum()
        total_mins = 24 * 60
        uptime_pct = ((total_mins - downtime_mins) / total_mins) * 100
        uptime_pct = round(max(0, min(100, uptime_pct)), 3)
        
        sla_breached = uptime_pct < srv["sla_uptime_target_pct"]
        
        availability.append({
            "availability_id": avail_id,
            "service_id": srv_id,
            "date": date_str,
            "uptime_pct": uptime_pct,
            "total_minutes": total_mins,
            "downtime_minutes": downtime_mins,
            "sla_breached": sla_breached
        })
        avail_id += 1

df_availability = pd.DataFrame(availability)
df_availability.to_csv(os.path.join(OUTPUT_DIR, "availability.csv"), index=False)

# Generate Capacity
capacity = []
cap_id = 1
months_passed = 0
for d in date_range:
    date_str = d.strftime("%Y-%m-%d")
    if d.day == 1:
        months_passed += 1
        
    for srv in services_data:
        srv_id = srv["service_id"]
        is_critical = srv["service_tier"] == "critical"
        
        # Base utilization
        base_cpu = 40 if is_critical else 20
        base_mem = 45 if is_critical else 25
        base_storage = 30
        
        # Add 2-4% growth per month
        growth_factor = 1 + (months_passed * random.uniform(0.02, 0.04))
        
        # Add noise
        cpu = base_cpu * growth_factor + random.uniform(-5, 15)
        mem = base_mem * growth_factor + random.uniform(-5, 10)
        storage = base_storage * growth_factor + random.uniform(-2, 5)
        
        # Business hour simulation for active connections (more on weekdays)
        conn_base = 5000 if is_critical else 1000
        if d.weekday() < 5:
            conn = int(conn_base * growth_factor * random.uniform(0.8, 1.2))
            req_vol = int(conn * random.uniform(10, 20))
        else:
            conn = int(conn_base * growth_factor * random.uniform(0.3, 0.6))
            req_vol = int(conn * random.uniform(5, 10))
            
        capacity.append({
            "capacity_id": cap_id,
            "service_id": srv_id,
            "date": date_str,
            "cpu_utilization_pct": round(min(100, max(0, cpu)), 2),
            "memory_utilization_pct": round(min(100, max(0, mem)), 2),
            "storage_utilization_pct": round(min(100, max(0, storage)), 2),
            "active_connections": conn,
            "request_volume": req_vol
        })
        cap_id += 1

df_capacity = pd.DataFrame(capacity)
df_capacity.to_csv(os.path.join(OUTPUT_DIR, "capacity.csv"), index=False)

# Generate SLA Tracking
sla_tracking = []
sla_id = 1
# Group availability by month
df_availability['month_year'] = pd.to_datetime(df_availability['date']).dt.strftime('%Y-%m')
df_incidents['month_year'] = pd.to_datetime(df_incidents['incident_date']).dt.strftime('%Y-%m')

months = df_availability['month_year'].unique()

for m in months:
    avail_month = df_availability[df_availability['month_year'] == m]
    inc_month = df_incidents[df_incidents['month_year'] == m]
    
    for srv in services_data:
        srv_id = srv["service_id"]
        
        # Availability metrics
        srv_avail = avail_month[avail_month['service_id'] == srv_id]
        total_mins = srv_avail['total_minutes'].sum()
        downtime_mins = srv_avail['downtime_minutes'].sum()
        actual_uptime = ((total_mins - downtime_mins) / total_mins) * 100
        actual_uptime = round(actual_uptime, 3)
        target_uptime = srv["sla_uptime_target_pct"]
        sla_met = actual_uptime >= target_uptime
        
        # Incident metrics
        srv_inc = inc_month[inc_month['service_id'] == srv_id]
        total_inc = len(srv_inc)
        p1_cnt = len(srv_inc[srv_inc['severity'] == 'P1'])
        p2_cnt = len(srv_inc[srv_inc['severity'] == 'P2'])
        mttr = srv_inc['downtime_minutes'].mean() / 60 if total_inc > 0 else 0
        
        sla_tracking.append({
            "sla_id": sla_id,
            "service_id": srv_id,
            "month_year": m,
            "target_uptime_pct": target_uptime,
            "actual_uptime_pct": actual_uptime,
            "sla_met": sla_met,
            "total_incidents": total_inc,
            "p1_count": p1_cnt,
            "p2_count": p2_cnt,
            "mttr_hours": round(mttr, 2),
            "breach_minutes": int(downtime_mins) if not sla_met else 0
        })
        sla_id += 1

df_sla_tracking = pd.DataFrame(sla_tracking)
df_sla_tracking.to_csv(os.path.join(OUTPUT_DIR, "sla_tracking.csv"), index=False)

# Print Summary
print("Data Generation Complete!")
print("-" * 50)
for name, df in [("services.csv", df_services), 
                 ("incidents.csv", df_incidents), 
                 ("availability.csv", df_availability), 
                 ("capacity.csv", df_capacity), 
                 ("sla_tracking.csv", df_sla_tracking)]:
    print(f"\n{name} - {len(df)} rows")
    print(df.head(3))
