from core import AddressBook, Record


contacts_book = AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return "Input Error. Please enter command"
        except SyntaxError as exception:   
            return exception.args[0]
        except TypeError:
            return "Input Error. Please enter command."     
    return inner


def find_comand(user_comand):    
    comand = user_comand
    record = ""
    for key in COMANDS:
        if user_comand.lower().strip().startswith(key):
            comand = key
            record = user_comand[len(key):]
            break
    if record:
        return made_func(comand)(record)
    return made_func(comand)()


def made_func(func):
    return COMANDS.get(func, unknown_func)

def show_all_phone():
    contacts_list = "|{:^10}| {:<}".format("Name", "Phone")
    for contact, phone in contacts_book.show_all_book().items():
        contacts_list += "\n|{:^10}| {:<}".format(contact, phone.get_phones())
    return   contacts_list


def show_page(n):
    page_n = 1
    contacts_list = "|{:^10}| {:<}".format("Name", "Phone")
    for page in contacts_book.iterator(int(n)):
        contacts_list += f"\nPage # {page_n}"
        for contact, phone in page.items():
            contacts_list += "\n|{:^10}| {:<}".format(contact, phone.get_phones())
        page_n += 1
    return contacts_list


def sey_hello():
    return "How can I help you?"


def sey_bye():
    return "Good bye!" 


def unknown_func():
    return "I don't understand what you want. Please enter the correct command"


def create_data(contact_line):
    contact_line = contact_line.strip().split(" ")
    name, phones = contact_line[0], contact_line[1:]
    name = name.title()
    return name, phones


@input_error
def show_phone(name):
    name, *_ = create_data(name)
    if name in contacts_book:
        return "|{:^10}|{:<}".format("Name", "Phone") +"\n|{:^10}|{:<}".format(name, contacts_book[name].get_phones())
    raise ValueError("This name is not in the phone book. Please enter the correct name.")


@input_error
def add_phone(phone_line):
    name, phones = create_data(phone_line)
    if name in contacts_book:
        raise ValueError ("This contact is already in the phone book. Please enter the correct name.")
    elif  not name or not phones:
        raise SyntaxError ("You entered an incorrect phone number or name")
    else:
        record = Record(name)
        
        for phone in phones:
            record.add_phones(phone) 
            
        contacts_book.add_record(record)
        return f"{name}'s phone added to the phone book."

    
#Функція додає новий телефон до вже існуючого контакту
@input_error
def add_new_phone(phone_line):
    name, phones = create_data(phone_line)
    if name not in contacts_book:
        raise ValueError ("This contact is not in the phone book. Please enter the correct name.")    
    for phone in phones:
        contacts_book[name].add_phones(phone)
    return f"{name}'s phones are appdate"


#Функція яка додає до контакту день народження
@input_error
def birth_day(data):
    name, b_day = create_data(data)
    if name not in contacts_book:
        raise ValueError ("This contact is not in the phone book. Please enter the correct name.")    
    contacts_book[name].add_birth_day(b_day[0])
    return f"{name}'s birth day added."


#Функція вказує кількість днів до наступнго Дня народження
@input_error
def birthday_func(data):
    name, *_ = create_data(data)
    if contacts_book[name].b_day :
        return f"{name}'s birthday is {contacts_book[name].days_to_birthday()} days away "
    else: 
        raise ValueError(f"I don't know when {name}'s birthday")


#Функція пошуку всіх збігів у контактній книзі
@input_error
def find_func(data):
    line_for_find, *_= create_data(data)
    find_line = contacts_book.find_info(line_for_find)
    if not find_line:
        return f"I can't find {line_for_find} in adress book"
    else:
        result = ""
        for line in find_line:
            result += line + "\n"
    return result[:-1]


@input_error
def delete_phone(phone_line):
    name, phones = create_data(phone_line)
    if name not in contacts_book:
        raise ValueError ("This contact is not in the phone book. Please enter the correct name.")
    if not contacts_book[name].find_phone(phones):
        raise ValueError ("This phone is not in the phone book. Please enter the correct phone.")
    for phone in phones:
        contacts_book[name].delete_phone(phone)
    return f"{name}'s phone delete"


def delete_contact(name):
    name, *_ = create_data(name)
    if name in contacts_book:
        contacts_book.delete_record(name)
        return f"{name}'s contact has been deleted"


@input_error
def change_phone(phone_line):
    name, phones = create_data(phone_line)
    if name in contacts_book: 
        if len(phones) != 2:
            raise ValueError ("Input Error. Enter correct information")
        if phones[0] not in contacts_book[name].get_phones_str() and phones[1] not in contacts_book[name].get_phones_str():
            raise ValueError ("Unknown number. Check the correctness of the input")
        if phones[0] in contacts_book[name].get_phones_str():
            new_phone, old_phone = phones[1], phones[0]
        else: 
            new_phone, old_phone = phones[0], phones[1]
        contacts_book[name].delete_phone(old_phone)
        contacts_book[name].add_phones(new_phone)
        return f"{name}'s phone number has been changed"
    else:
        raise ValueError ("This contact is not in the phone book. Please enter the correct name.")


COMANDS = {
        "hello": sey_hello,
        "add contact" : add_phone,
        "new phone" : add_new_phone,
        "change" : change_phone,
        "phone" : show_phone,
        "show all": show_all_phone,
        "good bye": sey_bye, 
        "close": sey_bye,
        "end": sey_bye,
        "delete phone": delete_phone, 
        "delete contact" : delete_contact, 
        "add birthday" : birth_day,
        "next birthday" : birthday_func,
        "show by pages": show_page,
        "find" : find_func
        }

            
def main():
    while True:
        user_comand = input("... ")
        result = find_comand(user_comand)
        print(result)
        if result == "Good bye!":
            contacts_book.push_to_file()
            break


if __name__ == '__main__':
    main()