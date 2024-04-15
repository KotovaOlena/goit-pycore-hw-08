from collections import UserDict
from datetime import datetime
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if str(p) == old_phone:
                p.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return str(p)
        return None

    def add_birthday(self, birthday):
        if isinstance(birthday, Birthday):
            self.birthday = birthday
        else:
            raise ValueError("Invalid birthday format. Use Birthday object.")

    def __str__(self):
        return f"Contact name: {self.name}, phones: {', '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


def get_upcoming_birthdays(address_book):
    upcoming_birthdays = []
    today = datetime.now().date()
    for record in address_book.values():
        if record.birthday:
            if (record.birthday.value.date() - today).days in range(1, 8):
                upcoming_birthdays.append(record)
    return upcoming_birthdays


class AddressBookBot:
    def __init__(self):
        self.book = AddressBook()

    def add_record(self, name, phone):
        if name in self.book:
            self.book[name].add_phone(phone)
        else:
            record = Record(name)
            record.add_phone(phone)
            self.book.add_record(record)

    def change_phone(self, name, new_phone):
        if name in self.book:
            self.book[name].edit_phone(new_phone)

    def get_phone(self, name):
        if name in self.book:
            return self.book[name]

    def show_all_records(self):
        return self.book.data

    def add_birthday(self, name, birthday):
        if name in self.book:
            self.book[name].add_birthday(birthday)
        else:
            raise ValueError("Contact not found.")

    def show_birthday(self, name):
        if name in self.book:
            return self.book[name].birthday
        else:
            raise ValueError("Contact not found.")

    def show_upcoming_birthdays(self):
        upcoming_birthdays = get_upcoming_birthdays(self.book)
        return [record.name for record in upcoming_birthdays]


def parse_input(user_input):
    return user_input.split()


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def main():
    book = load_data()

    bot = AddressBookBot()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            return

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            if len(args) != 2:
                print("Invalid number of arguments. Usage: add [name] [phone]")
            else:
                bot.add_record(args[0], args[1])
                print("Contact added successfully.")

        elif command == "change":
            if len(args) != 2:
                print("Invalid number of arguments. Usage: change [name] [new_phone]")
            else:
                bot.change_phone(args[0], args[1])
                print("Phone number changed successfully.")

        elif command == "phone":
            if len(args) != 1:
                print("Invalid number of arguments. Usage: phone [name]")
            else:
                phone = bot.get_phone(args[0])
                if phone:
                    print(f"The phone number for {args[0]} is {phone}.")
                else:
                    print("Contact not found.")

        elif command == "all":
            print("All contacts:")
            for name, record in bot.show_all_records().items():
                print(f"{name}: {record}")

        elif command == "add-birthday":
            if len(args) != 2:
                print("Invalid number of arguments. Usage: add-birthday [name] [DD.MM.YYYY]")
            else:
                try:
                    birthday = Birthday(args[1])
                    bot.add_birthday(args[0], birthday)
                    print("Birthday added successfully.")
                except ValueError as e:
                    print(e)

        elif command == "show-birthday":
            if len(args) != 1:
                print("Invalid number of arguments. Usage: show-birthday [name]")
            else:
                try:
                    birthday = bot.show_birthday(args[0])
                    if birthday:
                        print(f"The birthday for {args[0]} is {birthday}.")
                    else:
                        print("No birthday found.")
                except ValueError as e:
                    print(e)

        elif command == "birthdays":
            print("Upcoming birthdays for the next week:")
            upcoming_birthdays = bot.show_upcoming_birthdays()
            if upcoming_birthdays:
                for name in upcoming_birthdays:
                    print(name)
            else:
                print("No upcoming birthdays.")

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
