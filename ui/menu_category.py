from models.category import Category, get_all_categories, get_category_by_id

def menu_categories():
    while True:
        print("\n=== 💍Управление категориями💍 ===")
        print("1. Показать все категории")
        print("2. Добавить категорию")
        print("3. Удалить категорию")
        print("4. Изменить категорию")
        print("0. Назад в главное меню")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            show_all_categories()
        elif choice == "2":
            add_new_category()
        elif choice == "3":
            delete_category()
        elif choice == "4":
            edit_category()
        elif choice == "0":
            break
        else:
            print("❌ Неверный ввод. Пожалуйста, выберите действие из меню.")

def show_all_categories():
    """Показать все категории"""
    categories = get_all_categories()
    if not categories:
        print("\nСписок категорий пуст.")
        return
        
    print("\nСписок категорий:")
    for c in categories:
        print(f"{c.id}. {c.name} | Описание: {c.description if c.description else 'нет'}")

def add_new_category():
    """Добавить новую категорию"""
    print("\n=== Добавление новой категории ===")
    
    try:
        name = input("Название категории: ").strip()
        if not name:
            print("❌ Название категории не может быть пустым!")
            return
            
        description = input("Описание (необязательно): ").strip()
        
        category = Category(
            name=name,
            description=description if description else None
        )
        category.save()
        print("✅ Категория успешно добавлена.")
        
    except Exception as e:
        print(f"❌ Ошибка при добавлении категории: {str(e)}")

def delete_category():
    """Удалить категорию"""
    category_id = input("\nВведите ID категории для удаления: ")
    
    try:
        category_id = int(category_id)
        category = get_category_by_id(category_id)
        
        if not category:
            print("❌ Категория с указанным ID не найдена!")
            return
            
        confirm = input(f"Вы уверены, что хотите удалить категорию '{category.name}' (ID: {category.id})? [да/нет]: ")
        if confirm.lower() == 'да':
            category.delete()
            print("✅ Категория успешно удалена.")
        else:
            print("❌ Удаление отменено.")
            
    except ValueError:
        print("❌ Неверный формат ID. Введите числовое значение.")
    except Exception as e:
        print(f"❌ Ошибка при удалении категории: {str(e)}")

def edit_category():
    """Редактировать категорию"""
    try:
        category_id = int(input("\nВведите ID категории для редактирования: "))
        current_category = get_category_by_id(category_id)
        
        if not current_category:
            print("❌ Категория не найдена!")
            return
            
        print("\nОставьте поле пустым, чтобы не изменять значение")
        
        name = input(f"Новое название [{current_category.name}]: ").strip()
        description = input(f"Новое описание [{current_category.description if current_category.description else 'нет'}]: ").strip()

        updated_category = Category(
            id=category_id,
            name=name if name else current_category.name,
            description=description if description else current_category.description
        )
        
        updated_category.save()
        print("✅ Категория успешно обновлена.")
        
    except ValueError:
        print("❌ Ошибка ввода данных. Проверьте правильность введенных значений.")
    except Exception as e:
        print(f"❌ Ошибка при обновлении категории: {str(e)}")

if __name__ == "__main__":
    menu_categories()