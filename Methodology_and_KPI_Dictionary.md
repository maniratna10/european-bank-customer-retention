# Methodology and KPI Dictionary

## Analysis population
The supplied file contains 10,000 records and 14 columns. The analysis uses customer-level rows and the `Exited` field as the churn outcome (1 = exited, 0 = retained). All fields in the supplied extract are populated. The supplied data contains a `Year` field (2025), but no repeated customer history is provided.

## Derived engagement profiles
- Active / broader relationship: active member with at least two products.
- Active / single product: active member with one product.
- Inactive / higher balance: inactive member with balance at or above the filtered-data median.
- Inactive / lower balance: remaining inactive member.
These are operational groupings for exploration, not official bank customer classifications.

## KPI dictionary
| KPI | Operational definition | Interpretation |
|---|---|---|
| Engagement retention comparison | Churn rate among active customers versus inactive customers | A lower rate indicates stronger observed retention |
| Product depth | Number of products held; compare churn by count | Non-linear patterns are possible; include segment size |
| High-balance disengagement | Inactive customers at/above a configurable balance threshold | Identifies a segment for review; not automatically a premium tier |
| Credit card stickiness comparison | Churn rate among cardholders versus non-cardholders | Descriptive association only |
| Relationship Strength Index | 40 × activity + 40 × min(products, 2)/2 + 20 × card ownership | Simple transparent prioritisation score, not a probability |

## Validation performed
- Required-column presence
- Missing-value count
- Duplicate customer ID count
- Binary-domain checks for `HasCrCard`, `IsActiveMember`, and `Exited`
- Range and category review during analysis

## Limitations
1. `IsActiveMember` is the only direct engagement indicator. No login, transaction, channel or contact frequency is supplied.
2. No product-level names or usage frequency are available. Product count is a proxy for breadth, not actual utilization.
3. The extract does not specify currency.
4. No event dates or longitudinal snapshots are provided; retention trends over time cannot be established.
5. Observed differences do not establish causation. Confounding variables may explain part of the pattern.
6. Very small groups (notably three or four products) can produce unstable rates.
