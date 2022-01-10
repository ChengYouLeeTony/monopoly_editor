from .move_result_enum import *


class MoveResult(object):
    # move_result_type = None
    # value = None
    # yes = None
    # land = None

    def __init__(self, move_result_type, value, land):
        self.move_result_type = move_result_type
        self.value = value
        self.land = land
        self.yes = None
        self.msg = None
        self.title = ""
        self.is_user_define_option = False
        self.user_define_option_tuple = None

    def set_is_user_define_option(self, is_user_define_option):
        self.is_user_define_option = is_user_define_option

    def set_user_define_option_tuple(self, user_define_option_tuple):
        self.user_define_option_tuple = user_define_option_tuple

    def set_msg(self, msg):
        self.msg = msg

    def set_title(self, title):
        self.title = title

    def get_is_user_define_option(self):
        return self.is_user_define_option

    def get_user_define_option_tuple(self):
        return self.user_define_option_tuple

    def get_move_result_type(self):
        return self.move_result_type

    def get_value(self):
        return self.value

    def get_land(self):
        return self.land

    def get_title(self):
        return self.title

    def set_decision(self, decision):
        assert self.move_result_type == MoveResultType.BUY_LAND_OPTION or \
               self.move_result_type == MoveResultType.CONSTRUCTION_OPTION or \
               self.move_result_type == MoveResultType.USER_DEFINE
        self.yes = decision

    def get_decision(self):
        assert self.move_result_type == MoveResultType.BUY_LAND_OPTION or \
               self.move_result_type == MoveResultType.CONSTRUCTION_OPTION
        return self.yes

    def get_is_multiple_choice(self):
        return False

    def is_option(self):
        return self.move_result_type == MoveResultType.BUY_LAND_OPTION or \
               self.move_result_type == MoveResultType.CONSTRUCTION_OPTION

    def get_is_multiple_choice(self):
        return False

    def __str__(self):
        saying = self.msg if self.msg else ""
        saying += MoveResultType.get_description(self.move_result_type)
        ret = saying + " value:{0}, land: {1}".format(
            self.value, self.land)
        if self.yes is not None:
            ret += " decision: {0}".format(self.yes)
        return ret

    def beautify(self, curr_player = None):
        saying = self.msg if self.msg else ""
        saying += " " + MoveResultType.get_description(self.move_result_type)
        if self.move_result_type == MoveResultType.BUY_LAND_OPTION:
            saying += "<br><div>價格是" + str(self.value) + "元</div>"
        elif self.move_result_type == MoveResultType.PAYMENT:
            saying += "<br><div>要付出" + str(self.value) + "元</div>"
        elif self.move_result_type == MoveResultType.REWARD:
            saying += "<br><div>獎勵是 " + str(self.value) + "元</div>"
        elif self.move_result_type == MoveResultType.STOP_ROUND:
            saying += "<br><div>暫停 " + str(self.value) + "回合</div>"
        elif self.move_result_type == MoveResultType.CONSTRUCTION_OPTION:
            saying += "<br><div>建造費用是 " + str(self.value) + "元</div>"
        elif self.move_result_type == MoveResultType.USER_DEFINE:
            player = curr_player.get_player_name()
            money = curr_player.get_money()
            x1 =  curr_player.get_variable_1()
            x2 =  curr_player.get_variable_2()
            x3 =  curr_player.get_variable_3()
            x4 =  curr_player.get_variable_4()
            x5 =  curr_player.get_variable_5()
            saying = saying.replace("{money}", str(money)).replace("{player}", str(player)).replace("{x1}", str(x1)).replace("{x2}", str(x2)).replace("{x3}", str(x3)).replace("{x4}", str(x4)).replace("{x5}", str(x5))
            saying = saying.replace("\n", "<br><div>")
            print(saying)
            print('\n' in saying)
        else:
            pass

        return saying

class ChanceCardMoveResult(object):

    def __init__(self, move_result_type, title, subtitle, msg, money_addition, money_deduction, stop_round, variables_change, is_multiple_choice, multiple_choice_info, land, background_img_url, money_deduction_when_wrong_answer):
        self.title = title
        self.subtitle = subtitle
        self.msg = msg
        self.move_result_type = move_result_type
        self.money_addition = money_addition
        self.money_deduction = money_deduction
        self.stop_round = stop_round
        self.variables_change = variables_change
        self.is_multiple_choice = is_multiple_choice
        self.multiple_choice_info = multiple_choice_info
        self.land = land
        self.background_img_url = background_img_url
        self.yes = None
        self.money_deduction_when_wrong_answer = money_deduction_when_wrong_answer

    def get_title(self):
        return self.title

    def get_subtitle(self):
        return self.subtitle

    def get_msg(self):
        return self.msg

    def get_stop_round(self):
        return self.stop_round

    def get_variable_1_change(self):
        return self.variables_change[0]

    def get_variable_2_change(self):
        return self.variables_change[1]

    def get_variable_3_change(self):
        return self.variables_change[2]

    def get_variable_4_change(self):
        return self.variables_change[3]

    def get_variable_5_change(self):
        return self.variables_change[4]

    def get_variables_change(self):
        return self.variables_change

    def get_is_multiple_choice(self):
        return self.is_multiple_choice

    def get_multiple_choice_info(self):
        return self.multiple_choice_info

    def get_move_result_type(self):
        return self.move_result_type

    def get_value(self):
        return self.money_addition + self.money_deduction * -1

    def get_is_user_define_option(self):
        return False

    def get_land(self):
        return self.land

    def get_background_img_url(self):
        return self.background_img_url

    def get_money_deduction_when_wrong_answer(self):
        return self.money_deduction_when_wrong_answer

    def set_decision(self, decision):
        self.yes = decision

    def get_is_user_define_option(self):
        return False

    def is_option(self):
        return False

    def beautify(self, curr_player = None):
        saying = self.msg if self.msg else ""
        if self.move_result_type == MoveResultType.CHANCE_CARD:
            player = curr_player.get_player_name()
            money = curr_player.get_money()
            x1 =  curr_player.get_variable_1()
            x2 =  curr_player.get_variable_2()
            x3 =  curr_player.get_variable_3()
            x4 =  curr_player.get_variable_4()
            x5 =  curr_player.get_variable_5()
            saying = saying.replace("{money}", str(money)).replace("{player}", str(player)).replace("{x1}", str(x1)).replace("{x2}", str(x2)).replace("{x3}", str(x3)).replace("{x4}", str(x4)).replace("{x5}", str(x5))
            saying = saying.replace("\n", "<br><div>")
            print(saying)
            print('\n' in saying)
        else:
            pass

        return saying



