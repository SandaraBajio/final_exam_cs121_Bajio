import datetime
from utils.user import User
from utils.score import Score

class UserManager:
    def __init__(self):
        self.users = {}
        self.top_scores = []

    def load_users(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users[username] = password
        except FileNotFoundError:
            with open(filename, 'w') as file:
                pass
    
    def load_top_scores(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    username, points, wins = line.strip().split(',')
                    score = Score(username, int(points), int(wins))
                    self.top_scores.append(score)
        except FileNotFoundError:
            with open(filename, 'w') as file:
                pass

    def save_users(self, filename):
        with open(filename, 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username},{password}\n")

    def save_top_scores(self, filename):
        with open(filename, 'w') as file:
            for score in self.top_scores:
                file.write(f"{score.username},{score.points},{score.wins}\n")

    def validate_username(self, username):
        if len(username) < 4:
            print("Too short.")
            return False
        elif username in self.users:
            print("User already exists. ")
            return False
        return True
            
    def validate_password(self, password):
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
            return False
        return True

    def register(self):
        print("Registration")
        while True:
            username = input("Enter your username(atleast 4 characters) or leave blank to cancel: ")
            if not username:
                print("Registration cancelled.")
                return
            if self.validate_username(username):
                break
        while True:
            password = input("Enter your password(at least 8 characters) or leave to blank to cancel: ")
            if not password:
                print("Registration cancelled.")
                return
            if self.validate_password(password):
                break
            
        self.users[username] = password
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Registration successful at {timestamp}.")
        self.save_users("users.txt")
        
    def login(self):
        while True:
            username = input("Enter username: ")
            password = input("Enter password: ")
            if username in self.users and self.users[username] == password:
                print("Login Successful.")
                return User(username, password)
            else:
                print("Invalid username or password.")

    def exit(self):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Exiting program at {timestamp}")
        exit()
