# Career Materials for athenahealth Application

## Resume Bullet Points (STAR Format)

1. **Simulated** a highly realistic 12-month healthcare SaaS dataset using Python (Faker, Pandas) covering 500 incidents and capacity metrics across 8 microservices, establishing a robust testing environment for ITSM analytics.
2. **Designed** a normalized SQLite relational database schema and engineered 10 complex KPI queries (Window functions, aggregations) to automatically track SLA compliance and platform availability trends.
3. **Analyzed** incident data using Python (Pandas, Seaborn) to identify downtime root causes, revealing that 65% of high-severity outages occurred during mid-day peak hours, leading to optimized deployment schedules.
4. **Developed** a monthly SLA breach tracker correlating downtime minutes with service tiers, highlighting two critical healthcare services requiring immediate architectural review.
5. **Calculated** Mean Time to Resolve (MTTR) by incident severity and category, identifying a 3.2-hour resolution bottleneck in Application-tier issues to recommend standardized escalation runbooks.
6. **Engineered** time-series forecasting models using Facebook Prophet to predict 90-day CPU, memory, and storage demands, identifying 3 high-risk microservices needing proactive scaling.
7. **Built** a 3-page interactive Power BI dashboard featuring 15 custom DAX measures (Rolling 30D Uptime, MTTR, Business Impact Score) to provide operations leadership with real-time platform health visibility.
8. **Created** a proprietary Capacity Risk Scoring algorithm (0-100) weighting resource thresholds and service criticality, enabling SRE teams to prioritize infrastructure scaling 30 days ahead of projected outages.

---

## LinkedIn Post

**Hook:** In Healthcare SaaS, a 99% uptime still means 7 hours of downtime a month. When patient records or claims processing go offline, the impact is more than just lost revenue—it disrupts patient care. 🏥⚙️

**Body:** 
To better understand the challenges of platform reliability at scale, I built an end-to-end Service Performance & Capacity Monitoring Dashboard simulating an 8-service healthcare platform (like those used at athenahealth).

Here’s what I built:
🔹 **Data Engineering:** Simulated 12 months of IT incidents, SLAs, and capacity metrics using Python & SQLite.
🔹 **Predictive Analytics:** Implemented Facebook Prophet ML models to forecast CPU/Memory bottlenecks 90 days out.
🔹 **Risk Scoring:** Built an automated risk engine prioritizing scaling efforts for critical tier services.
🔹 **BI Dashboard:** Developed a 3-page Power BI executive dashboard with 15+ complex DAX measures.
🔹 **ITIL Alignment:** Drafted actionable engineering memos translating data into Incident & Capacity Management strategies.

**Skills Demonstrated:** Python (Pandas, Seaborn), SQL, Machine Learning (Time-Series Forecasting), Power BI, ITIL Frameworks.

**Call to Action:** 
Check out the full code, Jupyter notebooks, and interactive dashboard screenshots on my GitHub! Link in the comments below. 👇

**Hashtags:**
#ServiceManagement #ITSM #DataAnalytics #PowerBI #Python #CapacityPlanning #SRE #HealthcareTech #DataScience #Athenahealth

---

## Interview Preparation Q&A

**Q1: Walk me through your project and what problem it solves.**
*Answer:* I built a Service Performance Dashboard simulating a healthcare SaaS platform managing 8 microservices like EHR and Claims Processing. The core problem it solves is reactive infrastructure management. Instead of waiting for a service to crash or breach an SLA, this project uses historical data to track MTTR and applies machine learning to forecast capacity limits 90 days out, allowing teams to scale proactively.

**Q2: How did you handle capacity forecasting and what models did you use?**
*Answer:* I used the Facebook Prophet library in Python because it excels at handling time-series data with strong seasonal effects, like weekday traffic spikes in healthcare. I trained individual models for CPU, memory, and storage across all 8 services using 12 months of historical data. The models then projected utilization out 90 days, which I used to calculate exactly when a service would cross an 85% critical threshold.

**Q3: How does your dashboard help in post-incident review?**
*Answer:* The Incident Trends page of the Power BI dashboard visually correlates incident categories, severities, and downtime hours. During a PIR, a manager can use the cross-filtering to see that "Application" issues on Tuesday afternoons are causing the highest business impact. It shifts the conversation from anecdotes to data-driven root causes, highlighting exactly where runbooks or architecture need improvement.

**Q4: What ITIL processes did you apply in this project?**
*Answer:* The project heavily aligns with Capacity Management through the predictive Prophet forecasting and Risk Scoring model. It supports Incident and Problem Management by tracking MTTR and categorizing recurring root causes. Finally, it addresses Availability Management by actively tracking rolling 30-day uptime against defined 99.9% SLAs.

**Q5: How would you explain the SLA breach tracker to a non-technical stakeholder?**
*Answer:* I’d explain it as a platform report card. Every service promises to be "open for business" a certain percentage of the time, say 99.9%. The SLA tracker simply looks at the total minutes in a month, subtracts any time the service was down, and highlights in red any service that broke its promise. This helps business leaders quickly see which products are unreliable and need more investment.

**Q6: What were the most significant findings from your analysis?**
*Answer:* Two major findings stood out. First, while overall platform uptime looked healthy at 99.1%, the critical EHR service was quietly breaching its SLA target every quarter due to database issues. Second, the predictive models flagged the Authentication Service for an impending CPU bottleneck in less than 30 days, despite looking stable on a 30-day lookback, proving the value of forecasting.

**Q7: If this were a real production environment, what would you do differently?**
*Answer:* In a real environment, I wouldn't rely on batched CSV exports. I would connect Power BI directly to a live data warehouse like Snowflake or AWS Redshift using DirectQuery. I’d also integrate the capacity risk alerts directly into a system like Jira or PagerDuty to automatically notify the SRE team rather than relying solely on a static report.

**Q8: How does this project relate to the day-to-day work of a Service Performance Analyst?**
*Answer:* It mirrors the exact workflow of the role. I extracted messy operational data, cleaned and modeled it, applied analytical logic to find the signal in the noise, and built executive dashboards. More importantly, I translated those technical findings into a professional stakeholder memo with actionable recommendations, which is the core value a Service Performance Analyst brings to engineering teams.
