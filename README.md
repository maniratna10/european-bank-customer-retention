# Customer Engagement & Product Utilization Analytics

A Streamlit dashboard and descriptive research report built around the supplied `European_Bank.csv` dataset.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create an environment (recommended): `python -m venv .venv`
4. Activate it, then install dependencies: `pip install -r requirements.txt`
5. Start the dashboard: `streamlit run app.py`

The app loads `data/European_Bank.csv` by default. A different CSV can be uploaded from the sidebar.

## Dashboard modules
- Engagement versus churn
- Product-count and credit-card comparisons
- Inactive, higher-balance customer detector
- Transparent 0–100 Relationship Strength Index
- Filters for geography, activity, product count, balance and salary
- Download of the filtered at-risk customer segment

## KPI definitions
- Engagement retention ratio: active customer churn rate compared with inactive customer churn rate. Lower churn indicates stronger observed retention.
- Product depth index: descriptive relationship-depth score based on product count; the dashboard caps the contribution at two products so unusual higher-count groups do not dominate the score.
- High-balance disengagement rate: share of customers who are inactive and meet the selected balance threshold; churn within that group is also displayed.
- Credit card stickiness: compare observed churn for cardholders and non-cardholders. This is association, not causation.
- Relationship Strength Index: activity (40 points) + product depth (up to 40 points) + card ownership (20 points).

## Important interpretation notes
This dataset does not include transaction frequency, app logins, product names, customer contact history, or a time series of account activity. `IsActiveMember` is therefore used as the available engagement proxy. Currency is not specified in the supplied data, so balance and salary values are shown without assuming a currency. `Year` is present in the data but is not used to infer a trend.

The dashboard is descriptive and does not claim causal effects or produce a validated churn prediction model. Review segment sizes alongside churn rates, especially for customers with three or four products.

## Project contents
- `app.py`: Streamlit dashboard
- `data/European_Bank.csv`: supplied source dataset
- `reports/Research_Report.docx`: project research report
- `reports/Executive_Summary.md`: concise stakeholder summary
- `reports/Methodology_and_KPI_Dictionary.md`: definitions and limitations


## Presentation style
The dashboard uses a restrained editorial layout, muted colours, plain-language section titles and short analyst notes. Update the project title, report author details and any interpretation notes to reflect your own review before submission.


## Dashboard appearance
The dashboard is styled in a dark charcoal and muted green theme. Restart Streamlit after replacing the previous project folder to see the changes.
