# 0.6.1 new function add_birthday, import upcoming_birthdays() from previous taks

from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        self.name = name


class Phone(Field):
    def __init__(self, number):
        if len(number) != 10 or not number.isdigit():
            raise ValueError("Phone number must be 10 digits.")
        self.number = number


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        self.value = value


class Record:
    def __init__(self, name, *phones, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones]
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.number != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.number == old_phone:
                p.number = new_phone
                break
        else:
            raise ValueError(f"Phone '{old_phone}' not found for contact '{self.name.name}'.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.number == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.name] = record

    def delete_record(self, name):
        del self.data[name]

    def find_record(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def add_phone(self, name, phone):
        record = self.find_record(name)
        if record:
            record.add_phone(phone)
        else:
            raise KeyError(f"Contact '{name}' not found in the address book.")

    def delete_phone(self, name, phone):
        record = self.find_record(name)
        if record:
            record.remove_phone(phone)
        else:
            raise KeyError(f"Contact '{name}' not found in the address book.")

    def change_phone(self, name, old_phone, new_phone):
        record = self.find_record(name)
        if record:
            record.edit_phone(old_phone, new_phone)
        else:
            raise KeyError(f"Contact '{name}' not found in the address book.")

    def add_birthday(self, name, birthday):
        record = self.find_record(name)
        if record:
            record.add_birthday(birthday)
        else:
            raise KeyError(f"Contact '{name}' not found in the address book.")


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            print(f"Input error: {e}")
    return wrapper


@input_error
def add_contact(address_book, name, *numbers):
    record = Record(name, *numbers)
    address_book.add_record(record)
    print(f"Contact '{name}' with number(s) '{', '.join(numbers)}' added successfully.")


@input_error
def change_contact(address_book, name, old_number, new_number):
    address_book.change_phone(name, old_number, new_number)
    print(f"Number for contact '{name}' changed from '{old_number}' to '{new_number}'.")


@input_error
def delete_contact_phone(address_book, name, phone):
    address_book.delete_phone(name, phone)
    print(f"Phone number '{phone}' deleted for contact '{name}'.")


@input_error
def add_contact_phone(address_book, name, phone):
    address_book.add_phone(name, phone)
    print(f"Phone number '{phone}' added for contact '{name}'.")


@input_error
def edit_contact_phone(address_book, name, old_phone, new_phone):
    address_book.change_phone(name, old_phone, new_phone)
    print(f"Phone number for contact '{name}' changed from '{old_phone}' to '{new_phone}'.")


@input_error
def find_contact_phone(address_book, name, phone):
    record = address_book.find_record(name)
    if record:
        phone_obj = record.find_phone(phone)
        if phone_obj:
            print(f"Phone number '{phone}' found for contact '{name}'.")
        else:
            print(f"Phone number '{phone}' not found for contact '{name}'.")
    else:
        print(f"Contact '{name}' not found in the address book.")


@input_error
def show_phone(address_book, name):
    record = address_book.find_record(name)
    if record:
        print(f"The phone number(s) for '{name}' is/are {', '.join([p.number for p in record.phones])}.")
        if record.birthday:
            print(f"The birthday for '{name}' is {record.birthday.value}.")
    else:
        print(f"No phone number found for contact '{name}'.")


@input_error
def show_all_contacts(address_book):
    print("All contacts in the address book:")
    for name, record in address_book.items():
        print(f"{name}: {', '.join([p.number for p in record.phones])}")
        if record.birthday:
            print(f"Birthday: {record.birthday.value}")


@input_error
def add_contact_birthday(address_book, name, birthday):
    address_book.add_birthday(name, birthday)
    print(f"Birthday '{birthday}' added for contact '{name}'.")


def get_upcoming_birthdays(address_book, days=7):
    today = datetime.today().date()
    upcoming_birthdays = []

    for record in address_book.values():
        if record.birthday:
            birthday = record.birthday.date.date()
            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_until_birthday = (birthday_this_year - today).days

            if days_until_birthday <= days:
                weekday = birthday_this_year.weekday()
                if weekday == 5:  # Субота
                    birthday_this_year += timedelta(days=2)
                elif weekday == 6:  # Неділя
                    birthday_this_year += timedelta(days=1)

                upcoming_birthdays.append({
                    "name": record.name.name,
                    "congratulation_date": birthday_this_year.strftime("%Y.%m.%d")
                })

    return upcoming_birthdays


def parse_input(command):
    parts = command.split()
    if parts:
        return parts[0].lower(), parts[1:]
    return "", []


def main():
    print("Welcome to the assistant bot! ver. 0.6.1")
    address_book = AddressBook()
    while True:
        command = input("Enter a command: ").strip()

        if command.lower() in ["close", "exit"]:
            print("Good bye!")
            break

        cmd, args = parse_input(command)

        match cmd:
            case "hello":
                print("How can I help you?")

            case "add":
                if len(args) >= 2:
                    add_contact(address_book, args[0], *args[1:])
                else:
                    print("Invalid number of arguments for 'add' command.")

            case "change":
                if len(args) == 3:
                    change_contact(address_book, args[0], args[1], args[2])
                else:
                    print("Invalid number of arguments for 'change' command.")

            case "delete_phone":
                if len(args) == 2:
                    delete_contact_phone(address_book, args[0], args[1])
                else:
                    print("Invalid number of arguments for 'delete_phone' command.")

            case "add_phone":
                if len(args) == 2:
                    add_contact_phone(address_book, args[0], args[1])
                else:
                    print("Invalid number of arguments for 'add_phone' command.")

            case "edit_phone":
                if len(args) == 3:
                    edit_contact_phone(address_book, args[0], args[1], args[2])
                else:
                    print("Invalid number of arguments for 'edit_phone' command.")

            case "find_phone":
                if len(args) == 2:
                    find_contact_phone(address_book, args[0], args[1])
                else:
                    print("Invalid number of arguments for 'find_phone' command.")

            case "show":
                if len(args) == 1:
                    show_phone(address_book, args[0])
                elif len(args) == 0:
                    show_all_contacts(address_book)
                else:
                    print("Invalid number of arguments for 'show' command.")
                    
            case "add_birthday":
                if len(args) == 2:
                    add_contact_birthday(address_book, args[0], args[1])
                else:
                    print("Invalid number of arguments for 'add_birthday' command.")

            case "upcoming_birthdays":
                upcoming_birthdays = get_upcoming_birthdays(address_book)
                if upcoming_birthdays:
                    print("Upcoming birthdays in the next 7 days:")
                    for birthday in upcoming_birthdays:
                        print(f"{birthday['name']} has a birthday on {birthday['congratulation_date']}")
                else:
                    print("No upcoming birthdays in the next 7 days.")

            case _:
                print("Invalid command. Type again!")


if __name__ == "__main__":
    main()