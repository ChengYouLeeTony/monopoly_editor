from django.forms import ModelForm, ValidationError, TextInput, CharField, ImageField, FileInput
from django.utils.translation import ugettext_lazy as _
from django import forms
from monopoly.models import Map, Land
import re
import random
from io import BytesIO
from PIL import Image

class LandForm(ModelForm):
    color = CharField(label='土地顏色', max_length=7,
        widget=TextInput(attrs={'type': 'color', 'placeholder':' 請輸入hex code'}))
    image = ImageField(label=_('新自訂圖片'),required=False, help_text=_('設定自訂圖片後，將不再自動產生圖片'), error_messages = {'invalid':_("只可上傳圖片")}, widget=FileInput)

    def __init__(self, *args, **kwargs):
        self.pos = kwargs.pop('pos', None)
        self.variable_1_name = kwargs.pop('variable_1_name', "")
        self.variable_2_name = kwargs.pop('variable_2_name', "")
        self.variable_3_name = kwargs.pop('variable_3_name', "")
        self.variable_4_name = kwargs.pop('variable_4_name', "")
        self.variable_5_name = kwargs.pop('variable_5_name', "")
        super(LandForm, self).__init__(*args, **kwargs)
        self.fields['variable_1_change'].label = self.variable_1_name + "變化值(x1)"
        self.fields['variable_2_change'].label = self.variable_2_name + "變化值(x2)"
        self.fields['variable_3_change'].label = self.variable_3_name + "變化值(x3)"
        self.fields['variable_4_change'].label = self.variable_4_name + "變化值(x4)"
        self.fields['variable_5_change'].label = self.variable_5_name + "變化值(x5)"
        self.fields['modal_message'].widget.attrs['rows'] = 3
        self.fields['modal_message'].widget.attrs['cols'] = 25
        # self.fields['image'].widget = forms.FileInput
        # self.fields['image'].error_messages = {'invalid':_("只可上傳圖片")}
        if self.variable_1_name == "":
            del self.fields['variable_1_change']
        if self.variable_2_name == "":
            del self.fields['variable_2_change']
        if self.variable_3_name == "":
            del self.fields['variable_3_change']
        if self.variable_4_name == "":
            del self.fields['variable_4_change']
        if self.variable_5_name == "":
            del self.fields['variable_5_change']

        self.fields['land_type'].empty_label=None
    

    def clean_image(self):
        image_field = self.cleaned_data.get('image')
        if image_field:
            try:
                print(11)
                image_file = BytesIO(image_field.file.read())
                image = Image.open(image_file)
                if image.width < 256 or image.height < 256:
                    image.thumbnail((128, 128), Image.LANCZOS)
                image.thumbnail((256, 256), Image.LANCZOS)
                """rotate image to fit the board"""
                pos = self.pos
                if (pos <= 19 and pos >= 11):
                    image = image.transpose(Image.ROTATE_270)
                elif (pos <= 30 and pos >= 21):
                    image = image.transpose(Image.ROTATE_180)
                elif (pos <= 39 and pos >= 31):
                    image = image.transpose(Image.ROTATE_90)
                buffer = BytesIO()
                image.save(fp=buffer, format='PNG')
                image_field.file = buffer
                image_field.image = image

                return image_field
            except IOError:
                logger.exception("Error during resize image")

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
        model = Land
        fields = ['land_type', 'description', 'value', 'color', 'is_use_upload_image', 'image', 'modal_message', 'additional_parameter', 'variable_1_change', 'variable_2_change',
        'variable_3_change', 'variable_4_change', 'variable_5_change']
        labels = {'land_type': _('土地種類'), 'description': _('顯示內容'), 'value':_('土地數值'), 'is_use_upload_image':_('使用自訂圖片') ,'modal_message':_('觸發文字')}
        help_texts = {'land_type': _('請選擇土地所屬的種類'), 'description': _('最多輸入10個字')}