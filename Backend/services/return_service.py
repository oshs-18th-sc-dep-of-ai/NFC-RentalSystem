# 반납 관련 기능

from database import db
from models import Rental
import datetime

# 반납 처리 서비스 로직
def return_item(student_id, item_ids):
    updated_items = []
    errors = []

    for item_id in item_ids:
        rental = Rental.query.filter_by(id=item_id, student_id=student_id, rental_status=True).first()
        
        if not rental:
            errors.append(f"{item_id}번 물품의 대여 기록을 찾을 수 없습니다.")
        else:
            rental.rental_status = False  # 반납 완료
            rental.return_time = datetime.datetime.now()
            updated_items.append(item_id)
    
    db.session.commit()
    
    if errors:
        return {"error": errors}, 400
    return {"message": f"{updated_items}번 물품 반납 완료!"}
