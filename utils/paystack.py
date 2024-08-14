import requests
from fastapi import HTTPException, status
from dotenv import load_dotenv
import hmac
import hashlib
import hashlib
import os
import logging
import asyncio

load_dotenv()

logger = logging.getLogger(__name__)


PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SK')
PAYSTACK_BASE_URL = "https://api.paystack.co"


def create_payment(email: str, amount: int, currency: str):
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "email": email,
        "amount": int(amount * 100),  
        "currency": currency
    }
    
    response = requests.post(f"{PAYSTACK_BASE_URL}/transaction/initialize", json=payload, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"Failed to initiate payment: {response.text}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to initiate payment: {response.json().get('message', 'Unknown error')}"
        )
    
    
    return {
                "auth_url": response.json()["data"]["authorization_url"],
                "reference": response.json()["data"]["reference"]
            }

async def verify_payment(reference, max_retries=12, retry_delay=10):
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}", headers=headers)
            response.raise_for_status()
            
            response_data = response.json()
            payment_status = response_data["data"]["status"]
            
            if payment_status == "success":
                return {"status": "success", "data": response_data["data"]}
            elif payment_status == "failed":
                return {"status": "failed", "data": response_data["data"]}
            else:
                print(f"Payment status: {payment_status}. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
        
        except requests.RequestException as e:
            print(f"Error verifying payment: {e}. Retrying in {retry_delay} seconds...")
            await asyncio.sleep(retry_delay)
    
    return {"status": "timeout", "message": "Failed to verify payment after maximum retries"}



async def verify_webhook_signature(request):
    paystack_signature = request.headers.get("x-paystack-signature")
    if not paystack_signature:
        return False

    payload = await request.body()

    computed_signature = hmac.new(
        PAYSTACK_SECRET_KEY.encode('utf-8'),
        payload,
        hashlib.sha512
    ).hexdigest()

    return hmac.compare_digest(computed_signature, paystack_signature)


