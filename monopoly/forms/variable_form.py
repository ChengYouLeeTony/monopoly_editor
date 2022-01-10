from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _
from monopoly.models import UserDefineVariable, UserDefineVariableName

class VariableNameForm(ModelForm):

    class Meta:
        model = UserDefineVariableName
        fields = ['variable_1_name', 'variable_1_default', 'is_variable_1_visible', 'variable_2_name', 'variable_2_default', 'is_variable_2_visible', 'variable_3_name',
        'variable_3_default', 'is_variable_3_visible', 'variable_4_name', 'variable_4_default', 'is_variable_4_visible', 'variable_5_name', 'variable_5_default', 'is_variable_5_visible']
        labels = {'variable_1_name': _('自訂變數x1'), 'variable_2_name': _('自訂變數x2'), 'variable_3_name': _('自訂變數x3'),
        'variable_4_name': _('自訂變數x4'), 'variable_5_name': _('自訂變數x5'), 'variable_1_default': _('x1初始值'),
        'variable_2_default': _('x2初始值'), 'variable_3_default': _('x3初始值'), 'variable_4_default': _('x4初始值'),
        'variable_5_default': _('x5初始值'), 'is_variable_1_visible':_('自訂變數x1遊戲中可見'), 'is_variable_2_visible':_('自訂變數x2遊戲中可見'),
        'is_variable_3_visible':_('自訂變數x3遊戲中可見'), 'is_variable_4_visible':_('自訂變數x4遊戲中可見'), 'is_variable_5_visible':_('自訂變數x5遊戲中可見')}

class VariableForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.variable_1_name = kwargs.pop('variable_1_name', "")
        self.variable_2_name = kwargs.pop('variable_2_name', "")
        self.variable_3_name = kwargs.pop('variable_3_name', "")
        self.variable_4_name = kwargs.pop('variable_4_name', "")
        self.variable_5_name = kwargs.pop('variable_5_name', "")
        self.player_index = kwargs.pop('player_index', None)
        super( VariableForm, self).__init__(*args, **kwargs)
        self.fields['variable_1'].label = self.variable_1_name + "初始值"
        self.fields['variable_2'].label = self.variable_2_name + "初始值"
        self.fields['variable_3'].label = self.variable_3_name + "初始值"
        self.fields['variable_4'].label = self.variable_4_name + "初始值"
        self.fields['variable_5'].label = self.variable_5_name + "初始值"
        if self.variable_1_name == "":
            del self.fields['variable_1']
        if self.variable_2_name == "":
            del self.fields['variable_2']
        if self.variable_3_name == "":
            del self.fields['variable_3']
        if self.variable_4_name == "":
            del self.fields['variable_4']
        if self.variable_5_name == "":
            del self.fields['variable_5']

    class Meta:
        model = UserDefineVariable
        fields = ['player_name', 'variable_1', 'variable_2', 'variable_3', 'variable_4', 'variable_5']
        labels = {'player_name': _('玩家一名稱')}
   