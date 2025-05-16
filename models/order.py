import sqlite3
from database.db_manager import get_connection
from datetime import datetime

class Order:
    def __init__(self, id=None, client_id=None, product_id=None, order_date=None, 
                 total_amount=None, status="Новый"):  # Установлено значение по умолчанию для status
        self.id = id
        self.client_id = client_id
        self.product_id = product_id
        self.order_date = order_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Значение по умолчанию
        self.total_amount = total_amount or 0.0  # Значение по умолчанию
        self.status = status
        
    def save(self):
        """Сохраняет заказ в базу данных"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if self.id is None:
                cursor.execute("""
                    INSERT INTO orders (client_id, product_id, order_date, total_amount, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (self.client_id, self.product_id, self.order_date, 
                     self.total_amount, self.status))
                self.id = cursor.lastrowid
            else:
                cursor.execute("""
                    UPDATE orders 
                    SET client_id = ?, product_id = ?, order_date = ?, 
                        total_amount = ?, status = ?
                    WHERE id = ?
                """, (self.client_id, self.product_id, self.order_date,
                     self.total_amount, self.status, self.id))
            
            conn.commit()
        except sqlite3.Error as e:  # Более конкретное исключение
            if conn:
                conn.rollback()
            raise Exception(f"Ошибка при сохранении заказа: {str(e)}")
        finally:
            if conn:
                conn.close()

    def delete(self):
        """Удаляет заказ из базы данных"""
        if self.id is None:
            raise ValueError("Нельзя удалить заказ без ID")
            
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orders WHERE id = ?", (self.id,))
            conn.commit()
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise Exception(f"Ошибка при удалении заказа: {str(e)}")
        finally:
            if conn:
                conn.close()

def get_all_orders():
    """Возвращает все заказы"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, client_id, product_id, order_date, total_amount, status
            FROM orders
            ORDER BY order_date DESC
        """)  # Добавлена сортировка
        rows = cursor.fetchall()
        return [
            Order(
                id=row[0],
                client_id=row[1],
                product_id=row[2],
                order_date=row[3],
                total_amount=row[4],
                status=row[5]
            )
            for row in rows
        ]
    except sqlite3.Error as e:
        raise Exception(f"Ошибка при получении заказов: {str(e)}")
    finally:
        if conn:
            conn.close()

def get_order_by_id(order_id):
    """Возвращает заказ по ID"""
    if not order_id:
        raise ValueError("ID заказа не может быть пустым")
        
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, client_id, product_id, order_date, total_amount, status
            FROM orders
            WHERE id = ?
        """, (order_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
            
        return Order(
            id=row[0],
            client_id=row[1],
            product_id=row[2],
            order_date=row[3],
            total_amount=row[4],
            status=row[5]
        )
    except sqlite3.Error as e:
        raise Exception(f"Ошибка при получении заказа: {str(e)}")
    finally:
        if conn:
            conn.close()