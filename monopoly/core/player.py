from .building import Building
from .util import *
from .land import LandType


class Player(object):
    # _money = 0
    # _index = 0
    # _remaining_stop = 0
    # _properties = set()
    # _position = 0

    def __init__(self, index, player_name="", variable_1=0, variable_2=0, variable_3=0, variable_4=0, variable_5=0, constant=None, is_turn_over = "false"):
        self._index = index
        self._money = constant.INIT_PLAYER_MONEY
        self._position = 0
        self._remaining_stop = 0
        self._properties = set()
        self._player_name = player_name
        self._variable_1 = variable_1
        self._variable_2 = variable_2
        self._variable_3 = variable_3
        self._variable_4 = variable_4
        self._variable_5 = variable_5
        self._is_turn_over = is_turn_over
        self._infra_category_num_dict = {'owned_infra': set()}
        self._pass_start_reward = None

    def get_move_direction(self):
        if self._is_turn_over == "false":
            return "clockwise"
        else:
            return "counterClockwise"

    def get_is_turn_over(self):
        return self._is_turn_over

    def flip_is_turn_over(self):
        if self._is_turn_over == "false":
            self._is_turn_over = "true"
        else:
            self._is_turn_over = "false"

    def get_player_name(self):
        return self._player_name

    def set_player_name(self, new_name):
        self._player_name = new_name

    def get_variable_1(self):
        return self._variable_1

    def get_variable_2(self):
        return self._variable_2

    def get_variable_3(self):
        return self._variable_3

    def get_variable_4(self):
        return self._variable_4

    def get_variable_5(self):
        return self._variable_5

    def get_variables(self):
        return [self._variable_1, self._variable_2, self._variable_3, self._variable_4, self._variable_5]

    def set_variable_1(self, new_val):
        self._variable_1 = new_val

    def set_variable_2(self, new_val):
        self._variable_2 = new_val

    def set_variable_3(self, new_val):
        self._variable_3 = new_val

    def set_variable_4(self, new_val):
        self._variable_4 = new_val

    def set_variable_5(self, new_val):
        self._variable_5 = new_val

    def get_position(self):
        return self._position

    def get_money(self):
        return self._money

    def get_stop(self):
        return self._remaining_stop

    def add_properties(self, land):
        self._properties.add(land)

    def get_properties(self):
        return self._properties

    def get_asset(self):
        ret = self.get_money()
        for land in self._properties:
            ret += land.get_evaluation()
        return ret

    def get_owned_house_num(self):
        ret = 0
        for land in self._properties:
            if land.get_type() == LandType.CONSTRUCTION_LAND:
                ret += land.get_property_num()
        return ret

    def remove_property(self, building):
        self._properties.remove(building)

    def set_money(self, new_val):
        self._money = new_val

    def add_money(self, val):
        self._money += val

    def deduct_money(self, val):
        self._money -= val

    def get_stop_num(self):
        return self._remaining_stop

    def set_stop(self, val):
        self._remaining_stop = val

    def add_stop(self, val):
        self._remaining_stop += val

    def add_one_stop(self):
        self._remaining_stop += 1

    def deduct_stop_num(self):
        self._remaining_stop -= 1

    def set_position(self, pos):
        self._position = pos

    def get_index(self):
        return self._index

    def get_infra_category_num_dict(self):
        return self._infra_category_num_dict

    def set_infra_category_num_dict(self, infra_category_num_dict):
        self._infra_category_num_dict = infra_category_num_dict

    def add_owned_infra(self, land):
        self._infra_category_num_dict['owned_infra'].add(land)

    def get_owned_infra(self):
        return self._infra_category_num_dict['owned_infra']

    def set_pass_start_reward(self, money_pass_start):
        self._pass_start_reward = money_pass_start

    def get_pass_start_reward(self):
        return self._pass_start_reward
     
    def __str__(self):
        return "Player index: {0}".format(self._index)




def test():
    b = Building(1, 1, 1, 1, 1, 1)
    c = Building(1, 1, 1, 1, 1, 1)
    # assert b == c


test()
