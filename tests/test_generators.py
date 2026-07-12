def test_filter_by_currency():
    pass


def test_transaction_descriptions():
    pass


def test_card_number_generator():
    pass


empty_data = []
descriptions = list(transaction_descriptions(empty_data))
assert len(descriptions) == 0