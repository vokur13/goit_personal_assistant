import asyncio
from transliterate import translit
from faker import Faker

fake = Faker("uk_UA")

name = "Мар'яна"


async def translit_person_name(name):
    name_translit = ""
    for char in translit(name.lower(), "uk", reversed=True):
        if "'" in char:
            name_translit += "_"
            continue
        name_translit += char
    return name_translit


async def person_email(first_n, last_n):
    first_name_translit = await translit_person_name(first_n)
    last_name_translit = await translit_person_name(last_n)
    return f"{first_name_translit}.{last_name_translit}@{fake.free_email_domain()}"


if __name__ == "__main__":
    email = asyncio.run(person_email("Алевтін", "Дерев'янко"))
    print(email)
