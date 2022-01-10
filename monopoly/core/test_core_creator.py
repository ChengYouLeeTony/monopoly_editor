from .import_database import *
import django

def test1():
	import_cardsets_to_card_deck("tony")

def test_suite():
	test1()

if __name__ == "__main__":
	django.setup()
	test_suite()