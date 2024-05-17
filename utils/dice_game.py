import os
import random
import datetime
import time
from utils.score import Score

class DiceGame:
    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.current_user = None
        self.top_scores = []
        self.stage_won = False

    def menu(self):
        while True:
            self.loading("Loading Menu")
            os.system('cls' if os.name == 'nt' else 'clear')
            if self.current_user:
                print(f"\n=== Welcome to the Dice Game, {self.current_user.username} ===")
            else:
                print("\n=== Welcome to the Dice Game ===")
            print("1. Start Game")
            print("2. View Top Scores")
            print("3. Log out")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.start_game()
            elif choice == "2":
                self.display_top_scores()
            elif choice == "3":
                self.current_user = None
                print("Logged out successfully.")
                break
            else:
                print("Invalid choice. Please choose again.")

    def start_game(self):
        if not self.current_user:
            print("Error: No user logged in.")
            return
        self.loading("Starting Game")
        print("\n=== Game Started ===")
        start_time = datetime.datetime.now()
        print(f"Game started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.current_user.points = 0
        self.current_user.stages_won = 0
        self.stage_won = False  # Reset stage_won for each game
        time.sleep(1)  # Adding delay for suspense
        while True:
            stage_result = self.play_stage()
            if stage_result == "lost":
                if not self.stage_won:
                    print("Game over. You didn’t win any stages.")
                else:
                    print(f"Stage lost. Total points: {self.current_user.points}, Stages won: {self.current_user.stages_won}")
                if self.stage_won:  # Record score only if not first stage and stage was won previously
                    self.record_score()
                break
            elif stage_result == "won":
                self.stage_won = True
                print(f"Stage won! Total points: {self.current_user.points}")
                time.sleep(1)  # Adding delay for suspense
                continue_game = input("Do you want to continue to the next stage? (1: Yes, 0: No): ")
                if continue_game == "1":
                    continue
                elif continue_game == "0":
                    self.record_score()
                    break
                else:
                    print("Invalid input. Ending game.")
                    self.record_score()
                    break

        end_time = datetime.datetime.now()
        duration = end_time - start_time
        print(f"Game ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total game duration: {duration}")
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        self.menu()

    def play_stage(self):
        player_wins = 0
        computer_wins = 0
        while player_wins < 2 and computer_wins < 2:
            self.loading("Playing Stage")
            player_roll = random.randint(1, 6)
            computer_roll = random.randint(1, 6)
            self.display_dice(player_roll, "You")
            self.display_dice(computer_roll, "CPU")
            time.sleep(1)  # Adding delay for suspense
            if player_roll > computer_roll:
                player_wins += 1
                if not self.stage_won:  # If not the first stage, only add points if previous stage was won
                    self.current_user.points += 1
                print("You win this round!")
            elif player_roll < computer_roll:
                computer_wins += 1
                print("CPU wins this round!")
            else:
                print("It's a tie! No points awarded.")
        
        if player_wins == 2:
            self.current_user.stages_won += 1
            self.current_user.points += 3
            return "won"
        else:
            return "lost"

    def display_top_scores(self):
        self.loading("Loading Top Scores")
        if not self.user_manager.top_scores:  # Check if top_scores list is empty
            print("No scores available yet.")
            return
        print("\nTop-10 Highest Scores:")
        for score in self.user_manager.top_scores:  # Iterate over user_manager's top_scores
            print(f"Username: {score.username}, Points: {score.points}, Stages Won: {score.wins}")
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        self.menu()

    def record_score(self):
        self.loading("Recording Score")
        if self.current_user and self.current_user.stages_won > 0:  # Record score only if at least one stage was won
            new_score = Score(self.current_user.username, self.current_user.points, self.current_user.stages_won)
            self.user_manager.top_scores.append(new_score)
            self.user_manager.top_scores.sort(key=lambda x: x.points, reverse=True)
            if len(self.user_manager.top_scores) > 10:
                self.user_manager.top_scores = self.user_manager.top_scores[:10]
            self.user_manager.save_top_scores("top_scores.txt")  # Save the updated top scores to file

    def loading(self, message):
        print(f"{message} ", end='', flush=True)
        for _ in range(3):
            print(".", end='', flush=True)
            time.sleep(0.5)

    def display_dice(self, roll, player):
        # Define the ASCII art representations of dice faces with color
        dice_faces = [
            ['\033[37m ------- \033[0m',
             '\033[37m|       |\033[0m',
             '\033[37m|   \033[31mo   \033[37m|\033[0m',
             '\033[37m|       |\033[0m',
             '\033[37m ------- \033[0m'],

            ['\033[37m ------- \033[0m',
             '\033[37m| \033[31mo     \033[37m|\033[0m',
             '\033[37m|       |\033[0m',
             '\033[37m|     \033[31mo \033[37m|\033[0m',
             '\033[37m ------- \033[0m'],

            ['\033[37m ------- \033[0m',
             '\033[37m| \033[31mo     \033[37m|\033[0m',
             '\033[37m|   \033[31mo   \033[37m|\033[0m',
             '\033[37m|     \033[31mo \033[37m|\033[0m',
             '\033[37m ------- \033[0m'],

            ['\033[37m ------- \033[0m',
             '\033[37m| \033[31mo   \033[31mo \033[37m|\033[0m',
             '\033[37m|       |\033[0m',
             '\033[37m| \033[31mo   \033[31mo \033[37m|\033[0m',
             '\033[37m ------- \033[0m'],

            ['\033[37m ------- \033[0m',
             '\033[37m| \033[31mo   \033[31mo \033[37m|\033[0m',
             '\033[37m|   \033[31mo   \033[37m|\033[0m',
             '\033[37m| \033[31mo   \033[31mo \033[37m|\033[0m',
             '\033[37m ------- \033[0m'],

            ['\033[37m ------- \033[0m',
             '\033[37m| \033[31mo   \033[31mo \033[37m|\033[0m',
             '\033[37m| \033[31mo   \033[31mo \033[37m|\033[0m',
             '\033[37m| \033[31mo   \033[31mo \033[37m|\033[0m',
             '\033[37m ------- \033[0m']
        ]

        # Print the player's name and corresponding dice face with color
        print(f"\n{player} rolled:")
        for line in dice_faces[roll - 1]:
            print(line)


