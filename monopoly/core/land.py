from .building import *


class Land(object):
    # _pos = 0  # index
    # _description = "Empty Land"  # land
    # _content = None

    # property
    def __init__(self, pos, description, content):
        self._pos = pos
        self._description = description
        self._content = content

    def add_handler(self, handler):
        self._handlers.append(handler)

    def set_content(self, cotent_land):
        self._content = cotent_land

    def get_type(self):
        return self._content.get_type()

    def get_evaluation(self):
        if self.get_content().get_type() == LandType.INFRA or self.get_content(
        ).get_type() == LandType.CONSTRUCTION_LAND:
            return self.get_content().get_evaluation()
        return 0

    def get_content(self):
        return self._content

    def get_position(self):
        return self._pos

    def get_description(self):
        return self._description

    def get_price(self):
        return self._price

    def __str__(self):
        type_str = LandType.get_description(self.get_type())
        return "land position {0}, land content type {1}".format(
            self.get_position(), type_str)


class ConstructionLand(object):
    # _price = 0
    # _properties = BuildingType.NOTHING  # the list of the properties, if len == 0,
    # # means no
    # _building_num = 0
    # _owner = None

    def __init__(self, price, constant=None):
        self._price = price
        self._properties = BuildingType.NOTHING
        self._building_num = 0
        self._owner = None
        self.constant = constant

    def get_price(self):
        return self._price

    def get_evaluation(self):
        building_value = self._price
        if self._properties == BuildingType.HOUSE:
            building_value += self.constant.HOUSE_CONSTRUCTION_COST * self._building_num
        elif self._properties == BuildingType.HOTEL:
            building_value += self.constant.HOUSE_CONSTRUCTION_COST * self.constant.NUM_OF_HOUSE_EQUAL_HOTEL
        return building_value

    def get_property(self):
        return self._properties

    def get_property_type(self):
        if self._building_num == 0:
            return BuildingType.NOTHING
        return self._properties

    def get_type(self):
        return LandType.CONSTRUCTION_LAND

    def get_next_construction_price(self):
        if self._properties == BuildingType.HOUSE and self._building_num == self.constant.NUM_OF_HOUSE_EQUAL_HOTEL - 1:
            return self.constant.HOUSE_CONSTRUCTION_COST
        return self.constant.HOUSE_CONSTRUCTION_COST

    def get_property_num(self):
        return self._building_num

    def clear_properties(self):
        self._properties = BuildingType.NOTHING
        self._building_num = 0

    def set_owner(self, index):
        self._owner = index

    def is_constructable(self):
        return not self._properties == BuildingType.HOTEL

    def get_owner_index(self):
        return self._owner

    def add_properties(self):
        if self._properties == BuildingType.NOTHING or \
                (self._properties == BuildingType.HOUSE and
                 self._building_num < self.constant.NUM_OF_HOUSE_EQUAL_HOTEL - 1):
            self._building_num += 1
            self._properties = BuildingType.HOUSE
            return True
        elif self._properties == BuildingType.HOUSE and self._building_num == self.constant.NUM_OF_HOUSE_EQUAL_HOTEL - 1:
            self._properties = BuildingType.HOTEL
            self._building_num = self.constant.NUM_OF_HOUSE_EQUAL_HOTEL
            return True
        elif self._properties == BuildingType.HOTEL:
            return False
        else:
            # error
            print('Fatal error when adding properties')
            assert False

    def get_rent(self):
        if self._properties == BuildingType.HOTEL:
            ret = self._price * self.constant.RATIO_RENT_VS_PRICE + self.constant.NUM_OF_HOUSE_EQUAL_HOTEL * self.constant.HOUSE_CONSTRUCTION_COST * self.constant.RATIO_RENT_VS_PRICE_FOR_HOUSE + \
                  self.constant.RENT_CONSTANT
        else:
            ret = self._price * self.constant.RATIO_RENT_VS_PRICE + self._building_num * self.constant.HOUSE_CONSTRUCTION_COST * self.constant.RATIO_RENT_VS_PRICE_FOR_HOUSE + \
                  self.constant.RENT_CONSTANT
        print('debug114, rent is', int(ret))
        return int(ret)


class Infra(object):
    # _price = 0
    # _owner = None

    def __init__(self, price, constant=None, category=None):
        self._price = price
        self._owner = None
        self.constant = constant
        self.category = category
        self.num_of_same_category_of_same_owner = 1

    def get_owner_index(self):
        return self._owner

    def get_price(self):
        return self._price

    def get_type(self):
        return LandType.INFRA

    def set_owner(self, index):
        self._owner = index

    def get_payment(self):
        return int(self.get_price() * self.constant.RATIO_RENT_VS_PRICE_INFRA + self.num_of_same_category_of_same_owner * self.get_price() * self.constant.RATIO_RENT_VS_PRICE_INFRA_FOR_SAME_CATEGORY + self.constant.RENT_CONSTANT_INFRA)

    def get_evaluation(self):
        return self.get_price()

    def get_category(self):
        return self.category

    def set_num_of_same_category_of_same_owner(self, num):
        self.num_of_same_category_of_same_owner = num

    def add_num_of_same_category_of_same_owner(self):
        self.num_of_same_category_of_same_owner += 1


class StartLand(object):
    # _reward = 0

    def __init__(self, reward):
        self._reward = reward

    def get_reward(self):
        return self._reward

    def get_type(self):
        return LandType.START

    def get_owner_index(self):
        return None


class JailLand(object):
    # _stops = 0

    def __init__(self, stops):
        self._stops = stops

    def get_stop_num(self):
        return self._stops

    def get_type(self):
        return LandType.JAIL

    def get_owner_index(self):
        return None


class ParkingLand(object):
    def __init__(self, value = 0):
        self._value = value

    def get_value(self):
        return self._value
        
    def get_type(self):
        return LandType.PARKING

    def get_owner_index(self):
        return None


class ChanceLand(object):
    def __init__(self, value = 0):
        self._value = value

    def get_value(self):
        return self._value

    def get_type(self):
        return LandType.CHANCE

    def get_owner_index(self):
        return None

class UserDefineLand(object):
    def __init__(self, value = 0, title = "", message = "", option_tuple = None):
        self._value = value
        self._title = title
        self._message = message
        self._option_tuple = option_tuple

    def is_option(self):
        return (self._option_tuple != None)

    def get_value(self):
        return self._value

    def get_type(self):
        return LandType.USER_DEFINE

    def get_option_tuple(self):
        return self._option_tuple

    def get_confirm_button_text(self):
        if self._option_tuple:
            return self._option_tuple[0]
        else:
            return None

    def get_cancel_button_text(self):
        if self._option_tuple:
            return self._option_tuple[1]
        else:
            return None

    def get_owner_index(self):
        return None

    def set_message(self, message):
        self._message = message

    def set_title(self, message):
        self._title = title

    def get_message(self):
        return self._message

    def get_title(self):
        return self._title


class LandType(object):
    CONSTRUCTION_LAND = 0
    INFRA = 1
    START = 2
    PARKING = 3
    JAIL = 4
    CHANCE = 5
    USER_DEFINE = 6

    @staticmethod
    def get_description(val):
        ret = ["Construction Land",
               "Infrastructure",
               "New Start",
               "Parking ",
               "AIV Jail",
               "Chance Card",
               "自訂土地"]
        return ret[val]
