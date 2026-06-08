# Codelab 2 — AlloyDB-BigQuery Zero ETL Federation 🔗

## Overview
Established a Zero-ETL federation between AlloyDB (PostgreSQL) and BigQuery using the `bigquery_fdw` foreign data wrapper extension — enabling real-time analytical queries on BigQuery data directly from AlloyDB without data movement.

## Architecture
```
BigQuery (froyo_data) ◄──── bigquery_fdw ────► AlloyDB PostgreSQL
        │                                              │
   Analytical Data                            Transactional Data
   (Product specs,                           (Live orders,
    Ingredients,                              Customer data)
    Allergens)
                    └──────────────────────┘
                         HTAP Queries
```

## Key Components

### AlloyDB Infrastructure
| Component | Value |
|-----------|-------|
| Cluster | `froyo-cluster` |
| Instance | `froyo-instance` |
| Region | `us-central1` |
| Version | PostgreSQL 15 |
| VPC | `alloydb-vpc` |
| Private IP | `10.211.0.2` |

### BigQuery Federation Setup
1. Enabled `bigquery_fdw` extension on AlloyDB instance
2. Created foreign data wrapper server pointing to BigQuery
3. Created user mapping for authentication
4. Created 8 foreign tables mirroring BigQuery dataset

### Foreign Tables Created
```sql
-- These tables live in AlloyDB but query BigQuery in real-time
allergen, consistsof, containsallergen,
ingredient, product, suppliedby, supplier,
froyo_data_materialized
```

## Challenges Overcome
- **bigquery_fdw.enabled flag**: Required explicit database flag on instance
- **IAM permissions**: AlloyDB service account needed BigQuery roles
- **VPC peering**: Private service access setup for AlloyDB connectivity
- **Billing interruption**: Cluster recreation after billing lapse

## Verification Query
```sql
SELECT p.product_name, i.ingredient_name, a.allergen_name
FROM consistsof c
INNER JOIN product p ON c.product_id = p.product_id
INNER JOIN ingredient i ON c.ingredient_id = i.ingredient_name
LEFT OUTER JOIN containsallergen a ON i.ingredient_id = a.ingredient_id
WHERE UPPER(p.product_name) LIKE '%MIDNIGHT%SWIRL%'
AND a.allergen_name IS NOT NULL;
```
