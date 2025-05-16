from models.clients import Client, get_all_clients, get_client_by_id

def menu_clients():
    while True:
        print("\n=== 😀Управление клиентами😀 ===")
        print("1. Показать всех клиентов")
        print("2. Добавить клиента")
        print("3. Удалить клиента")
        print("4. Изменить клиента")
        print("0. Назад в главное меню")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            show_all_clients()
        elif choice == "2":
            add_new_client()
        elif choice == "3":
            delete_client()
        elif choice == "4":
            edit_client()
        elif choice == "0":
            break
        else:
            print("❌ Неверный ввод. Пожалуйста, выберите действие из меню.")

def show_all_clients():
    """Показать всех клиентов"""
    clients = get_all_clients()
    if not clients:
        print("\nСписок клиентов пуст.")
        return
        
    print("\nСписок клиентов:")
    for client in clients:
        print(f"{client.id}. {client.name} | Телефон: {client.phone} | "
              f"Email: {client.email if client.email else 'N/A'} | "
              f"Адрес: {client.address if client.address else 'N/A'}")

def add_new_client():
    """Добавить нового клиента"""
    print("\n=== Добавление нового клиента ===")
    
    try:
        name = input("Имя клиента: ").strip()
        if not name:
            print("❌ Имя клиента не может быть пустым!")
            return
            
        phone = input("Телефон: ").strip()
        email = input("Email (необязательно): ").strip()
        address = input("Адрес (необязательно): ").strip()
        
        client = Client(
            name=name,
            phone=phone,
            email=email if email else None,
            address=address if address else None
        )
        client.save()
        print("✅ Клиент успешно добавлен.")
        
    except Exception as e:
        print(f"❌ Ошибка при добавлении клиента: {str(e)}")

def delete_client():
    """Удалить клиента"""
    client_id = input("\nВведите ID клиента для удаления: ")
    
    try:
        client_id = int(client_id)
        client = get_client_by_id(client_id)
        
        if not client:
            print("❌ Клиент с указанным ID не найден!")
            return
            
        confirm = input(f"Вы уверены, что хотите удалить клиента '{client.name}' (ID: {client.id})? [да/нет]: ")
        if confirm.lower() == 'да':
            client.delete()
            print("✅ Клиент успешно удалён.")
        else:
            print("❌ Удаление отменено.")
            
    except ValueError:
        print("❌ Неверный формат ID. Введите числовое значение.")
    except Exception as e:
        print(f"❌ Ошибка при удалении клиента: {str(e)}")

def edit_client():
    """Редактировать клиента"""
    try:
        client_id = int(input("\nВведите ID клиента для редактирования: "))
        current_client = get_client_by_id(client_id)
        
        if not current_client:
            print("❌ Клиент не найден!")
            return
            
        print("\nОставьте поле пустым, чтобы не изменять значение")
        
        name = input(f"Новое имя [{current_client.name}]: ").strip()
        phone = input(f"Новый телефон [{current_client.phone}]: ").strip()
        email = input(f"Новый email [{current_client.email if current_client.email else 'N/A'}]: ").strip()
        address = input(f"Новый адрес [{current_client.address if current_client.address else 'N/A'}]: ").strip()

        updated_client = Client(
            id=client_id,
            name=name if name else current_client.name,
            phone=phone if phone else current_client.phone,
            email=email if email else current_client.email,
            address=address if address else current_client.address
        )
        
        updated_client.save()
        print("✅ Клиент успешно обновлён.")
        
    except ValueError:
        print("❌ Ошибка ввода данных. Проверьте правильность введенных значений.")
    except Exception as e:
        print(f"❌ Ошибка при обновлении клиента: {str(e)}")

if __name__ == "__main__":
    menu_clients()