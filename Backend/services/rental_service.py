# 대여 관련 기능

from database import db
from models import Rental
import datetime

# 물품 대여 처리
def borrow_item(student_id, item_name, item_ids):
    borrowed_items = []
    errors = []

    for item_id in item_ids:
        existing_rental = Rental.query.filter_by(id=item_id, rental_status=True).first()
        
        if existing_rental:
            errors.append(f"{item_name} {item_id}번은 이미 대여 중입니다.")
        else:
            rental = Rental(
                student_id=student_id,
                product_name=item_name,
                id=item_id,
                rental_time=datetime.datetime.now(),
                rental_status=True
            )
            db.session.add(rental)
            borrowed_items.append(item_id)
    
    db.session.commit()

    if errors:
        return {"error": errors}, 400
    return {"message": f"{item_name} {borrowed_items}번 대여 성공!"}

# 대여 상태 조회
def get_rental_status(student_id):
    rentals = Rental.query.filter_by(student_id=student_id, rental_status=True).all()
    rental_list = [
        {
            "id": r.id,
            "product_name": r.product_name,
            "rental_time": r.rental_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        for r in rentals
    ]
    return {"rented_items": rental_list}
