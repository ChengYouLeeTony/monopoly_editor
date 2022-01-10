from django.forms import ModelForm, ValidationError, FileField

from monopoly.models import Profile

MAX_UPLOAD_SIZE = 2500000

class ProfileForm(ModelForm):
    # avatar = FileField(required=False)

    class Meta:
        model = Profile
        fields = ["bio", "avatar"]

    def clean_avatar(self):
        picture = self.cleaned_data['avatar']

        if not picture:
            return picture
        if not picture or not hasattr(picture, 'content_type'):
            raise ValidationError('您必須上傳一張圖片')
        if picture.content_type and not picture.content_type.startswith('image'):
            raise ValidationError('檔案類別不是圖片')
        if picture.size > MAX_UPLOAD_SIZE:
            raise ValidationError('檔案容量太大 (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture



