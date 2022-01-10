from monopoly.models import Cardset, ChanceCard, Map, Land, UserDefineVariable
from .card import Card
from .card_deck import CardDeck
from .board import Board
from .land import Land as LandObject
from .land import ConstructionLand, Infra, StartLand, JailLand, ParkingLand, ChanceLand, UserDefineLand
from .util import *
from .util import Constant

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def import_cardsets_to_card_decks(cardsets):
	"""return card_decks which looks like [cardeck_1, caedect_2,...]"""
	card_decks = []
	
	for i in range(len(cardsets)):
		card_deck = CardDeck()
		one_cardset_cards = ChanceCard.objects.filter(cardset=cardsets[i])
		background_img_url = cardsets[i].background_img_url
		if len(one_cardset_cards) > 0:
			for card in one_cardset_cards:
				title = card.title
				subtitle = card.subtitle
				msg = card.description
				money_addition = card.money_addition
				money_deduction = card.money_deduction
				stop_round = card.stop_round
				money_deduction_when_wrong_answer = card.money_deduction_when_wrong_answer
				variables_change = [card.variable_1_change, card.variable_2_change, card.variable_3_change,
									card.variable_4_change, card.variable_5_change]
				is_multiple_choice = card.is_multiple_choice
				multiple_choice_info = {'multiple_choice_1': card.multiple_choice_1,
										'multiple_choice_2': card.multiple_choice_2,
										'multiple_choice_3': card.multiple_choice_3,
										'multiple_choice_4': card.multiple_choice_4,
										'multiple_choice_answer': card.multiple_choice_answer}
				card_object = Card(title, subtitle, msg, money_addition, money_deduction, stop_round, variables_change, is_multiple_choice, multiple_choice_info, background_img_url, money_deduction_when_wrong_answer)
				card_deck.insert(card_object)
			card_deck.shuffle()
			card_decks.append(card_deck)
		else:
			card_object = Card(title = "這個卡片集沒有卡片喔!", subtitle = "", msg = "", money_addition = "0",
				money_deduction = "0", stop_round=0, variables_change = [""] * NUM_OF_VARIABLES, is_multiple_choice = False, multiple_choice_info= {}, background_img_url = "", money_deduction_when_wrong_answer = 0)
			card_deck.insert(card_object)
			card_decks.append(card_deck)

	return card_decks

def import_map_to_board(map_id):
	_map = Map.objects.get(id = map_id)
	"""import constant"""
	constant = Constant(_map)
	cardsets = _map.cardsets.all().order_by('cardset_name')
	card_decks = import_cardsets_to_card_decks(cardsets)
	lands = Land.objects.filter(_map = _map).order_by('pos')
	board = Board()
	board.clear()
	for land in lands:
		pos = land.pos
		description = land.description
		land_type = land.land_type.land_type
		value = land.value
		additional_parameter = land.additional_parameter
		if land_type == "可建造土地":
			content = ConstructionLand(value, constant)			
		elif land_type == "基礎設施(不可蓋房子)":
			content = Infra(value, constant, additional_parameter)
		elif land_type == "機會":
			content = ChanceLand(value)
		elif land_type == "起點":
			content = StartLand(value)
		elif land_type == "監獄":
			content = JailLand(value)
		elif land_type == "公園":
			content = ParkingLand(value)
		elif land_type == "自訂土地":
			modal_message = land.modal_message.split(';', 2)
			title = ""
			message = ""
			option_tuple = None
			if len(modal_message) == 3:
				title = modal_message[0]
				message = modal_message[1]
				options = modal_message[2].split(',', 2)
				"""expect options look like [後觸發, 確認, 取消]"""
				if len(options) == 2:
					"""trigger variables change before or after confirm"""
					confirm_button_text = options[0].replace('\r','').replace('\n', '').replace('[', '')
					cancel_button_text = options[1].replace('\r','').replace('\n', '').replace(']', '')
					"""(False, "確認", "取消")"""
					option_tuple  = (confirm_button_text, cancel_button_text)
					print("option_tuple")				
					print(option_tuple)				
			elif len(modal_message) == 2:
				title = modal_message[0]
				message = modal_message[1]
			elif len(modal_message) == 1:
				title = "自訂土地"
				message = modal_message[0]
			content = UserDefineLand(value, title, message, option_tuple)
		land_object = LandObject(pos, description, content)
		board.insert(land_object)
	"""import player variable"""
	player_variables_4_list = import_player_variables(_map)
	return board, card_decks, player_variables_4_list, constant

def import_player_variables(_map):
	player_variables_4 = UserDefineVariable.objects.filter(_map=_map)
	player_variables_4_list = []
	for player_variables in player_variables_4:
		player_variable_list = [player_variables.player_name, player_variables.variable_1, player_variables.variable_2, player_variables.variable_3, player_variables.variable_4, player_variables.variable_5]
		player_variables_4_list.append(player_variable_list)
	return player_variables_4_list


