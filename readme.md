# ⚡ Electric Vehicles Adoption Analysis in Washington State

Electric vehicles (EVs) are transforming the transportation landscape, but access to them is not evenly distributed. In this project, I explored the real-world EV registration data from Washington State to understand how policy, infrastructure, and technology shape EV adoption.

[View it here!](https://github.com/Kenmaaa05/ev-adoption-analysis/blob/main/outputs/ev_dashboard.pdf)

---

## Key Questions

- Who has access to EVs across counties and cities?
- Are EVs concentrated only in urban centers?
- Which manufacturers dominate the EV market?
- How does electric range vary across manufacturers and models?
- Are government policies (CAFV eligibility) driving any real impact?

---

## Highlights of the Power BI Dashboard and EV analysis

### EV Accessibility & Infrastructure

- **Choropleth map** of EV density by county  
- **CAFV eligibility rates** by county, identifying where policy is underutilized  
- **Electric Range of EVs** by region, a potential equity gap  
- **Electric utilities** by region, which areas are underserved?

### Technology & Market Trends

- **Electric range categories by model year**, evolution of EV tech  
- **Top manufacturers and models** over time 
- **CAFV eligibility by brand**, who's making compliant EVs?  
- **Missing range data % by make**, data quality & model-level coverage

---

## Tech Stack

- **Python** (Pandas, NumPy, Matplotlib) for cleaning, transformation, imputation  
- **PostgreSQL** for structured storage and querying  
- **Power BI** for interactive visualizations  

---

## Data Preprocessing

- Normalized column names and formats  
- Parsed and split multi-utility rows  
- Converted vehicle well known text geolocations into standardized lat/long  
- Imputed missing electric range using mode by `(make, model)`  
- Created new features: `range_category`, `price_band`, etc.
- mapped urban and rural counties accordingly.

---

## Repository Structure

```
ev-adoption-analysis/
│
├── data/ 
│ └──Electric_Vehicle_Population_Data.csv
├── notebooks/ 
│ └── ev_analysis.ipynb
├── outputs/ 
│ ├── cleaned_ev.csv
│ ├── ev_dashboard.pbix 
│ └── ev_dashboard.pdf
├── postgres/ 
│ └── pgadmin.py
└── README.md
```


---

## Data Source

This analysis uses public data from:  
[data.wa.gov – Electric Vehicle Population Dataset](https://catalog.data.gov/dataset/electric-vehicle-population-data)

---

This was an end-to-end project where I explored EV adoption and accessibility, infrastructure gaps, and manufacturer trends through data wrangling and visual storytelling.

**Goals:**
- Tell a complete story from raw data to insights
- Practice geospatial and policy-aware data analysis
- Deliver a dashboard suitable for business or public policy use

---
