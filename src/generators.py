import itertools

def card_number_generator(prefix, length=16):
    """ Генератор номеров карт. prefix - первые цифры в виде строки length - общая длина номера карты"""
    zeros_count = length - len(prefix)
    # Задаем начальное значение последних цифр (.count())
    for counter in itertools.count(1):
        counter_str = f"{counter:0{zeros_count}d}"
        card_number = ''.join(prefix + counter_str)
        card_num = ' '.join([card_number[i:i+4] for i in range(0, len(card_number), 4)])
        yield card_num


# Создаем генератор номеров, всего 16 цифр (prefix - задает начальные цифры(до 14 цифр))
card = card_number_generator(prefix="", length=16)
# Вывод n - номеров.
for _ in range(5):
    print(next(card))
