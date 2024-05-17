from utils.user_manager import UserManager
from utils.dice_game import DiceGame

def main():
    user_system = UserManager()
    user_system.load_users("users.txt")
    user_system.load_top_scores("top_scores.txt")  # Load top scores when the program starts

    while True:
        try: 
            print("\n1. Register\n2. Log in\n3. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                user_system.register()
            elif choice == "2":
                logged_in_user = user_system.login()
                if logged_in_user:
                    game = DiceGame(user_system)
                    game.current_user = logged_in_user
                    game.menu()
            elif choice == "3":
                user_system.exit()  # Save top scores before exiting
            else:
                print("Invalid choice. Please choose again.")
        except Exception as e:
            print(f'Error: {e}')

if __name__ == "__main__":
    main()
