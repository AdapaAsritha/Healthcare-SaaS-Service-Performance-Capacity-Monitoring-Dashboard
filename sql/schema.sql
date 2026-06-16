CREATE TABLE IF NOT EXISTS services (
    service_id TEXT PRIMARY KEY,
    service_name TEXT NOT NULL,
    service_tier TEXT NOT NULL,
    team_owner TEXT,
    sla_uptime_target_pct REAL
);

CREATE TABLE IF NOT EXISTS incidents (
    incident_id TEXT PRIMARY KEY,
    service_id TEXT,
    incident_date TEXT,
    severity TEXT,
    category TEXT,
    start_time TEXT,
    end_time TEXT,
    downtime_minutes INTEGER,
    resolution_notes TEXT,
    status TEXT,
    FOREIGN KEY (service_id) REFERENCES services(service_id)
);

CREATE TABLE IF NOT EXISTS availability (
    availability_id INTEGER PRIMARY KEY,
    service_id TEXT,
    date TEXT,
    uptime_pct REAL,
    total_minutes INTEGER,
    downtime_minutes INTEGER,
    sla_breached BOOLEAN,
    FOREIGN KEY (service_id) REFERENCES services(service_id)
);

CREATE TABLE IF NOT EXISTS capacity (
    capacity_id INTEGER PRIMARY KEY,
    service_id TEXT,
    date TEXT,
    cpu_utilization_pct REAL,
    memory_utilization_pct REAL,
    storage_utilization_pct REAL,
    active_connections INTEGER,
    request_volume INTEGER,
    FOREIGN KEY (service_id) REFERENCES services(service_id)
);

CREATE TABLE IF NOT EXISTS sla_tracking (
    sla_id INTEGER PRIMARY KEY,
    service_id TEXT,
    month_year TEXT,
    target_uptime_pct REAL,
    actual_uptime_pct REAL,
    sla_met BOOLEAN,
    total_incidents INTEGER,
    p1_count INTEGER,
    p2_count INTEGER,
    mttr_hours REAL,
    breach_minutes INTEGER,
    FOREIGN KEY (service_id) REFERENCES services(service_id)
);

-- Indexes for frequently queried columns
CREATE INDEX IF NOT EXISTS idx_incidents_service_id ON incidents(service_id);
CREATE INDEX IF NOT EXISTS idx_incidents_incident_date ON incidents(incident_date);
CREATE INDEX IF NOT EXISTS idx_incidents_severity ON incidents(severity);
CREATE INDEX IF NOT EXISTS idx_availability_service_id ON availability(service_id);
CREATE INDEX IF NOT EXISTS idx_availability_date ON availability(date);
CREATE INDEX IF NOT EXISTS idx_capacity_service_id ON capacity(service_id);
CREATE INDEX IF NOT EXISTS idx_capacity_date ON capacity(date);
CREATE INDEX IF NOT EXISTS idx_sla_tracking_service_id ON sla_tracking(service_id);
CREATE INDEX IF NOT EXISTS idx_sla_tracking_month_year ON sla_tracking(month_year);
