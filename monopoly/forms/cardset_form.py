from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _
from monopoly.models import Cardset
import mimetypes

class CardsetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(CardsetForm, self).__init__(*args, **kwargs)

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
        model = Cardset
        fields = ['cardset_name', 'background_img_url']
        labels = {'cardset_name': _('卡片集名稱'), 'background_img_url': _('卡片集背景圖片網址')}
        help_texts = {'cardset_name': _('請設名稱介於1~20個字')}