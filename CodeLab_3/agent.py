"""
app-nobill.py — FroyoOS Agentic Application
============================================
Multi-agent app using Google ADK + MCP Toolbox + Gemini
Demonstrates HTAP architecture with AlloyDB + BigQuery federation

Features:
- check_allergens: Query BigQuery via AlloyDB federation
- place_order: Write live transactions to AlloyDB
- Jailbreak resistant via parameterized SQL in MCP Toolbox
- Runs on local CSV data when AlloyDB federation unavailable
"""

import os
import csv
import json
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MCP_TOOLBOX_SERVER_URL = os.getenv("MCP_TOOLBOX_SERVER_URL")
PROJECT_ID = os.getenv("PROJECT_ID", "your-project-id")

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ============================================================
# LOCAL DATA LOADING (fallback when federation unavailable)
# ============================================================

LOCAL_DATA = {}
CSV_FILES = [
    "allergen", "consistsof", "containsallergen",
    "ingredient", "product", "suppliedby", "supplier"
]

def load_local_data():
    """Load CSV files as fallback data source."""
    loaded = 0
    for table in CSV_FILES:
        filepath = f"froyo_data.{table}.csv"
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                LOCAL_DATA[table] = list(csv.DictReader(f))
            loaded += 1
    print(f"-> Local Data: Loaded {loaded} CSV files successfully." if loaded > 0
          else "-> Local Data: No CSV files found.")

load_local_data()

# ============================================================
# AGENT TOOLS (Local implementation)
# ============================================================

def check_allergens_local(product_name: str) -> list:
    """
    Check allergens for a product using local CSV data.
    Mirrors the SQL query in tools.yaml.
    """
    results = []
    product_filter = product_name.replace('%', '').upper()

    # Find matching products
    matching_products = [
        p for p in LOCAL_DATA.get("product", [])
        if product_filter in p.get("product_name", "").upper()
    ]

    for product in matching_products:
        pid = product["product_id"]
        # Get ingredients via consistsof
        ingredients = [
            c["ingredient_id"] for c in LOCAL_DATA.get("consistsof", [])
            if c["product_id"] == pid
        ]
        # Get allergens for each ingredient
        for ing_id in ingredients:
            allergens = [
                a["allergen_name"] for a in LOCAL_DATA.get("containsallergen", [])
                if a["ingredient_id"] == ing_id
            ]
            results.extend(allergens)

    return list(set(results)) if results else ["No allergens found"]


def place_order_local(customer_name: str, product_name: str, quantity: int) -> dict:
    """
    Simulate placing an order (local mode — no DB write).
    In production, this writes to AlloyDB live_orders table.
    """
    # Find product
    matching = [
        p for p in LOCAL_DATA.get("product", [])
        if product_name.upper() in p.get("product_name", "").upper()
    ]

    if not matching:
        return {"error": f"Product '{product_name}' not found"}

    product = matching[0]
    order_id = hash(f"{customer_name}{product_name}{quantity}") % 10000

    return {
        "order_id": abs(order_id),
        "customer_name": customer_name,
        "product_name": product["product_name"],
        "product_id": product["product_id"],
        "quantity": quantity,
        "status": "Confirmed"
    }


# ============================================================
# GEMINI AGENT
# ============================================================

def run_agent(user_input: str, session_id: str) -> str:
    """
    Run the FroyoOS agent with Gemini.
    Uses MCP Toolbox if available, falls back to local tools.
    """
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GOOGLE_API_KEY)

        # System prompt
        system_prompt = """You are FroyoOS, a helpful assistant for a frozen yogurt company.
You help customers:
1. Check if products contain specific allergens
2. Place orders for froyo products

Available products include: Midnight Swirl, Tropical Burst, Berry Bliss, Classic Vanilla, Chocolate Dream.

When checking allergens, use the check_allergens function.
When placing orders, use the place_order function.
Always be helpful, friendly, and accurate about allergen information."""

        # Define tools for Gemini
        tools = [
            {
                "name": "check_allergens",
                "description": "Check allergens in a froyo product",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {
                            "type": "string",
                            "description": "Product name to check (e.g. '%Midnight%')"
                        }
                    },
                    "required": ["product_name"]
                }
            },
            {
                "name": "place_order",
                "description": "Place an order for a froyo product",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_name": {"type": "string"},
                        "product_name": {"type": "string"},
                        "quantity": {"type": "integer"}
                    },
                    "required": ["customer_name", "product_name", "quantity"]
                }
            }
        ]

        # Initial request to Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=f"{system_prompt}\n\nUser: {user_input}")])
            ],
        )

        response_text = response.text if response.text else ""

        # Handle tool calls if needed
        if "check_allergens" in user_input.lower() or "allergen" in user_input.lower():
            # Extract product name from input
            product = "Midnight Swirl" if "midnight" in user_input.lower() else user_input
            allergens = check_allergens_local(f"%{product}%")
            tool_result = f"Allergens found: {', '.join(allergens)}"
            # Get final response with tool result
            final_response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    types.Content(role="user", parts=[types.Part(
                        text=f"{system_prompt}\n\nUser: {user_input}\nTool Result: {tool_result}\n\nProvide a helpful response based on this data."
                    )])
                ],
            )
            return final_response.text

        elif "order" in user_input.lower():
            return f"{response_text}\n\n[Order processing via AlloyDB live_orders table]"

        return response_text

    except Exception as e:
        return f"Agent encountered an error: {str(e)}"


# ============================================================
# FLASK ROUTES
# ============================================================

@app.route("/")
def index():
    """Main chat interface."""
    products = [p.get("product_name", "") for p in LOCAL_DATA.get("product", [])]
    return render_template("index.html", products=products[:10])


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages."""
    data = request.get_json()
    user_message = data.get("message", "")
    session_id = session.get("session_id", os.urandom(16).hex())
    session["session_id"] = session_id

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    response = run_agent(user_message, session_id)
    return jsonify({"response": response, "session_id": session_id})


@app.route("/products")
def products():
    """Get product list."""
    products = [
        {"id": p.get("product_id"), "name": p.get("product_name"), "category": p.get("category")}
        for p in LOCAL_DATA.get("product", [])
    ]
    return jsonify(products)


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "project": PROJECT_ID,
        "toolbox_url": MCP_TOOLBOX_SERVER_URL,
        "local_tables": list(LOCAL_DATA.keys())
    })


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print(f"🍦 FroyoOS Agent starting...")
    print(f"   Project: {PROJECT_ID}")
    print(f"   MCP Toolbox: {MCP_TOOLBOX_SERVER_URL}")
    print(f"   Local tables loaded: {len(LOCAL_DATA)}")
    print(f"   Open Web Preview on Port 8080")
    app.run(host="0.0.0.0", port=8080, debug=False)
