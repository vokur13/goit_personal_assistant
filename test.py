from faker import Faker
from transliterate import translit
from phonenumber_field.phonenumber import PhoneNumber

fake = Faker("uk_UA")


first_name = fake.first_name()
print(first_name)
last_name = fake.last_name()
print(last_name)


def translit_person_name(name):
    name_translit = ""
    for char in translit(name.lower(), "uk", reversed=True):
        if "'" in char:
            continue
        name_translit += char
    return name_translit


def person_email(first_n, last_n):
    first_name_translit = translit_person_name(first_n)
    last_name_translit = translit_person_name(last_n)
    return f"{first_name_translit}.{last_name_translit}@{fake.free_email_domain()}"


email = person_email(first_name, last_name)
print(email)

print(fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=65))

print(fake.text(max_nb_chars=100))

number = f"+380{fake.msisdn()[4:]}"
number = PhoneNumber.from_string(number, region="UA")
print(number.as_e164)
address = fake.address()
print(address)
