from monopoly.models import Map

NUM_OF_VARIABLES = 5

class Constant(object):
	def __init__(self, _map):
		basic_setting = _map.basicsetting
		self.INIT_PLAYER_MONEY = basic_setting.money_initial
		self.MONEY_PASS_START = basic_setting.money_pass_start
		self.HOUSE_CONSTRUCTION_COST = basic_setting.house_construction_cost
		self.NUM_OF_HOUSE_EQUAL_HOTEL = basic_setting.num_of_house_equal_hotel
		self.RATIO_RENT_VS_PRICE = basic_setting.ratio_rent_vs_price
		self.RATIO_RENT_VS_PRICE_FOR_HOUSE = basic_setting.ratio_rent_vs_price_for_house
		self.RENT_CONSTANT = basic_setting.rent_constant
		self.RATIO_RENT_VS_PRICE_INFRA = basic_setting.ratio_rent_vs_price_infra
		self.RATIO_RENT_VS_PRICE_INFRA_FOR_SAME_CATEGORY = basic_setting.ratio_rent_vs_price_infra_for_same_category
		self.RENT_CONSTANT_INFRA = basic_setting.rent_constant_infra
