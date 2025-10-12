#!/usr/bin/env python3
import os
import json
import sys
import time
from typing import Any

try:
    import requests
except ImportError:
    print("The 'requests' package is required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

BASE_URL = os.getenv("API_BASE", "http://localhost:8000")


def pretty(title: str, obj: Any):
    print(f"\n=== {title} ===")
    try:
        print(json.dumps(obj, indent=2)[:8000])
    except Exception:
        print(str(obj)[:8000])


def get(path: str):
    return requests.get(f"{BASE_URL}{path}", timeout=30)


def post(path: str, json_body=None, files=None, data=None):
    return requests.post(f"{BASE_URL}{path}", json=json_body, files=files, data=data, timeout=60)


def main():
    print(f"Using API base: {BASE_URL}")

    # Health
    r = get("/health")
    pretty("GET /health", {"status_code": r.status_code, "body": r.json() if r.ok else r.text})

    # Status
    r = get("/status")
    pretty("GET /status", {"status_code": r.status_code, "body": r.json() if r.ok else r.text})

    # Assistant (generic)
    r = post("/assistant", json_body={"message": "Order milk and tomatoes", "user_id": "tester"})
    pretty("POST /assistant", {"status_code": r.status_code, "body": r.json() if r.ok else r.text})

    # Quick order
    r = post("/quick-order", json_body={
        "items": ["milk", "tomatoes"],
        "user_id": "tester",
        "delivery_preference": "fastest",
        "auto_approve": False
    })
    pretty("POST /quick-order", {"status_code": r.status_code, "body": r.json() if r.ok else r.text})

    # Quick order approve (dummy)
    r = post("/quick-order/approve", json_body={
        "order_id": "sample-order-id",
        "approved": True,
        "user_id": "tester"
    })
    pretty("POST /quick-order/approve", {"status_code": r.status_code, "body": r.json() if r.ok else r.text})

    # Quick order status (dummy)
    r = get("/quick-order/status/sample-order-id")
    pretty("GET /quick-order/status/{order_id}", {"status_code": r.status_code, "body": r.json() if r.ok else r.text})

    # Payment create order (dummy values)
    r = post("/payment/create-order", json_body={
        "amount": 100.0,
        "currency": "INR",
        "receipt": "rcpt_123"
    })
    pretty("POST /payment/create-order", {"status_code": r.status_code, "body": r.json() if r.ok else r.text})

    # Payment verify (dummy; likely to error but validates path/logs)
    r = post("/payment/verify", json_body={
        "payment_id": "pay_dummy",
        "order_id": "order_dummy",
        "signature": "sig_dummy"
    })
    pretty("POST /payment/verify", {"status_code": r.status_code, "body": r.json() if r.ok else r.text})

    # Payment create link
    r = post("/payment/create-link", json_body={
        "amount": 99.0,
        "currency": "INR",
        "description": "Test link",
        "reference_id": "ref_1"
    })
    pretty("POST /payment/create-link", {"status_code": r.status_code, "body": r.json() if r.ok else r.text})

    # Payment methods
    r = get("/payment/methods")
    pretty("GET /payment/methods", {"status_code": r.status_code, "body": r.json() if r.ok else r.text})

    # Speech languages
    r = get("/speech/languages")
    pretty("GET /speech/languages", {"status_code": r.status_code, "body": r.json() if r.ok else r.text})

    # Test endpoints
    for path in ["/test/food", "/test/travel", "/test/shopping", "/test/payment", "/test/quick-commerce"]:
        r = post(path)
        pretty(f"POST {path}", {"status_code": r.status_code, "body": r.json() if r.ok else r.text})

    print("\nSmoke test complete. Check app.log for detailed backend logs.")


if __name__ == "__main__":
    main()
