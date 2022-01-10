from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _
from monopoly.models import BasicSetting
import mimetypes
import re
import random

class BasicSettingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BasicSettingForm, self).__init__(*args, **kwargs)
        self.fields['game_process'].widget.attrs['rows'] = 5
        self.fields['game_process'].widget.attrs['cols'] = 80

    def clean_money_pass_start(self):
        data = self.cleaned_data["money_pass_start"]
        if data == "":
            return "0"
        x1 = random.randint(20, 40)
        x2 = random.randint(20, 40)
        x3 = random.randint(20, 40)
        x4 = random.randint(20, 40)
        x5 = random.randint(20, 40)
        pattern = r'^(x1|x2|x3|x4|x5|\d|\(|\s)*(x1|x2|x3|x4|x5|\d|\(|\)|\+|-|\*|/|\s)*(x1|x2|x3|x4|x5|\d|\))$'
        try:
            math_operation_str = re.match(pattern, data).group()
            print(math_operation_str)
            """check twice"""
            result = eval(math_operation_str)
            print("result")
            print(result)
            if isinstance(result, (int,float)):
                return data
        except ZeroDivisionError:
            try:
                x1 = random.randint(1, 19)
                x2 = random.randint(1, 19)
                x3 = random.randint(1, 19)
                x4 = random.randint(1, 19)
                x5 = random.randint(1, 19)
                result = eval(math_operation_str)
                if isinstance(result, (int,float)):
                    return data
            except:
                raise ValidationError(_('算式有誤請重新輸入'), code='variable_error')
        except:
             raise ValidationError(_('算式有誤請重新輸入'), code='variable_error')

    class Meta:
        model = BasicSetting
        fields = ['money_initial', 'money_pass_start', 'house_construction_cost', 'num_of_house_equal_hotel', 'welcome_info', 'game_process']
        labels = {'money_initial': _('玩家起始金錢'), 'money_pass_start':_('經過起點獎勵'), 'house_construction_cost': _('建造房屋費用'), 'num_of_house_equal_hotel': _('一棟旅館等於幾棟房屋'), 'welcome_info': _('歡迎玩家訊息'), 'game_process': _('遊戲流程訊息')}