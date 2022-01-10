from django.forms import ModelForm, ValidationError, ChoiceField, RadioSelect
from django.utils.translation import ugettext_lazy as _
from monopoly.models import Cardset, ChanceCard
import re
import random

class CardForm(ModelForm):
    CHOICES=[(1,'選項ㄧ'), (2,'選項二'), (3,'選項三'), (4,'選項四')]
    multiple_choice_answer = ChoiceField(choices=CHOICES, widget=RadioSelect(attrs={'class': "custom-radio-list"}), label="答案")
    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        self.fields['variable_1_change'].label = "x1變化值(x1)"
        self.fields['variable_2_change'].label = "x2變化值(x2)"
        self.fields['variable_3_change'].label = "x3變化值(x3)"
        self.fields['variable_4_change'].label = "x4變化值(x4)"
        self.fields['variable_5_change'].label = "x5變化值(x5)"
        self.fields['description'].widget.attrs['rows'] = 3
        self.fields['description'].widget.attrs['cols'] = 25
        self.fields['multiple_choice_answer'].initial = [1]

    def clean_variable_1_change(self):
        return self.data_clean_variable_change('variable_1_change')

    def clean_variable_2_change(self):
        return self.data_clean_variable_change('variable_2_change')

    def clean_variable_3_change(self):
        return self.data_clean_variable_change('variable_3_change')

    def clean_variable_4_change(self):
        return self.data_clean_variable_change('variable_4_change')

    def clean_variable_5_change(self):
        return self.data_clean_variable_change('variable_5_change')

    def data_clean_variable_change(self, variable_change):
        data = self.cleaned_data[variable_change]
        if data == "":
            return data
        x1 = random.randint(20, 40)
        x2 = random.randint(20, 40)
        x3 = random.randint(20, 40)
        x4 = random.randint(20, 40)
        x5 = random.randint(20, 40)
        pattern = r'^(x1|x2|x3|x4|x5|\d|\(|\s)*(x1|x2|x3|x4|x5|\d|\(|\)|\+|-|\*|/|%|\s)*(x1|x2|x3|x4|x5|\d|\))$'
        try:
            math_operation_str = re.match(pattern, data).group()
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

    def clean_multiple_choice_answer(self):
        choice = self.cleaned_data['multiple_choice_answer']
        if self.cleaned_data['is_multiple_choice'] == False:
            return self.cleaned_data['multiple_choice_answer']

        if choice == "1" and self.cleaned_data['multiple_choice_1'] == "" or \
        choice == "2" and self.cleaned_data['multiple_choice_2'] == "" or \
        choice == "3" and self.cleaned_data['multiple_choice_3'] == "" or \
        choice == "4" and self.cleaned_data['multiple_choice_4'] == "":
            raise ValidationError(_('答案的選項不可為空白'), code='answer_error')
        return self.cleaned_data['multiple_choice_answer']

    class Meta:
        model = ChanceCard
        fields = ['title', 'subtitle', 'description', 'money_addition', 'money_deduction', 'stop_round', 'variable_1_change', 'variable_2_change',
        'variable_3_change', 'variable_4_change', 'variable_5_change', 'is_multiple_choice', 'multiple_choice_1', 'multiple_choice_2', 'multiple_choice_3', 'multiple_choice_4', 'multiple_choice_answer',
        'money_deduction_when_wrong_answer']
        labels = {'title': _('標題'), 'subtitle': _('副標題'), 'description': _('卡片內容'), 'money_addition': _('增加金額'), 'money_deduction': _('減少金額'), 'stop_round': _('暫停回合'),
        'is_multiple_choice': _('使用選項'), 'multiple_choice_1': _('選項一'), 'multiple_choice_2': _('選項二'), 'multiple_choice_3': _('選項三'), 'multiple_choice_4': _('選項四'),
        'money_deduction_when_wrong_answer':_('答錯時減少金額')}
        help_texts = {'description': _('直接貼上圖片網址可使用圖片'), 'is_multiple_choice': _('勾選使用選項後，機會卡將變為選擇題，玩家選擇正確選項後才能觸發後續事件')}


