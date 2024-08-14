from models import SubscriptionPlan, Payment, User
from utils.paystack import create_payment, verify_payment
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session, select
from database import get_session
from utils.auth import get_current_active_client
from datetime import datetime, timedelta


subs_route = APIRouter()


@subs_route.get("/subscriptions/view")
def get_subscription_plans(session: Session = Depends(get_session),
                      current_user: User = Depends(get_current_active_client)
                      ):
    query = select(SubscriptionPlan)
    subs_plan = session.exec(query).all()
    return [
        {
            "plan_name": sub.plan_name,
            "features": sub.features,
            "price": sub.price
        }
        for sub in subs_plan
    ]



@subs_route.post("/pay/{sub_type}")
def  pay_per_sub( sub_type: str,
                   background_tasks: BackgroundTasks,
                    session: Session = Depends(get_session),
                    current_user: User = Depends(get_current_active_client),
                    ):
    # Create a payment
    query = select(SubscriptionPlan).where(SubscriptionPlan.plan_name == sub_type)
    subscription_plan = session.exec(query).first()
    payment_result = create_payment(
            amount=subscription_plan.price,  
            email=current_user.email,
            currency="NGN"
        )
    BackgroundTasks
    payment_data = {
        "user_id": current_user.user_id,
        "plan_id": subscription_plan.plan_id,
        "amount": subscription_plan.price,
        "currency": "NGN",

    }

    
    background_tasks.add_task(verify_and_update_payment, payment_result["reference"], payment_data, session)

    if "error" in payment_result:
        raise HTTPException(status_code=400, detail=payment_result["error"])
    
    return{
      "message": "payment initiated",
      "payment_url": payment_result["auth_url"],
      "reference" : payment_result["reference"]
    }


async def verify_and_update_payment(reference: str, payment_data: dict, session: Session):
    verification_result = await verify_payment(reference)
    if verification_result['status'] == "success":
        new_payment = Payment(
            user_id=payment_data["user_id"],
            plan_id=payment_data["plan_id"],
            amount=payment_data["amount"],
            currency=payment_data["currency"],
            refrence_id= reference,
            payment_status="success"
        )
        session.add(new_payment)
        user = session.get(User, payment_data["user_id"])
        if user:
            user.subscription_plan_id = payment_data["plan_id"]
            # Assuming the subscription is for 30 days
            user.subscription_end_date = datetime.utcnow() + timedelta(days=30)
        
        session.commit()
    else:
        print(f"Payment {reference} failed or timed out")
