from models.order import Order, get_all_orders, get_order_by_id
from models.clients import get_all_clients, get_client_by_id
from models.product import get_all_products, get_product_by_id
from datetime import datetime

def show_all_orders():
    """Показать все заказы"""
    orders = get_all_orders()
    if not orders:
        print("\nСписок заказов пуст.")
        return
        
    print("\nСписок заказов:")
    for order in orders:
        client = get_client_by_id(order.client_id) if order.client_id else None
        product = get_product_by_id(order.product_id) if order.product_id else None
        print(f"{order.id}. Дата: {order.order_date} | Клиент: {client.name if client else 'N/A'} | "
              f"Товар: {product.name if product else 'N/A'} | Сумма: {order.total_amount} руб. | "
              f"Статус: {order.status}")

def create_new_order():
    """Создание нового заказа"""
    print("\n=== Создание нового заказа ===")
    
    try:
        # Выбор клиента
        clients = get_all_clients()
        if not clients:
            print("❌ Нет доступных клиентов. Сначала создайте клиента.")
            return
            
        print("\nДоступные клиенты:")
        for client in clients:
            print(f"{client.id}. {client.name}")
        client_id = int(input("Введите ID клиента: "))
        
        # Выбор товара
        products = get_all_products()
        if not products:
            print("❌ Нет доступных товаров. Сначала создайте товар.")
            return
            
        print("\nДоступные товары:")
        for product in products:
            print(f"{product.id}. {product.name} (Цена: {product.price} руб.)")
        product_id = int(input("Введите ID товара: "))
        
        quantity = int(input("Количество: "))
        product = get_product_by_id(product_id)
        total_amount = product.price * quantity
        
        order = Order(
            client_id=client_id,
            product_id=product_id,
            order_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_amount=total_amount,
            status="Новый"
        )
        order.save()
        print("✅ Заказ успешно создан.")
        
    except ValueError:
        print("❌ Ошибка ввода данных. Проверьте правильность введенных значений.")

def cancel_order():
    """Отмена заказа"""
    order_id = input("\nВведите ID заказа для отмены: ")
    
    try:
        order_id = int(order_id)
        order = get_order_by_id(order_id)
        
        if not order:
            print("❌ Заказ с указанным ID не найден!")
            return
            
        confirm = input(f"Вы уверены, что хотите отменить заказ #{order.id}? [да/нет]: ")
        if confirm.lower() == 'да':
            order.status = "Отменен"
            order.save()
            print("✅ Заказ успешно отменён.")
        else:
            print("❌ Отмена заказа отменена.")
            
    except ValueError:
        print("❌ Неверный формат ID. Введите числовое значение.")

def edit_order():
    """Редактировать заказ"""
    try:
        order_id = int(input("\nВведите ID заказа для редактирования: "))
        order = get_order_by_id(order_id)
        
        if not order:
            print("❌ Заказ не найден!")
            return
            
        print("\nТекущие данные заказа:")
        client = get_client_by_id(order.client_id)
        product = get_product_by_id(order.product_id)
        print(f"Клиент: {client.name if client else 'N/A'}")
        print(f"Товар: {product.name if product else 'N/A'}")
        print(f"Количество: {order.total_amount / product.price if product else 'N/A'}")
        print(f"Сумма: {order.total_amount} руб.")
        print(f"Статус: {order.status}")
        
        print("\nОставьте поле пустым, чтобы не изменять значение")
        
        # Выбор нового клиента
        print("\nДоступные клиенты:")
        clients = get_all_clients()
        for c in clients:
            print(f"{c.id}. {c.name}")
        new_client_id = input("Введите новый ID клиента: ").strip()
        
        # Выбор нового товара
        print("\nДоступные товары:")
        products = get_all_products()
        for p in products:
            print(f"{p.id}. {p.name} (Цена: {p.price} руб.)")
        new_product_id = input("Введите новый ID товара: ").strip()
        
        new_quantity = input("Новое количество: ").strip()
        new_status = input("Новый статус: ").strip()
        
        # Обновление данных
        if new_client_id:
            order.client_id = int(new_client_id)
        if new_product_id:
            order.product_id = int(new_product_id)
            product = get_product_by_id(order.product_id)
        if new_quantity:
            quantity = int(new_quantity)
            order.total_amount = product.price * quantity
        if new_status:
            order.status = new_status
        
        order.save()
        print("✅ Заказ успешно обновлён.")
        
    except ValueError:
        print("❌ Ошибка ввода данных. Проверьте правильность введенных значений.")

def show_order_details():
    """Показать детали заказа"""
    try:
        order_id = int(input("\nВведите ID заказа для просмотра: "))
        order = get_order_by_id(order_id)
        
        if not order:
            print("❌ Заказ не найден!")
            return
            
        client = get_client_by_id(order.client_id)
        product = get_product_by_id(order.product_id)
        
        print("\n=== Детали заказа ===")
        print(f"ID заказа: {order.id}")
        print(f"Дата создания: {order.order_date}")
        print(f"Клиент: {client.name if client else 'N/A'}")
        print(f"Телефон клиента: {client.phone if client else 'N/A'}")
        print(f"Товар: {product.name if product else 'N/A'}")
        print(f"Цена за единицу: {product.price if product else 'N/A'} руб.")
        print(f"Количество: {order.total_amount / product.price if product else 'N/A'}")
        print(f"Общая сумма: {order.total_amount} руб.")
        print(f"Статус: {order.status}")
        
    except ValueError:
        print("❌ Неверный формат ID. Введите числовое значение.")

def menu_orders():
    while True:
        print("\n=== Управление заказами ===")
        print("1. Показать все заказы")
        print("2. Создать новый заказ")
        print("3. Отменить заказ")
        print("4. Изменить заказ")
        print("5. Показать детали заказа")
        print("0. Назад в главное меню")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            show_all_orders()
        elif choice == "2":
            create_new_order()
        elif choice == "3":
            cancel_order()
        elif choice == "4":
            edit_order()
        elif choice == "5":
            show_order_details()
        elif choice == "0":
            break
        else:
            print("❌ Неверный ввод. Пожалуйста, выберите действие из меню.")

if __name__ == "__main__":
    menu_orders()