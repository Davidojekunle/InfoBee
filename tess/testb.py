# from fastapi import APIRouter, Depends, HTTPException, Request
# from utils.paystack import initialize_subscription, verify_payment
# from schemas.payments import PaymentRequest, PaymentResponse
# from models import User, SubscriptionPlan, Payment
# from utils.auth import get_current_active_client
# from database import get_session
# from sqlmodel import Session, select
# from datetime import datetime

# payments_router = APIRouter()

# @payments_router.post("/subscribe", response_model=PaymentResponse)
# async def subscribe_to_plan(
#     plan_id: int,
#     current_user: User = Depends(get_current_active_client),
#     session: Session = Depends(get_session)
# ):
#     plan = session.get(SubscriptionPlan, plan_id)
#     if not plan:
#         raise HTTPException(status_code=404, detail="Subscription plan not found")

#     if plan.plan_name == "Free":
#         if current_user.trial_ >= 5:
#             raise HTTPException(status_code=403, detail="Free trial limit reached")
#         current_user.subscription_plan_id = plan_id
#         current_user.subscription_start_date = datetime.utcnow()
#         current_user.trial_usage += 1
#         session.add(current_user)
#         session.commit()
#         return {"message": "Subscribed to free plan"}

#     customer_id = "CUS_xnxdt6s1zg1f4nx"  # You should fetch this from your user data or Paystack customer creation process
#     subscription_response = initialize_subscription(customer=customer_id, plan=plan.plan_code)
#     return PaymentResponse(status=True, message="Subscription initialized", data=subscription_response)
