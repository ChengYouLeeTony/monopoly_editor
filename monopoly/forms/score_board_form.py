from django.forms import ModelForm, ValidationError, ChoiceField, RadioSelect, CharField, URLInput
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from monopoly.models import ScoreBoardSetting
from django.forms import ModelMultipleChoiceField
from django.forms.widgets import RadioSelect
import mimetypes

class ScoreBoardForm(ModelForm):
    prior_variable = ChoiceField(widget=RadioSelect(attrs={'class': "custom-radio-list"}), label="計分依據")
    bgm_choice = [
        ('background', '同背景音樂'), 
        ('score_board_bgm_0','先往く者達(前進的人)'),
        ("score_board_bgm_1", "Don't Give Up"),
        ("others", "其他")
    ]
    score_board_sound_effect = CharField(widget=RadioSelect(choices=bgm_choice, attrs={'class': "custom-radio-list"}), label="計分板背景音樂")
    background_img_url = CharField(widget=URLInput(), required=False, label="計分板背景圖片", help_text="請輸入圖片連結，若此項未輸入，使用預設背景圖片")

    def __init__(self, *args, **kwargs):
        x1_name = kwargs.pop('variable_1_name', "")
        x2_name = kwargs.pop('variable_2_name', "")
        x3_name = kwargs.pop('variable_3_name', "")
        x4_name = kwargs.pop('variable_4_name', "")
        x5_name = kwargs.pop('variable_5_name', "")
        super(ScoreBoardForm, self).__init__(*args, **kwargs)
        CHOICES = [('asset', '總資產(現金+土地+建築)'), ('money','現金餘額'), ('pure_asset', '純資產(土地+建築)')]
        if x1_name != "":
            CHOICES.append(('x1',x1_name))
        if x2_name != "":
            CHOICES.append(('x2',x2_name))
        if x3_name != "":
            CHOICES.append(('x3',x3_name))
        if x4_name != "":
            CHOICES.append(('x4',x4_name))
        if x5_name != "":
            CHOICES.append(('x5',x5_name))
        self.fields['prior_variable'].choices = CHOICES

    def clean_background_img_url(self):
        data = self.cleaned_data['background_img_url']
        """allow none value"""
        if data == "":
            return data

        if self.is_url_image(data):
            return data
        else:
            raise ValidationError(_('圖片網址有誤請重新輸入'), code='img_url_error')
    
    def is_url_image(self, url):    
        mimetype,encoding = mimetypes.guess_type(url)
        return (mimetype and mimetype.startswith('image'))

    class Meta:
        model = ScoreBoardSetting
        fields = ['prior_variable', 'is_descending_order', 'title', 'subtitle', 'background_img_url', 'score_board_sound_effect']
        labels = {'is_descending_order': _('降序排列'), 'title': _('計分板標題'), 'subtitle': _('計分板副標題')}
        help_texts = {'is_descending_order': _('分數是否由高至低排列')}