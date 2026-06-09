#!/bin/bash
# Codelab 5 — Load Additional BigQuery Tables
# Loads orders, order_items, customer_allergen_data tables
# Required for Antigravity IDE analytics and BigQuery Agent

set -e

export PROJECT_ID=${PROJECT_ID:-"your-project-id"}
export DATASET="froyo_data"
export GITHUB_RAW="https://raw.githubusercontent.com/AbiramiSukumaran/froyo-data/main"

echo "🚀 Loading Codelab 5 BigQuery Tables..."
echo "Project: $PROJECT_ID | Dataset: $DATASET"

# Download CSV files
echo "📥 Downloading CSV files..."
wget -q ${GITHUB_RAW}/orders.csv -O /tmp/orders.csv
wget -q ${GITHUB_RAW}/order_items.csv -O /tmp/order_items.csv
wget -q ${GITHUB_RAW}/customer_allergen_data.csv -O /tmp/customer_allergen_data.csv
echo "✅ Downloads complete"

# Load orders table
echo "📊 Loading orders table..."
bq load \
  --autodetect \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --allow_quoted_newlines \
  --quote="" \
  ${DATASET}.orders \
  /tmp/orders.csv 2>/dev/null || echo "Table already exists"
echo "✅ orders loaded"

# Load order_items table
echo "📊 Loading order_items table..."
bq load \
  --autodetect \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --allow_quoted_newlines \
  --quote="" \
  ${DATASET}.order_items \
  /tmp/order_items.csv 2>/dev/null || echo "Table already exists"
echo "✅ order_items loaded"

# Load customer_allergen_data table
echo "📊 Loading customer_allergen_data table..."
bq load \
  --autodetect \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --allow_quoted_newlines \
  --quote="" \
  ${DATASET}.customer_allergen_data \
  /tmp/customer_allergen_data.csv 2>/dev/null || echo "Table already exists"
echo "✅ customer_allergen_data loaded"

# Verify — should show 11 tables
echo ""
echo "📋 Verifying all tables (should be 11):"
bq ls --project_id=$PROJECT_ID $DATASET

echo ""
echo "✅ Codelab 5 Data Setup Complete!"
echo ""
echo "Next Steps:"
echo "1. Open Antigravity IDE and configure Data Agent Kit"
echo "2. Create GEMINI.md in your project folder"
echo "3. Create BigQuery Conversational Agent at:"
echo "   https://console.cloud.google.com/bigquery/agents?project=$PROJECT_ID"
