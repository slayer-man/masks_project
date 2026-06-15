from tests.mask_test import *
import re

card_number = str("Visa Classic 6831982476737658")

# Найти все цифры
card_number = re.findall(r'\d+', card_number)
print(card_number) # ['1', '2', '3', '4']

# Найти все буквы
letters = re.findall(r'[a-zA-Zа-яА-ЯёЁ]+', card_number)
print(letters) # ['a', 'b', 'c', 'd'])

print(' '.join(letters + card_number))
