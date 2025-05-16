from models.product import Product, get_all_products
from models.category import get_all_categories, get_category_by_id

def menu_products():
    while True:
        print("\n=== 💍Управление товарами💍 ===")
        print("1. Показать все товары")
        print("2. Добавить товар")
        print("3. Удалить товар")
        print("4. Изменить товар")
        print("0. Назад в главное меню")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            show_all_products()
            
        elif choice == "2":
            add_new_product()
            
        elif choice == "3":
            delete_product()
            
        elif choice == "4":
            edit_product()
            
        elif choice == "0":
            break
            
        else:
            print("❌ Неверный ввод. Пожалуйста, выберите действие из меню.")

def show_all_products():
    """Показать все товары"""
    products = get_all_products()
    if not products:
        print("\nСписок товаров пуст.")
        return
        
    print("\nСписок товаров:")
    for p in products:
        category = get_category_by_id(p.category_id) if hasattr(p, 'category_id') else None
        
        
        print(f"{p.id}. {p.name} | Размер: {p.size} | Цена: {p.price} руб. | "
              f"В наличии: {p.stock} | Категория: {category.name if category else 'N/A'} | "
            )

def add_new_product():
    """Добавить новый товар"""
    print("\n=== Добавление нового товара ===")
    
    try:
        name = input("Название товара: ").strip()
        if not name:
            print("❌ Название товара не может быть пустым!")
            return
            
        size = float(input("Размер: "))
        price = float(input("Цена: "))
        stock = int(input("Количество на складе: "))

        # Выбор категории
        print("\nДоступные категории:")
        categories = get_all_categories()
        if not categories:
            print("❌ Нет доступных категорий. Сначала создайте категорию.")
            return
            
        for c in categories:
            print(f"{c.id} - {c.name}")
            
        category_id = int(input("Введите ID категории: "))
        if not any(c.id == category_id for c in categories):
            print("❌ Указана несуществующая категория!")
            return

      
            
        

        product = Product(
            name=name,
            size=size,
            price=price,
            stock=stock,
            category_id=category_id,
          
        )
        product.save()
        print("✅ Товар успешно добавлен.")
        
    except ValueError:
        print("❌ Ошибка ввода данных. Проверьте правильность введенных значений.")

def delete_product():
    """Удаление товара"""
    product_id = input("\nВведите ID товара для удаления: ")
    
    try:
        product_id = int(product_id)
        product = next((p for p in get_all_products() if p.id == product_id), None)
        
        if not product:
            print("❌ Товар с указанным ID не найден")
            return
            
        confirm = input(f"Вы уверены, что хотите удалить товар '{product.name}' (ID: {product.id})? [да/нет]: ")
        if confirm.lower() == 'да':
            product.delete()
            print("✅ Товар успешно удалён.")
        else:
            print("❌ Удаление отменено.")
            
    except ValueError:
        print("❌ Неверный формат ID. Введите числовое значение.")

def edit_product():
    """Редактирование товара"""
    try:
        product_id = int(input("\nВведите ID товара для редактирования: "))
        current_product = next((p for p in get_all_products() if p.id == product_id), None)
        
        if not current_product:
            print("❌ Товар не найден!")
            return
            
        print("\nОставьте поле пустым, чтобы не изменять значение")
        
        # Основные данные
        name = input(f"Новое название [{current_product.name}]: ").strip()
        size = input(f"Новый размер [{current_product.size}]: ")
        price = input(f"Новая цена [{current_product.price}]: ")
        stock = input(f"Новое количество на складе [{current_product.stock}]: ")

        # Категория
        current_category = get_category_by_id(current_product.category_id) if hasattr(current_product, 'category_id') else None
        print(f"\nТекущая категория: {current_category.name if current_category else 'N/A'}")
        print("Доступные категории:")
        categories = get_all_categories()
        for c in categories:
            print(f"{c.id} - {c.name}")
        category_id = input("Введите новый ID категории (оставьте пустым, чтобы не менять): ")

       

        # Проверка ввода
        if category_id and not any(c.id == int(category_id) for c in categories):
            print("❌ Указана несуществующая категория!")
            return
            
       

        # Создаем обновленный товар
        updated_product = Product(
            id=product_id,
            name=name if name else current_product.name,
            size=float(size) if size else current_product.size,
            price=float(price) if price else current_product.price,
            stock=int(stock) if stock else current_product.stock,
            category_id=int(category_id) if category_id else current_product.category_id,
           
        )
        
        updated_product.save()
        print("✅ Товар успешно обновлён.")
        
    except ValueError:
        print("❌ Ошибка ввода данных. Проверьте правильность введенных значений.")
        