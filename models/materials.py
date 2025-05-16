from database.db_manager import get_connection

class Material:
    def __init__(self, id=None, name=None, unit=None, price_per_unit=None, supplier_id=None):
        self.id = id
        self.name = name  # Исправлено: было self.id = name
        self.unit = unit
        self.price_per_unit = price_per_unit
        self.supplier_id = supplier_id
        
    def save(self):
        """Добавляет новый материал или обновляет существующий"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id is None:
                cursor.execute("""
                    INSERT INTO materials (name, unit, price_per_unit, supplier_id)
                    VALUES (?, ?, ?, ?)
                """, (self.name, self.unit, self.price_per_unit, self.supplier_id))
                self.id = cursor.lastrowid
            else:
                cursor.execute("""
                    UPDATE materials 
                    SET name = ?, 
                        unit = ?, 
                        price_per_unit = ?,
                        supplier_id = ?
                    WHERE id = ?
                """, (self.name, self.unit, self.price_per_unit, self.supplier_id, self.id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def delete(self):
        """Удаляет материал"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM materials WHERE id = ?", (self.id,))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                conn.close()

# Вспомогательные функции
def get_all_materials():
    """Возвращает все материалы"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, name, unit, price_per_unit, supplier_id 
            FROM materials
        """)
        rows = cursor.fetchall()
        return [
            Material(
                id=row[0], 
                name=row[1], 
                unit=row[2], 
                price_per_unit=row[3],
                supplier_id=row[4]
            )
            for row in rows
        ]
    except Exception as e:
        raise e
    finally:
        conn.close()

def get_material_by_id(material_id):
    """Возвращает материал по ID"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, name, unit, price_per_unit, supplier_id
            FROM materials
            WHERE id = ?
        """, (material_id,))
        row = cursor.fetchone()
        if row:
            return Material(
                id=row[0], 
                name=row[1], 
                unit=row[2], 
                price_per_unit=row[3],
                supplier_id=row[4]
            )
        return None
    except Exception as e:
        raise e
    finally:
        conn.close()