from app import mysql

def get_summary():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT 
            (SELECT COUNT(*) FROM Rentals WHERE rental_status = 1) AS borrowed_items,
            (SELECT COUNT(*) FROM Rentals WHERE rental_status = 2) AS pending_returns,
            (SELECT COUNT(*) FROM Rentals WHERE rental_status = 3) AS overdue_items
    """)
    result = cursor.fetchone()
    cursor.close()
    return {
        "borrowed_items": result[0],
        "pending_returns": result[1],
        "overdue_items": result[2],
        "overdue_items": result[2]
    }

def add_item(data):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO Products (product_name, category, quantity, description, status) 
            VALUES (%s, %s, %s, %s, 'available')
        """, (data['name'], data['category'], data['quantity'], data.get('description', '')))
        mysql.connection.commit()
        return {"message": "Item added successfully!"}
    except Exception as e:
        mysql.connection.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()

def delete_item(item_id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM Products WHERE product_id = %s", (item_id,))
        mysql.connection.commit()
        return {"message": "Item deleted successfully!"}
    except Exception as e:
        mysql.connection.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()

def update_item_status(item_id, status):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("""
            UPDATE Products 
            SET status = %s 
            WHERE product_id = %s
        """, (status, item_id))
        mysql.connection.commit()
        return {"message": "Item status updated successfully!"}
    except Exception as e:
        mysql.connection.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()

def force_return(rental_id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("""
            UPDATE Rentals 
            SET rental_status = 0, rental_returntime = NOW() 
            WHERE rental_id = %s
        """, (rental_id,))
        mysql.connection.commit()
        return {"message": "Item forcibly returned!"}
    except Exception as e:
        mysql.connection.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()
