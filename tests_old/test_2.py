import re

text = "Visa Classic 6831982476737658"

# Найти все цифры
numbers = re.findall(r'\d+', text)
print(numbers) # ['1', '2', '3', '4']

# Найти все буквы
letters = re.findall(r'[a-zA-Zа-яА-ЯёЁ]+', text)
print(letters) # ['a', 'b', 'c', 'd'])

print(' '.join(letters + numbers))
