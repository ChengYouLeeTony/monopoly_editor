class Card(object):

    def __init__(self, title, subtitle, msg, money_addition, money_deduction, stop_round, variables_change, is_multiple_choice, multiple_choice_info, background_img_url, money_deduction_when_wrong_answer):
        """
        title: str
        subtitle: str
        msg: str
        money_addition: str
        money_deduction: str
        stop_round: int
        variables_change: [str, str, str, str, str]
        is_multiple_choice: bool
        multiple_choice_info: {
            'multiple_choice_1': str,
            'multiple_choice_2': str,
            'multiple_choice_3': str,
            'multiple_choice_4': str,
            'multiple_choice_answer': int (1~4)
        }
        money_deduction_when_wrong_answer: int
        """
        self._title = title
        self._subtitle = subtitle
        self._msg = msg
        self._money_addition = money_addition
        self._money_deduction = money_deduction
        self._stop_round = stop_round
        self._variables_change = variables_change
        self._is_multiple_choice = is_multiple_choice
        self._multiple_choice_info = multiple_choice_info
        self._background_img_url = background_img_url
        self._money_deduction_when_wrong_answer = money_deduction_when_wrong_answer

    def get_title(self):
        return self._title

    def get_subtitle(self):
        return self._subtitle

    def get_msg(self):
        return self._msg

    def get_money_addition(self):
        return self._money_addition

    def get_money_deduction(self):
        return self._money_deduction

    def get_stop_round(self):
        return self._stop_round

    def get_variables_change(self):
        return self._variables_change

    def get_is_multiple_choice(self):
        return self._is_multiple_choice

    def get_multiple_choice_info(self):
        return self._multiple_choice_info

    def get_background_img_url(self):
        return self._background_img_url

    def get_money_deduction_when_wrong_answer(self):
        return self._money_deduction_when_wrong_answer

    def __str__(self):
        return self.get_msg()
