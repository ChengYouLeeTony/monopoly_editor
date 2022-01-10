from django.forms import ModelForm, ValidationError, ImageField, FileInput, TextInput, CharField
from django.utils.translation import ugettext_lazy as _
from monopoly.models import BackGroundSetting
import re
from io import BytesIO
from PIL import Image
import mimetypes

class BackGroundSettingForm(ModelForm):
    land_background_color = CharField(label='土地背景顏色', max_length=7,
        widget=TextInput(attrs={'type': 'color', 'placeholder':' 請輸入hex code'}))
    land_text_color = CharField(label='土地文字顏色', max_length=7,
        widget=TextInput(attrs={'type': 'color', 'placeholder':' 請輸入hex code'}))
    def clean_tile_background_img(self):
        image_field = self.cleaned_data.get('tile_background_img')
        if image_field:
            try:
                image_file = BytesIO(image_field.file.read())
                image = Image.open(image_file)
                if image.width < 256 or image.height < 256:
                    image.thumbnail((128, 128), Image.LANCZOS)
                image.thumbnail((256, 256), Image.LANCZOS)
                buffer = BytesIO()
                image.save(fp=buffer, format='PNG')
                image_field.file = buffer
                image_field.image = image

                return image_field
            except IOError:
                logger.exception("Error during resize image")

    def clean_modal_background_img_url(self):
        data = self.cleaned_data['modal_background_img_url']
        """allow none value"""
        if data == "":
            return data

        if self.is_url_image(data):
            return data
        else:
            raise ValidationError(_('圖片網址有誤請重新輸入'), code='img_url_error')

    def clean_background_img_url(self):
        data = self.cleaned_data['background_img_url']
        """allow default value"""
        if data == "預設":
            return data

        if self.is_url_image(data):
            return data
        else:
            raise ValidationError(_('背景圖片網址有誤請重新輸入'), code='img_url_error')

    def is_url_image(self, url):    
        mimetype,encoding = mimetypes.guess_type(url)
        return (mimetype and mimetype.startswith('image'))

    class Meta:
        model = BackGroundSetting
        fields = ['background_img_url', 'tile_background_img', 'modal_background_img_url', 'land_background_color', 'land_text_color']
        labels = {'background_img_url': _('背景圖片網址'), 'tile_background_img': _('圖版中央圖片'), 'modal_background_img_url': _('遊戲訊息背景圖片網址')}