from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _
from monopoly.models import MusicSetting, MusicAuthor
import re

class MusicSettingForm(ModelForm):
    music_author_names = [music_author.name for music_author in MusicAuthor.objects.all()]
    music_labels = {
        'background': '背景',
        'money_deduction': '金錢減少時',
        'money_addition': '金錢增加時',
        'dice': '丟骰子時',
        'build': '建造建築時',
        'hover_button': '滑鼠滑過按鈕時',
        'player_move': '玩家移動時',
        'player_teleport': '玩家傳送時',
        'player_turn_over': '玩家轉向時',
        'wrong_answer': '回答錯誤時',
        'user_define_1': '自訂音效1',
        'user_define_2': '自訂音效2',
        'user_define_3': '自訂音效3',
    }

    def clean_background(self):
        data = self.cleaned_data['background']
        return self.data_clean_audio_url(data, self.music_author_names, self.music_labels['background'])

    def clean_money_deduction(self):
        data = self.cleaned_data['money_deduction']
        return self.data_clean_audio_url(data, self.music_author_names, self.music_labels['money_deduction'])

    def clean_money_addition(self):
        data = self.cleaned_data['money_addition']
        return self.data_clean_audio_url(data, self.music_author_names, self.music_labels['money_addition'])

    def clean_dice(self):
        data = self.cleaned_data['dice']
        return self.data_clean_audio_url(data, self.music_author_names, self.music_labels['dice'])

    def clean_hover_button(self):
        data = self.cleaned_data['hover_button']
        return self.data_clean_audio_url(data, self.music_author_names, self.music_labels['hover_button'])

    def clean_build(self):
        data = self.cleaned_data['build']
        return self.data_clean_audio_url(data, self.music_author_names, self.music_labels['build'])

    def clean_player_move(self):
        data = self.cleaned_data['player_move']
        return self.data_clean_audio_url(data, self.music_author_names, self.music_labels['player_move'])

    def clean_player_teleport(self):
        data = self.cleaned_data['player_teleport']
        return self.data_clean_audio_url(data, self.music_author_names, self.music_labels['player_teleport'])

    def clean_player_turn_over(self):
        data = self.cleaned_data['player_turn_over']
        return self.data_clean_audio_url(data, self.music_author_names, self.music_labels['player_turn_over'])

    def clean_wrong_answer(self):
        data = self.cleaned_data['wrong_answer']
        return self.data_clean_audio_url(data, self.music_author_names, self.music_labels['wrong_answer'])

    def clean_user_define_1(self):
        data = self.cleaned_data['user_define_1']
        return self.data_clean_audio_url(data, self.music_author_names, self.music_labels['user_define_1'])

    def clean_user_define_2(self):
        data = self.cleaned_data['user_define_2']
        return self.data_clean_audio_url(data, self.music_author_names, self.music_labels['user_define_2'])

    def clean_user_define_3(self):
        data = self.cleaned_data['user_define_3']
        return self.data_clean_audio_url(data, self.music_author_names, self.music_labels['user_define_3'])
 

    def data_clean_audio_url(self, data, music_author_names, label):
        if data == "預設" or data == "":
            return data
        elif self.valid_from_copy(data, music_author_names):
            return data
        elif self.is_url_audio(data):
            return data
        elif self.is_google_drive_audio(data):
            pattern = r"/d/(.*)/view\?"
            google_id = re.search(pattern, data).group(1)
            google_url = "https://docs.google.com/uc?export=download&id=" + google_id
            return google_url
        elif self.is_google_drive_download_audio(data):
            return data
        else:
            raise ValidationError(_(label + '音樂網址有誤請重新輸入'), code='audio_url_error')     

    def valid_from_copy(self, data, music_author_names):
        music_author_pattern = "("
        for music_author_name in music_author_names:
            music_author_pattern += music_author_name + "|"
        music_author_pattern = music_author_pattern[:-1] + ")"
        pattern = r"^" + music_author_pattern + r".*(.mp3|.wav|.ogg)$"

        return re.match(pattern, data)

    def is_url_audio(self, data):    
        pattern = r"^(http|https).*(.mp3|.ogg|.wav)"
        return re.match(pattern, data)

    def is_google_drive_audio(self, data):
        pattern = r"https://drive.google.com/.*"
        return re.match(pattern, data)

    def is_google_drive_download_audio(self, data):
        pattern = r"https://docs.google.com/.*"
        return re.match(pattern, data)


    class Meta:
        model = MusicSetting
        fields = ['background', 'money_deduction', 'money_addition', 'dice', 'hover_button', 'build', 'player_move', 'player_teleport', 'player_turn_over', 'wrong_answer', 'user_define_1', 'user_define_2', 'user_define_3']
        labels = {'background': _('背景音樂'), 'money_deduction': _('金錢減少時'), 'money_addition': _('金錢增加時'), 'dice':_('丟骰子時'), 'hover_button':_('滑鼠滑過按鈕時'), 'build':_('建造建築時'),
                'player_move':_('玩家移動時'), 'player_teleport':_('玩家傳送時'), 'player_turn_over':_('玩家轉向時'), 'wrong_answer': _('回答錯誤時(機會卡選擇題)'), 'user_define_1':_('自訂音效1'), 'user_define_2':_('自訂音效2'), 'user_define_3':_('自訂音效3')}