#!/bin/bash
# Codelab 3 — FroyoOS Agent App Deployment Script
# Deploys MCP Toolbox to Cloud Run with AlloyDB VPC connectivity

set -e

export PROJECT_ID=${PROJECT_ID:-"your-project-id"}
export REGION="us-central1"
export SERVICE_NAME="toolbox-froyo"
export SECRET_NAME="tools-froyo"
export SA_NAME="toolbox-identity"
export VPC_NAME="alloydb-vpc"
export SUBNET_NAME="alloydb-subnet"
export IMAGE="us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest"

echo "🚀 Starting Codelab 3 Deployment..."
echo "Project: $PROJECT_ID | Region: $REGION"

# Enable required APIs
echo "📡 Enabling APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  --project=$PROJECT_ID

# Create service account
echo "👤 Creating service account..."
gcloud iam service-accounts create $SA_NAME \
  --display-name="MCP Toolbox Service Account" \
  --project=$PROJECT_ID 2>/dev/null || echo "SA already exists"

# Grant required roles to service account
echo "🔑 Granting IAM roles..."
for ROLE in \
  roles/secretmanager.secretAccessor \
  roles/alloydb.client \
  roles/serviceusage.serviceUsageConsumer \
  roles/bigquery.dataViewer \
  roles/bigquery.user; do
    gcloud projects add-iam-policy-binding $PROJECT_ID \
      --member="serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
      --role="$ROLE" --quiet
    echo "  ✅ $ROLE"
done

# Create secret from tools.yaml
echo "🔐 Creating Secret Manager secret..."
gcloud secrets delete $SECRET_NAME --project=$PROJECT_ID --quiet 2>/dev/null || true
gcloud secrets create $SECRET_NAME \
  --data-file=tools.yaml \
  --project=$PROJECT_ID
echo "  ✅ Secret created: $SECRET_NAME"

# Deploy to Cloud Run
echo "☁️ Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --service-account ${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
  --region $REGION \
  --set-secrets "/app/tools.yaml=${SECRET_NAME}:latest" \
  --args="--config=/app/tools.yaml","--address=0.0.0.0","--port=8080" \
  --network $VPC_NAME \
  --subnet $SUBNET_NAME \
  --allow-unauthenticated \
  --vpc-egress private-ranges-only \
  --project=$PROJECT_ID

# Get Cloud Run URL
CLOUD_RUN_URL=$(gcloud run services describe $SERVICE_NAME \
  --region=$REGION \
  --project=$PROJECT_ID \
  --format="value(status.url)")

echo ""
echo "✅ Deployment Complete!"
echo "Cloud Run URL: $CLOUD_RUN_URL"
echo ""
echo "Next Steps:"
echo "1. Update .env file with: MCP_TOOLBOX_SERVER_URL=$CLOUD_RUN_URL"
echo "2. Run: pip install -r requirements.txt"
echo "3. Run: python app-nobill.py"
echo "4. Open Web Preview on Port 8080"
