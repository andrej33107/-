from database.db_manager import get_connection

class Category:
    def __init__(self, id=None, name=None, description=None):
        self.id = id
        self.name = name
        self.description = description
        
    def save(self):
        """Добавляет новую категорию или обновляет существующую"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id is None:
                cursor.execute("""
                    INSERT INTO categories (name, description)
                    VALUES (?, ?)
                """, (self.name, self.description))
                self.id = cursor.lastrowid
            else:
                cursor.execute("""
                    UPDATE categories 
                    SET name = ?, 
                        description = ?
                    WHERE id = ?
                """, (self.name, self.description, self.id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def delete(self):
        """Удаляет категорию"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM categories WHERE id = ?", (self.id,))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                conn.close()

# Вспомогательные функции
def get_all_categories():
    """Возвращает все категории"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, description FROM categories")
        rows = cursor.fetchall()
        return [
            Category(
                id=row[0], 
                name=row[1], 
                description=row[2]
            )
            for row in rows
        ]
    except Exception as e:
        raise e
    finally:
        conn.close()

def get_category_by_id(category_id):
    """Возвращает категорию по ID"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, name, description 
            FROM categories 
            WHERE id = ?
        """, (category_id,))
        row = cursor.fetchone()
        if row:
            return Category(
                id=row[0], 
                name=row[1], 
                description=row[2]
            )
        return None
    except Exception as e:
        raise e
    finally:
        conn.close()
        