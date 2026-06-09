# Codelab 5 — Data Agents in Antigravity IDE & BigQuery 🚀

## Overview
Implemented two complementary data agent experiences:
1. **Antigravity IDE** with Google Cloud Data Agent Kit — developer-focused analytical agent
2. **BigQuery Conversational Analytics Agent** — business user natural language interface

## Architecture
```
                    FroyoOS Data Agents
                           │
          ┌────────────────┴────────────────┐
          │                                  │
   Antigravity IDE                  BigQuery Agent
   (Developer Experience)           (Business Experience)
          │                                  │
   Data Agent Kit                   Conversational Analytics
          │                                  │
   Generates + Executes SQL         Natural Language → SQL
          │                                  │
          └────────────┬───────────────────┘
                       │
               BigQuery froyo_data
               (11 tables total)
```

## Part A — Antigravity IDE

### Setup
- **IDE**: Antigravity 2.0
- **Extension**: Google Cloud Data Agent Kit
- **Context File**: `GEMINI.md` (provides domain knowledge)
- **Project**: codevipasana-4

### GEMINI.md Purpose
Provides the agent with:
- Project context and domain knowledge
- Table relationships and naming conventions
- Critical rules for data access patterns

### Sample Queries Executed
1. `Does Midnight Swirl contain any allergen?`
   - Generated JOIN query across product, consistsof, ingredient, containsallergen
   - Returned: Soy allergen identified

2. `Top 5 products purchased by dairy-allergic customers`
   - Generated complex multi-table JOIN
   - Used: orders, order_items, customer_allergen_data, product

3. `Forecast sales for next 30 days`
   - Generated BQML CREATE MODEL statement
   - Used: ML.FORECAST for time series prediction

## Part B — BigQuery Conversational Agent

### Agent Configuration
| Setting | Value |
|---------|-------|
| Agent Name | Froyo Agent |
| Dataset | froyo_data (codevipasana-4) |
| Tables | 10 tables (all froyo_data tables) |
| Status | Published ✅ |

### Knowledge Sources (10 Tables)
```
allergen, consistsof, containsallergen, ingredient,
product, suppliedby, supplier, orders, order_items,
customer_allergen_data
```

### Test Results
| Query | Result |
|-------|--------|
| Allergen check for Midnight Swirl | ✅ Soy identified |
| Top 5 products for dairy-allergic customers | ✅ Table returned |
| 30-day sales forecast | ✅ Chart + data returned |
| 2026 top selling product prediction | ✅ Forecast generated |

## Files
| File | Description |
|------|-------------|
| `GEMINI.md` | Antigravity IDE context file |
| `load_tables.sh` | Script to load 3 extra BigQuery tables |
| `bq_agent_config.json` | BigQuery agent configuration export |
