# FroyoOS — Antigravity IDE Agent Context

## 1. Project Context
- **Project ID**: codevipasana-4
- **Domain**: This project is centralized around "Froyo", a brand of frozen yogurt offering multiple flavors including Midnight Swirl, Tropical Burst, Berry Bliss, Classic Vanilla, and Chocolate Dream.
- **Data**: All froyo product specs, customer data, and order information is stored in BigQuery `froyo_data` dataset in project `codevipasana-4`.

## 2. Dataset Structure

### Product & Ingredient Tables (from PDF extraction via Dataplex)
| Table | Description |
|-------|-------------|
| `froyo_data.product` | Froyo product catalog (product_id, product_name, category, stability) |
| `froyo_data.ingredient` | Ingredients (ingredient_id, ingredient_name, purity, moisture_content, ph_range, specific_gravity_range) |
| `froyo_data.allergen` | Allergen types (allergen_name) |
| `froyo_data.consistsof` | Product-ingredient relationships (product_id, ingredient_id) |
| `froyo_data.containsallergen` | Ingredient-allergen mapping (ingredient_id, allergen_name) |
| `froyo_data.suppliedby` | Ingredient-supplier links (ingredient_id, supplier_id) |
| `froyo_data.supplier` | Supplier info (supplier_id, supplier_name, production_site_id, facility_grade) |

### Transaction & Customer Tables
| Table | Description |
|-------|-------------|
| `froyo_data.orders` | Customer orders (order_id, customer_id, order_date, total_amount) |
| `froyo_data.order_items` | Order line items (order_item_id, order_id, product_id, quantity, unit_price) |
| `froyo_data.customer_allergen_data` | Customer allergy profiles (customer_id, customer_name, allergen_name) |

## 3. Execution & Data Processing Rules

- **CRITICAL RULE — Dataset Reference**: Always use full table references with dataset ID. Example: `froyo_data.orders` NOT just `orders`.
- **CRITICAL RULE — Customer Data**: Froyo customer allergy data is in `froyo_data.customer_allergen_data`.
- **CRITICAL RULE — Sales Data**: Sales data is in `froyo_data.orders` and `froyo_data.order_items`.
- **CRITICAL RULE — Product Data**: Product and ingredient data extracted from PDFs is in `froyo_data.product`, `froyo_data.ingredient`, etc.
- **CRITICAL RULE — Allergen Queries**: To find allergens for a product, JOIN product → consistsof → ingredient → containsallergen.

## 4. Sample Query Patterns

### Find allergens for a product:
```sql
SELECT p.product_name, a.allergen_name
FROM `codevipasana-4.froyo_data.product` p
JOIN `codevipasana-4.froyo_data.consistsof` c ON p.product_id = c.product_id
JOIN `codevipasana-4.froyo_data.ingredient` i ON c.ingredient_id = i.ingredient_id
JOIN `codevipasana-4.froyo_data.containsallergen` ca ON i.ingredient_id = ca.ingredient_id
JOIN `codevipasana-4.froyo_data.allergen` a ON ca.allergen_name = a.allergen_name
WHERE UPPER(p.product_name) LIKE '%MIDNIGHT%SWIRL%';
```

### Top products for customers with specific allergy:
```sql
SELECT p.product_name, COUNT(*) as purchase_count
FROM `codevipasana-4.froyo_data.orders` o
JOIN `codevipasana-4.froyo_data.order_items` oi ON o.order_id = oi.order_id
JOIN `codevipasana-4.froyo_data.product` p ON oi.product_id = p.product_id
JOIN `codevipasana-4.froyo_data.customer_allergen_data` cad ON o.customer_id = cad.customer_id
WHERE UPPER(cad.allergen_name) = 'DAIRY'
GROUP BY p.product_name
ORDER BY purchase_count DESC
LIMIT 5;
```

## 5. Agent Behavior Guidelines
- Always verify table existence before querying
- Use parameterized queries where possible
- For forecasting, use BigQuery ML (BQML) with CREATE MODEL and ML.FORECAST
- Present results in a clear, business-friendly format
- Flag any data quality issues found during analysis
