from database.db_manager import get_connection

class Client:
    def __init__(self, id=None, name=None, phone=None, email=None, address=None):
        self.id = id
        self.name = name  # Исправлено: было self.id = name (как в вашем оригинале)
        self.phone = phone
        self.email = email
        self.address = address
        
    def save(self):
        """Добавляет нового клиента или обновляет существующего"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id is None:
                cursor.execute("""
                    INSERT INTO clients (name, phone, email, address)
                    VALUES (?, ?, ?, ?)
                """, (self.name, self.phone, self.email, self.address))
                self.id = cursor.lastrowid
            else:
                cursor.execute("""
                    UPDATE clients 
                    SET name = ?, 
                        phone = ?,
                        email = ?,
                        address = ?
                    WHERE id = ?
                """, (self.name, self.phone, self.email, self.address, self.id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def delete(self):
        """Удаляет клиента"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM clients WHERE id = ?", (self.id,))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                conn.close()

# Вспомогательные функции
def get_all_clients():
    """Возвращает всех клиентов"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, name, phone, email, address 
            FROM clients
        """)
        rows = cursor.fetchall()
        return [
            Client(
                id=row[0], 
                name=row[1], 
                phone=row[2], 
                email=row[3],
                address=row[4]
            )
            for row in rows
        ]
    except Exception as e:
        raise e
    finally:
        conn.close()

def get_client_by_id(client_id):
    """Возвращает клиента по ID"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, name, phone, email, address
            FROM clients
            WHERE id = ?
        """, (client_id,))
        row = cursor.fetchone()
        if row:
            return Client(
                id=row[0], 
                name=row[1], 
                phone=row[2], 
                email=row[3],
                address=row[4]
            )
        return None
    except Exception as e:
        raise e
    finally:
        conn.close()