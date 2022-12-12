from collections import UserDict
from datetime import datetime, timedelta
import pickle

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
 

class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if not value.isnumeric():
            raise ValueError("The phone number must consist of numbers only ")
        self._value = value

class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        try: 
            self._value = datetime.strptime(value, "%d.%m.%Y")
        except:
            raise ValueError("Enter the date in the form dd.mm.yyyy")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.b_day = None
        
    def add_phones(self, phone):
        self.phones.append(Phone(phone))

    def get_phones_str(self):
        phone_str = []
        for phone in self.phones:
            phone_str.append(phone.value)
        return phone_str

    def get_phones(self):
        return ", ".join(self.get_phones_str())
         
    def delete_phone(self, phone):
        for remove_phone in self.phones:
            if phone == remove_phone.value:
                self.phones.remove(remove_phone)

    def find_phone(self, phones):
        for phone in phones: 
            if phone not in self.get_phones_str():
                return False
        return True
    
    def add_birth_day(self, b_day):
        self.b_day = Birthday(b_day)
    
    def days_to_birthday(self):
        now_day = datetime.now()
        days_for_b_day = (self.b_day.value - now_day).days
        if days_for_b_day < 0:
            nextb_day = datetime(year = now_day.year + 1, month=self.b_day.value.month, day = self.b_day.value.day)
            return (nextb_day - now_day).days
        else: 
            return days_for_b_day

    
       

class AddressBook(UserDict):
    def __init__(self, file_name = "adress_book"):
        super().__init__()
        self.file_name = f"{file_name}.bin"
        self.read_contact_from_file()
        
                
    def add_record(self, record):
        self.data[record.name.value] = record
        
    def show_all_book(self):
        return self.data
        
    def delete_record(self, name):
        del self.data[name]

    def __iter__(self):
        for key, value in self.data.items():
            yield key, value
            
    def iterator(self, count):
        for key, value in self:
            i = 1
            page = {}
            while i <= count:
                page[key] = value
                i += 1
            yield page
            
    def read_contact_from_file(self):
        try:
            with open(self.file_name, "rb") as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            print ("Adress book not found. A new address book is created")
        except EOFError:
            pass   
        
    def push_to_file(self):
        with open(self.file_name, "wb") as fh:
            pickle.dump(self.data, fh)
            
    def find_info(self, line_to_find):
        find_result = []
        for key, value in self.data.items():
            if line_to_find in key:
                find_result.append(f"Name contact is {key}")
            for phone in value.get_phones_str():
                if line_to_find in phone:
                    find_result.append(f"contact {key} has this {phone} phone")
        return find_result
        
            
            
    
        