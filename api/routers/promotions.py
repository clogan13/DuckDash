from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models.Promotion import Promotion
from ..schemas.Promotion import PromotionBase, PromotionCreate, PromotionUpdate, PromotionResponse
from typing import List
from datetime import date

router = APIRouter(
    prefix="/promotions",
    tags=["promotions"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=PromotionResponse, status_code=status.HTTP_201_CREATED)
def create_promotion(promo: PromotionCreate, db: Session = Depends(get_db)):
    new_promo = Promotion(
        code=promo.code,
        discount_percent=promo.discount_percent,
        discount_amount=promo.discount_amount,
        start_date=promo.start_date.date() if promo.start_date else date.today(),
        end_date=promo.end_date.date() if promo.end_date else date.today(),
        description=promo.description,
        usage_limit=None
    )
    db.add(new_promo)
    db.commit()
    db.refresh(new_promo)
    return new_promo

@router.get("/", response_model=List[PromotionResponse])
def list_promotions(db: Session = Depends(get_db)):
    return db.query(Promotion).all()

@router.get("/{code}", response_model=PromotionResponse)
def get_promotion(code: str, db: Session = Depends(get_db)):
    promo = db.query(Promotion).filter(Promotion.code == code).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promo

@router.put("/{code}", response_model=PromotionResponse)
def update_promotion(code: str, promo_update: PromotionUpdate, db: Session = Depends(get_db)):
    promo = db.query(Promotion).filter(Promotion.code == code).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promotion not found")
    for field, value in promo_update.dict(exclude_unset=True).items():
        if hasattr(promo, field):
            setattr(promo, field, value)
    db.commit()
    db.refresh(promo)
    return promo

@router.delete("/{code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_promotion(code: str, db: Session = Depends(get_db)):
    promo = db.query(Promotion).filter(Promotion.code == code).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promotion not found")
    db.delete(promo)
    db.commit()
    return None

@router.get("/validate/{code}")
def validate_promotion(code: str, db: Session = Depends(get_db)):
    promo = db.query(Promotion).filter(Promotion.code == code).first()
    now = date.today()
    if not promo:
        return {"valid": False, "reason": "Promotion not found"}
    if promo.start_date > now or promo.end_date < now:
        return {"valid": False, "reason": "Promotion not active"}
    if promo.usage_limit is not None and promo.usage_limit <= 0:
        return {"valid": False, "reason": "Usage limit reached"}
    return {"valid": True, "discount_percent": promo.discount_percent, "discount_amount": promo.discount_amount} 