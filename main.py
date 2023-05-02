import json
import random
import time
import os
import codecs

PHRASES_FILE = "phrases.txt"
USERS_FILE = "users.json"
STATS_FILE = "stats.json"


def load_phrases():
    with open(PHRASES_FILE, "r", encoding="utf-8") as f:
        phrases = [line.strip() for line in f.readlines()]
    return phrases


def encrypt_phrase(phrase):
    return codecs.encode(phrase, "rot13")


def decrypt_phrase(encrypted_phrase):
    return codecs.decode(encrypted_phrase, "rot13")


def add_user(login, password, encrypted_phrase, avg_time):
    if not os.path.isfile(USERS_FILE):
        # Создаем новый файл и записываем в него первого пользователя
        with open(USERS_FILE, "w") as f:
            users = {login: {"password": password, "encrypted_phrase": encrypted_phrase, "avg_time": avg_time}}
            json.dump(users, f)
    else:
        # Если файл уже существует, то загружаем данные и добавляем нового пользователя
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        users[login] = {"password": password, "encrypted_phrase": encrypted_phrase, "avg_time": avg_time}
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)


def register_user():
    print("Welcome to the registration page!")
    login = input("Enter your login: ")
    password = input("Enter your password: ")
    phrases = load_phrases()
    phrase = random.choice(phrases)
    encrypted_phrase = encrypt_phrase(phrase)
    print(f"Please type the following phrase at least 4 times: {decrypt_phrase(encrypted_phrase)}")
    times = []
    for i in range(4):
        start_time = time.time()
        typed_phrase = input("Type the phrase: ")
        end_time = time.time()
        time_taken = end_time - start_time
        times.append(time_taken)
        if typed_phrase != phrase:
            print("Incorrect phrase. Please try again.")
            return
    avg_time = sum(times) / len(times)
    add_user(login, password, encrypted_phrase, avg_time)
    # with open(USERS_FILE, "r") as f:
    #     users = json.load(f)
    # users[login] = {"password": password, "encrypted_phrase": encrypted_phrase, "avg_time": avg_time}
    # with open(USERS_FILE, "w") as f:
    #     json.dump(users, f)
    print("Registration complete!")


def authenticate_user():
    print("Welcome to the login page!")
    login = input("Enter your login: ")
    password = input("Enter your password: ")
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    if login not in users or users[login]["password"] != password:
        print("Invalid login or password. Please try again.")
        return
    encrypted_phrase = users[login]["encrypted_phrase"]
    phrase = decrypt_phrase(encrypted_phrase)
    print(f"Please type the following phrase: {phrase}")
    times = []
    for i in range(4):
        start_time = time.time()
        typed_phrase = input("Type the phrase: ")
        end_time = time.time()
        time_taken = end_time - start_time
        times.append(time_taken)
        if typed_phrase != phrase:
            print("Incorrect phrase. Please try again.")
            return
    avg_time = sum(times) / len(times)
    if abs(avg_time - users[login]["avg_time"]) < 0.5:
        print("Authentication successful!")
        with open(STATS_FILE, "a") as f:
            f.write(f"{login}: {avg_time}\n")
    else:
        print("Authentication failed. Please try again.")


def main():
    while True:
        choice = input("Enter 'r' for registration, 'l' for login, or 'q' to quit: ")
        if choice == "r":
            register_user()
        elif choice == "l":
            authenticate_user()
        elif choice == "q":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
