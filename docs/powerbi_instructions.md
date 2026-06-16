# Power BI Dashboard Setup Guide

This guide provides step-by-step instructions to build the Healthcare SaaS Service Performance & Capacity Monitoring Dashboard.

## TASK 1 — Power BI Setup & Data Loading

1. **Open Power BI Desktop**: If you don't have it installed, download it for free from the [Microsoft Store](https://aka.ms/pbidesktopstore) or [Power BI website](https://powerbi.microsoft.com/desktop/).
2. **Load Data**:
   - Go to `Home > Get Data > Text/CSV`.
   - Load the following 6 files from the `data/processed/` folder one by one:
     - `powerbi_incidents.csv`
     - `powerbi_availability.csv`
     - `powerbi_capacity_current.csv`
     - `powerbi_capacity_forecast.csv`
     - `powerbi_risk_summary.csv`
     - `powerbi_sla_summary.csv`
3. **Power Query Editor Transformations**:
   - Click `Transform Data` to open the Power Query Editor.
   - **Data Types**: Ensure columns like `uptime_pct`, `downtime_minutes`, `cpu_utilization_pct` are set to Decimal Number or Whole Number.
   - **Parse Dates**: Ensure `date`, `incident_date`, and `start_time` columns are set to Date or Date/Time format.
   - **Calculated Column in `powerbi_availability`**:
     - Go to `Add Column > Custom Column`.
     - Name: `Month_Year`
     - Formula: `= Date.ToText([date], "MMM yyyy")` (Or use DAX later).
   - **Calculated Column in `powerbi_incidents`**:
     - Go to `Add Column > Custom Column`.
     - Name: `Downtime_Hours`
     - Formula: `= [downtime_minutes] / 60`
   - **Clean Up**: Remove any rows with nulls in critical ID or date columns.
   - Click `Close & Apply`.
4. **Data Modeling (Relationships)**:
   - Go to the Model View (left panel, third icon).
   - Drag `service_name` from `powerbi_availability` to `service_name` in `powerbi_incidents` to create a Many-to-Many relationship (Cross filter direction: Both).
   - Create a relationship between `powerbi_sla_summary[service_name]` and `powerbi_risk_summary[service_name]`.
5. **Create Date Table (DAX)**:
   - Go to the Data View (left panel, second icon).
   - Click `Table tools > New table`.
   - Enter the DAX formula:
     ```dax
     DateTable = CALENDAR(DATE(2024,1,1), DATE(2025,12,31))
     ```
   - Add calculated columns to `DateTable`:
     ```dax
     Year = YEAR(DateTable[Date])
     MonthNum = MONTH(DateTable[Date])
     Month = FORMAT(DateTable[Date], "MMM")
     MonthYear = FORMAT(DateTable[Date], "MMM YYYY")
     Quarter = "Q" & FORMAT(DateTable[Date], "Q")
     WeekDay = FORMAT(DateTable[Date], "dddd")
     ```

## TASK 2 — DAX Measures

Create a dedicated Measures table (Home > Enter Data, name it `_Measures`). Right-click `_Measures` and select `New Measure` to add each of the following:

1. **Total Incidents**: Counts the total number of incidents recorded.
   `Total Incidents = COUNTROWS(powerbi_incidents)`
2. **P1 Incidents**: Filters incidents to only show Priority 1 (critical) issues.
   `P1 Incidents = CALCULATE([Total Incidents], powerbi_incidents[severity] = "P1")`
3. **P2 Incidents**: Filters incidents to show Priority 2 issues.
   `P2 Incidents = CALCULATE([Total Incidents], powerbi_incidents[severity] = "P2")`
4. **Avg MTTR Hours**: Calculates the Mean Time to Resolve across incidents.
   `Avg MTTR Hours = AVERAGE(powerbi_sla_summary[mttr_hours])`
5. **Overall Uptime %**: Computes the average availability percentage across all services.
   `Overall Uptime % = AVERAGE(powerbi_availability[uptime_pct])`
6. **SLA Breach Count**: Counts how many times a service failed to meet its monthly SLA target.
   `SLA Breach Count = COUNTROWS(FILTER(powerbi_sla_summary, powerbi_sla_summary[sla_met] = FALSE()))`
7. **SLA Compliance Rate %**: Percentage of months where services met their SLA targets.
   `SLA Compliance Rate % = DIVIDE(COUNTROWS(FILTER(powerbi_sla_summary, powerbi_sla_summary[sla_met] = TRUE())), COUNTROWS(powerbi_sla_summary), 0) * 100`
8. **Total Downtime Hours**: Sums up the total outage time in hours.
   `Total Downtime Hours = SUM(powerbi_incidents[Downtime_Hours])`
9. **Rolling 30D Uptime %**: Average uptime over the last 30 days dynamically based on the current date context.
   `Rolling 30D Uptime % = CALCULATE(AVERAGE(powerbi_availability[uptime_pct]), DATESINPERIOD(DateTable[Date], LASTDATE(DateTable[Date]), -30, DAY))`
10. **Capacity at Risk Services**: Counts services flagged as High or Critical risk in the capacity forecasting model.
    `Capacity at Risk Services = COUNTROWS(FILTER(powerbi_risk_summary, powerbi_risk_summary[risk_level] IN {"CRITICAL RISK", "HIGH RISK"}))`
11. **Avg CPU Utilization %**: Average current CPU usage.
    `Avg CPU Utilization % = AVERAGE(powerbi_capacity_current[cpu_utilization_pct])`
12. **Avg Memory Utilization %**: Average current Memory usage.
    `Avg Memory Utilization % = AVERAGE(powerbi_capacity_current[memory_utilization_pct])`
13. **Business Impact Score Total**: Sums the weighted impact score of incidents.
    `Business Impact Score Total = SUM(powerbi_incidents[business_impact_score])`
14. **MOM Incident Change %**: Calculates month-over-month growth or reduction in incident volume.
    ```dax
    MOM Incident Change % = 
    VAR CurrentMonth = [Total Incidents] 
    VAR PrevMonth = CALCULATE([Total Incidents], DATEADD(DateTable[Date], -1, MONTH)) 
    RETURN DIVIDE(CurrentMonth - PrevMonth, PrevMonth, 0) * 100
    ```
15. **Services Breaching SLA**: Creates a comma-separated list of services that missed SLA targets.
    `Services Breaching SLA = CONCATENATEX(FILTER(powerbi_sla_summary, powerbi_sla_summary[sla_met] = FALSE()), powerbi_sla_summary[service_name], ", ")`

## TASK 3 — Page 1: Executive Summary Dashboard

Create a new page named `Executive Summary`.
*Theme Settings*: Go to View > Themes > Select "Executive". Set background to White, Font to Segoe UI. Add a text box at the top: **"Healthcare SaaS — Service Performance Dashboard"** (14pt, bold).

**Top Row (4 KPI Cards)**:
- **Card 1**: `Overall Uptime %`. Format: Percentage, 2 decimals. *Conditional Formatting* (Callout Value): Green if >99.5%, Yellow if 99-99.5%, Red if <99%.
- **Card 2**: `SLA Compliance Rate %`. Format: Percentage. *Conditional Formatting*: Same as Card 1.
- **Card 3**: `Total P1 Incidents`. *Conditional Formatting*: Red if >5, Yellow if 3-5, Green if <3.
- **Card 4**: `Avg MTTR (Hours)`. *Conditional Formatting*: Red if >4, Yellow if 2-4, Green if <2.

**Middle Row (2 Charts)**:
- **Line Chart**: "Monthly Uptime % by Service". X-Axis: `powerbi_availability[month_year]`, Y-Axis: `uptime_pct` (Average), Legend: `service_name`. Add a Constant Line (Analytics pane) at 99.5 labeled "SLA Target".
- **Clustered Bar Chart**: "Incidents by Severity". X-Axis: `severity`, Y-Axis: `Total Incidents`. Data Colors: P1=Red, P2=Orange, P3=Yellow, P4=Green.

**Bottom Row (2 Visuals)**:
- **Matrix**: Rows: `service_name`. Values: `Overall Uptime %`, `SLA Breach Count`, `Avg MTTR Hours`, `P1 Incidents`. Apply background conditional formatting to the Uptime column.
- **Donut Chart**: "Incidents by Category". Legend: `category`, Values: `Total Incidents`. Enable detail labels showing Category and % of Total.

**Right Panel (Slicers)**:
- `service_name` (Dropdown, Multi-select)
- `month_year` (Between date range)
- `severity` (Checkbox)
- `service_tier` (Dropdown)
*Ensure slicers are synced across all pages (View > Sync slicers).*

## TASK 4 — Page 2: Incident Trends Analysis

Create a new page named `Incident Trends`.

**Top Row (3 KPI Cards)**:
- `Total Incidents`
- `Total Downtime Hours`
- `Business Impact Score Total`

**Middle Row (2 Charts)**:
- **Area Chart**: "Incident Trend Over Time". X-Axis: `powerbi_incidents[incident_date]` (Month level), Y-Axis: `Total Incidents`, Legend: `severity`.
- **Stacked Bar Chart**: "Downtime Hours by Service and Severity". Y-Axis: `service_name`, X-Axis: `Total Downtime Hours`, Legend: `severity`.

**Bottom Row (2 Charts)**:
- **Matrix (Heatmap)**: "Incidents by Day of Week". Rows: `DateTable[WeekDay]`, Columns: `DateTable[Month]`, Values: `Total Incidents`. Apply conditional formatting (Background color) to the values: White (Lowest) to Dark Red (Highest).
- **Clustered Bar Chart**: "Top Services by Business Impact Score". Y-Axis: `service_name`, X-Axis: `Business Impact Score Total`. Sort Descending. Color bars by `service_tier`.
- **Text Box**: Add a note: *"Insight: Services with highest business impact require priority P1 response protocols."*

## TASK 5 — Page 3: Capacity Forecast & Risk

Create a new page named `Capacity & Risk`.

**Top Row (4 KPI Cards)**:
- `Avg CPU Utilization %`
- `Avg Memory Utilization %`
- `Capacity at Risk Services`
- `SLA Breach Count`

**Middle Row (2 Charts)**:
- **Line Chart**: "CPU Utilization Forecast (90 days)". Filter visual to `metric = "cpu"`. X-Axis: `date`, Y-Axis: `forecasted_value`. Add `lower_bound` and `upper_bound` as secondary lines to simulate a confidence interval. Change the line style for future dates to dotted.
- **Gauge Chart**: "Current Avg CPU Utilization". Value: `Avg CPU Utilization %`. Min: 0, Max: 100, Target: 75. Create an identical Gauge for Memory next to it.

**Bottom Row (2 Charts)**:
- **Table**: "Capacity Risk Register". Columns: `service_name`, `risk_score`, `risk_level`, `cpu_warning_days`, `memory_warning_days`, `recommended_action`. Conditional formatting on `risk_level`: CRITICAL=Red, HIGH=Orange, MEDIUM=Yellow, LOW=Green.
- **Clustered Column Chart**: "90-Day Forecasted Utilization by Service". X-Axis: `service_name`, Y-Axis: `forecasted_value`. Legend: `metric`. Filter to only show the last forecasted date (90 days out). Add a constant line at 85% labeled "Critical Threshold".

## TASK 6 — Polish & Export

1. **Navigation**: Go to Insert > Buttons > Page Navigator. Place it at the top of each page to easily click between Executive Summary, Incident Trends, and Capacity & Risk.
2. **Logo**: Insert > Shapes > Rectangle. Add text "Healthcare SaaS Monitor" and place in the top left corner as a logo.
3. **Tooltips**: For all bar and line charts, drag `service_name` and relevant value columns into the Tooltips well.
4. **Export**: 
   - File > Export > Export to PDF. 
   - Take PNG screenshots of the PDF pages and save them in the `powerbi-screenshots/` directory as `page1.png`, `page2.png`, and `page3.png`.
5. **Save**: Save your Power BI project as `healthcare_saas_dashboard.pbix` in the root folder.
