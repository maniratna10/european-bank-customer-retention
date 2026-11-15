# Executive Summary
## Customer Engagement & Product Utilization Analytics for Retention Strategy

### Purpose
This analysis examines whether the engagement indicator and breadth of banking relationships are associated with customer exits. It also identifies customers who have a relatively high balance but are marked inactive, a group that may warrant proactive relationship review.

### Dataset
The supplied European Bank extract contains 10,000 customer records. The overall observed exit rate is **20.37%**. The file contains customer profile, balance, salary, product-count, credit-card and active-member fields. It does not contain transaction frequency, digital-channel activity or product-level usage details.

### Main findings
- Customers marked active have an observed exit rate of **14.27%**, compared with **26.85%** for inactive customers. This is a 12.58 percentage-point difference.
- Customers with two products have an observed exit rate of **7.58%**, compared with **27.71%** among one-product customers.
- The three-product segment has an observed exit rate of **82.71%** (266 customers), while all 60 customers in the four-product segment exited. These unusual high rates should not be interpreted as evidence that adding products causes churn; the groups are small and may represent a distinct customer cohort or data-generation pattern.
- Credit-card ownership is only weakly differentiated in this extract: observed exit is **20.18%** for cardholders and **20.81%** for non-cardholders.
- There are **2,356** inactive customers with a balance of at least 100,000 (currency not specified). Their observed exit rate is **32.77%**.

### Recommended actions
1. Prioritise a service-led outreach review for inactive, higher-balance customers. Confirm whether inactivity reflects low product usage, a dormant account, a service issue or an incomplete activity flag.
2. Review the one-product segment for relevant, needs-based product education and service engagement. Avoid indiscriminate cross-selling.
3. Investigate the three- and four-product groups separately before making product-bundling decisions. Validate product definitions, acquisition channels, fees and cohort composition.
4. Use channel activity and transaction recency in a future data collection phase to build a more complete engagement measure.
5. Track retention outcomes after any pilot intervention, using a holdout group where practical.

### Stakeholder note
The dashboard is a descriptive decision-support tool, not a churn prediction model. Results describe the supplied dataset and should be validated against operational bank records before policy or customer-level decisions are made.
