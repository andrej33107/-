from database.db_manager import get_connection

class Product:
    def __init__(self, id=None, name=None, size=None, price=None, stock=None, category_id=None):
        self.id = id
        self.name = name
        self.size = size
        self.price = price
        self.stock = stock
        self.category_id = category_id
        
    def save(self):
        """Сохраняет товар в базу данных"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if self.id is None:
                cursor.execute("""
                    INSERT INTO products (name, size, price, stock, category_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (self.name, self.size, self.price, self.stock, self.category_id))
                self.id = cursor.lastrowid
            else:
                cursor.execute("""
                    UPDATE products 
                    SET name = ?, size = ?, price = ?, stock = ?, category_id = ?
                    WHERE id = ?
                """, (self.name, self.size, self.price, self.stock, self.category_id, self.id))
            
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def delete(self):
        """Удаляет товар из базы данных"""
        if self.id is not None:
            conn = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM products WHERE id = ?", (self.id,))
                conn.commit()
            except Exception as e:
                if conn:
                    conn.rollback()
                raise e
            finally:
                if conn:
                    conn.close()

def get_all_products():
    """Возвращает все товары из базы данных"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, size, price, stock, category_id
            FROM products
        """)  # Убрана лишняя запятая после category_id
        rows = cursor.fetchall()
        return [
            Product(
                id=row[0],
                name=row[1],
                size=row[2],
                price=row[3],
                stock=row[4],
                category_id=row[5]
            )
            for row in rows
        ]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def get_product_by_id(product_id):
    """Возвращает товар по его ID"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, size, price, stock, category_id
            FROM products
            WHERE id = ?
        """, (product_id,))
        row = cursor.fetchone()
        if row:
            return Product(
                id=row[0],
                name=row[1],
                size=row[2],
                price=row[3],
                stock=row[4],
                category_id=row[5]
            )
        return None
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()