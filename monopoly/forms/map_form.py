from django.forms import ModelForm, ValidationError
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from monopoly.models import Map, Cardset
from django.forms import ModelMultipleChoiceField

class MapForm(ModelForm):
    cardsets = ModelMultipleChoiceField(label="使用卡片集", help_text="按住“Control”或“Command”(MAC)以選擇多於一個卡片集", queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.allow_name_duplicate = kwargs.pop('allow_name_duplicate', None)
        super(MapForm, self).__init__(*args, **kwargs)
        self.fields['cardsets'].queryset = Cardset.objects.filter(user=self.user).annotate(card_num=Count('chancecard')).filter(card_num__gt=0)
        
    
    def clean_map_name(self):
        data = self.cleaned_data['map_name']
        if self.allow_name_duplicate:
            return data
        user_old_maps = Map.objects.filter(creator= self.user)
        #check if new map name is the same as old one
        for i in range(len(user_old_maps)):
            if data == user_old_maps[i].map_name:
                raise ValidationError(_('新地圖名稱重複,請設為不重複名稱'), code='map_name_duplicate')
        return data

    class Meta:
        model = Map
        fields = ['map_name', 'cardsets']
        labels = {'map_name': _('地圖名稱')}
        help_texts = {'map_name': _('請設名稱介於1~20個字')}