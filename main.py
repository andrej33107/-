from database.db_manager import initialize_db
from ui.menu import show_main_menu
from ui.menu_products import menu_products
from ui.menu_clients import menu_clients
from ui.menu_orders import menu_orders
from ui.menu_category import menu_categories
#from ui.menu_materials import menu_materials

def main():
    try:
        # Инициализация базы данных
        initialize_db()
        
        # Основной цикл программы
        while True:
            user_choice = show_main_menu()
            
            if user_choice == "1":
                menu_products()
            elif user_choice == "2":
                menu_categories()
            elif user_choice == "3":
                menu_clients()
            elif user_choice == "4":
                menu_orders()
            elif user_choice == "0":
                print("\nВыход из программы. До свидания!")
                break
            else:
                print("\n❌ Неверный ввод. Пожалуйста, выберите пункт из меню.")
                
    except Exception as e:
        print(f"\n⚠️ Произошла ошибка: {str(e)}")
        print("Пожалуйста, сообщите об этом администратору системы.")

if __name__ == "__main__":
    main()