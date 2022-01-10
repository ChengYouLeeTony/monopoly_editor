from django.db import models

# Create your models here.
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

# Used to send mail from within Django
from django.core.mail import send_mail
import uuid # Required for unique book instances
from colorfield.fields import ColorField
from .core.initial_value import *
import secrets

# We will use the default User model and this Profile model for user info
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=140, blank=True)
    avatar = models.FileField(blank=False, upload_to='avatar/')
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return str(self.user) + str(self.bio) + str(self.avatar)

class Session:
    def __init__(self):
        pass

    def register(self, conf):
        error_message = "錯誤: "
        translate_dict = {
            'username': '使用者名稱',
            'firstname': '名',
            'lastname': '姓',
            'password': '密碼',
            'email': '信箱'
        }
        for (key, value) in conf.items():
            if key == "request": continue
            if not value or len(value) == 0:
                key = translate_dict[key]
                error_message += key + " 不能為空白"
                return False, error_message

        if len(User.objects.filter(username=conf["username"])):
            error_message += "使用者名稱重複，請更換一個"
            return False, error_message

        request = conf["request"]

        user = User.objects.create_user(
            username=conf["username"],
            first_name=conf["firstname"],
            last_name=conf["lastname"],
            password=conf["password"],
            email=conf["email"]
        )

        user.is_active = False
        user.save()

        # Generate a one-time use token and an email message body
        token = default_token_generator.make_token(user)

        email_body = """
        請點擊下面的鏈接以驗證您的電子郵件地址和完成您的帳戶註冊：
        https://{host}{path}
        """.format(host=request.get_host(),
                path=reverse('confirm', args=(user.username, token)))

        send_mail(subject="來自大富翁創造家的信箱驗證",
                message= email_body,
                from_email="tony180004@gmail.com",
                recipient_list=[user.email])

        return True, None

class Cardset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cardset_name = models.CharField(max_length=20, help_text='請輸入卡片集名稱')
    background_img_url = models.CharField(default="", blank=True, max_length=500)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="卡片集的獨特id", editable=False)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('cardset-detail', args=[str(self.id)])

    def __str__(self):
        return self.cardset_name

class ChanceCard(models.Model):
    cardset = models.ForeignKey('Cardset', on_delete=models.CASCADE)
    title = models.CharField(default="", max_length=15)
    subtitle = models.CharField(default="", max_length=15, blank=True)
    description = models.TextField(default="", max_length=200, blank=True, help_text='請輸入機會內容的描述')
    money_addition = models.CharField(default="0", help_text='請輸入增加的金錢數目', max_length=30)
    money_deduction = models.CharField(default="0", help_text='請輸入減少的金錢數目', max_length=30)
    stop_round = models.IntegerField(default=0, help_text='請輸入暫停的回合數目')
    variable_1_change = models.CharField(default="", blank=True, max_length=30)
    variable_2_change = models.CharField(default="", blank=True, max_length=30)
    variable_3_change = models.CharField(default="", blank=True, max_length=30)
    variable_4_change = models.CharField(default="", blank=True, max_length=30)
    variable_5_change = models.CharField(default="", blank=True, max_length=30)
    is_multiple_choice = models.BooleanField(default=False)
    multiple_choice_1 = models.CharField(default="", blank=True, max_length=20)
    multiple_choice_2 = models.CharField(default="", blank=True, max_length=20)
    multiple_choice_3 = models.CharField(default="", blank=True, max_length=20)
    multiple_choice_4 = models.CharField(default="", blank=True, max_length=20)
    multiple_choice_answer =  models.IntegerField(default=0)
    money_deduction_when_wrong_answer = models.IntegerField(default=0)

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.description[:10])

class Map(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    cardsets = models.ManyToManyField(Cardset, blank=True, help_text="選擇所包含的卡片集")
    map_name = models.CharField(max_length=20, help_text='請輸入地圖名稱')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="地圖的獨特id", editable=False)
    rolled_rule = models.TextField(default= INIT_MAP_ROLLED_RULE, max_length=2000)
    rolled_rule_blockly = models.TextField(default = INIT_MAP_ROLLED_RULE_BLOCKLY , max_length=100000)

    def display_cardsets(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([cardset.cardset_name for cardset in self.cardsets.all()[:3]])

    display_cardsets.short_description = 'Cardsets'

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('map-detail', args=[str(self.id)])

    def __str__(self):
        return '{0} ({1})'.format(self.map_name, self.creator)

class LandType(models.Model):
    land_type = models.CharField(max_length=20, help_text='請輸入土地的種類')

    def __str__(self):
        return self.land_type

def map_lands_path(instance, filename):
    return 'map/{0}/{1}_{2}'.format(instance._map.id, secrets.token_urlsafe(), filename) 

class Land(models.Model):
    _map = models.ForeignKey(Map, on_delete=models.CASCADE)
    pos = models.IntegerField(help_text='土地的位置')
    description = models.CharField(default="台北市", blank=True, max_length=10, help_text='請輸入土地的描述')
    land_type = models.ForeignKey(LandType, on_delete=models.DO_NOTHING)
    value = models.IntegerField(default=0, null=True, blank=True)
    color = ColorField(null=True, blank=True, default='#955436')
    is_use_upload_image = models.BooleanField(default=False)
    image = models.ImageField(default='', null=True, blank=True, upload_to=map_lands_path)
    modal_message = models.TextField(default="", blank=True, max_length=100)
    variable_1_change = models.CharField(default="", blank=True, max_length=30)
    variable_2_change = models.CharField(default="", blank=True, max_length=30)
    variable_3_change = models.CharField(default="", blank=True, max_length=30)
    variable_4_change = models.CharField(default="", blank=True, max_length=30)
    variable_5_change = models.CharField(default="", blank=True, max_length=30)
    additional_parameter = models.CharField(default="", blank=True, max_length=30)

    def __str__(self):
        return '{0} ({1}({2}))'.format(self.description, self.land_type, self.value)

class UserDefineVariable(models.Model):
    _map = models.ForeignKey(Map, on_delete=models.CASCADE)
    player_name = models.CharField(default="", blank=True, max_length=10)
    player_index = models.IntegerField(default=0)
    variable_1 = models.IntegerField(default=0, null=True, blank=True)
    variable_2 = models.IntegerField(default=0, null=True, blank=True)
    variable_3 = models.IntegerField(default=0, null=True, blank=True)
    variable_4 = models.IntegerField(default=0, null=True, blank=True)
    variable_5 = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return '({0}, {1}, {2}, {3}, {4})'.format(self.variable_1, self.variable_2, self.variable_3, self.variable_4, self.variable_5)

class UserDefineVariableName(models.Model):
    _map = models.OneToOneField(Map, on_delete=models.CASCADE)
    variable_1_name = models.CharField(default="", blank=True, max_length=10, help_text="請輸入自訂變數x1在遊戲中的名稱")
    variable_2_name = models.CharField(default="", blank=True, max_length=10, help_text="請輸入自訂變數x2在遊戲中的名稱")
    variable_3_name = models.CharField(default="", blank=True, max_length=10, help_text="請輸入自訂變數x3在遊戲中的名稱")
    variable_4_name = models.CharField(default="", blank=True, max_length=10, help_text="請輸入自訂變數x4在遊戲中的名稱")
    variable_5_name = models.CharField(default="", blank=True, max_length=10, help_text="請輸入自訂變數x5在遊戲中的名稱")
    variable_1_default = models.IntegerField(default=0, null=True, blank=True)
    variable_2_default = models.IntegerField(default=0, null=True, blank=True)
    variable_3_default = models.IntegerField(default=0, null=True, blank=True)
    variable_4_default = models.IntegerField(default=0, null=True, blank=True)
    variable_5_default = models.IntegerField(default=0, null=True, blank=True)
    is_variable_1_visible = models.BooleanField(default=True)
    is_variable_2_visible = models.BooleanField(default=True)
    is_variable_3_visible = models.BooleanField(default=True)
    is_variable_4_visible = models.BooleanField(default=True)
    is_variable_5_visible = models.BooleanField(default=True)

    def __str__(self):
        return '({0}, {1}, {2}, {3}, {4})'.format(self.variable_1_name, self.variable_2_name, self.variable_3_name, self.variable_4_name, self.variable_5_name)

class ScoreBoardSetting(models.Model):
    _map = models.OneToOneField(Map, on_delete=models.CASCADE)
    prior_variable = models.CharField(default="asset", max_length=30)
    is_descending_order = models.BooleanField(default=True)
    title = models.CharField(default="計分板", max_length=15, blank=True)
    subtitle = models.CharField(default="Good Game!", max_length=15, blank=True)
    background_img_url = models.CharField(default="", blank=True, max_length=500)
    score_board_sound_effect = models.CharField(default="background", blank=True, max_length=500)
    audio_url = models.CharField(default="default/bgm/background.mp3", blank=True, max_length=500)

    def __str__(self):
        return self.prior_variable + "is_descending_order: " + str(self.is_descending_order)

class MusicAuthor(models.Model):
    name = models.CharField(default="", max_length=200)
    credit_url = models.CharField(default="", blank=True, max_length=1000)

    def __str__(self):
        return self.name

class MusicCollection(models.Model):
    author = models.ForeignKey(MusicAuthor, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=200)
    path = models.CharField(default="", max_length=200)

    def __str__(self):
        return self.name

class MusicSetting(models.Model):
    _map = models.OneToOneField(Map, on_delete=models.CASCADE)
    background = models.CharField(default="預設", blank=True, max_length=500)
    money_deduction = models.CharField(default="預設", blank=True, max_length=500)
    money_addition = models.CharField(default="預設", blank=True, max_length=500)
    dice = models.CharField(default="預設", blank=True, max_length=500)
    hover_button = models.CharField(default="預設", blank=True, max_length=500)
    build = models.CharField(default="預設", blank=True, max_length=500)
    player_move = models.CharField(default="預設", blank=True, max_length=500)
    player_teleport = models.CharField(default="預設", blank=True, max_length=500)
    player_turn_over = models.CharField(default="預設", blank=True, max_length=500)
    wrong_answer = models.CharField(default="預設", blank=True, max_length=500)
    user_define_1 = models.CharField(default="", blank=True, max_length=500)
    user_define_2 = models.CharField(default="", blank=True, max_length=500)
    user_define_3 = models.CharField(default="", blank=True, max_length=500)
    volume_background = models.IntegerField(default=60)
    volume_money_deduction = models.IntegerField(default=100)
    volume_money_addition = models.IntegerField(default=100)
    volume_dice = models.IntegerField(default=100)
    volume_hover_button = models.IntegerField(default=100)
    volume_build = models.IntegerField(default=100)
    volume_player_move = models.IntegerField(default=100)
    volume_player_teleport = models.IntegerField(default=100)
    volume_player_turn_over = models.IntegerField(default=100)
    volume_user_define_1 = models.IntegerField(default=100)
    volume_user_define_2 = models.IntegerField(default=100)
    volume_user_define_3 = models.IntegerField(default=100)
    volume_wrong_answer = models.IntegerField(default=100)


    def __str__(self):
        return self.background

def map_background_path(instance, filename):
    return 'map/{0}/-1'.format(instance._map.id) + secrets.token_urlsafe() + '.png'

class BackGroundSetting(models.Model):
    _map = models.OneToOneField(Map, on_delete=models.CASCADE)
    background_img_url = models.CharField(default="預設", blank=True, max_length=500)
    tile_background_img = models.ImageField(default='', null=True, blank=True, upload_to= map_background_path)
    modal_background_img_url = models.CharField(default="", blank=True, max_length=500)
    land_background_color = ColorField(null=True, blank=True, default='#cde6d0')
    land_text_color = ColorField(null=True, blank=True, default='#000000')
    def __str__(self):
        return self.background_img_url

class BasicSetting(models.Model):
    _map = models.OneToOneField(Map, on_delete=models.CASCADE)
    money_initial = models.IntegerField(default=15000)
    money_pass_start = models.CharField(default="2000", max_length=100)
    house_construction_cost = models.IntegerField(default=1000)
    num_of_house_equal_hotel = models.IntegerField(default=4)
    ratio_rent_vs_price = models.FloatField(default=0.1)
    ratio_rent_vs_price_for_house = models.FloatField(default=0.5)
    rent_constant = models.IntegerField(default=0)
    ratio_rent_vs_price_infra = models.FloatField(default=0)
    ratio_rent_vs_price_infra_for_same_category = models.FloatField(default=0.125)
    rent_constant_infra = models.IntegerField(default=0)
    welcome_info = models.CharField(default="歡迎來到大富翁遊戲", max_length=15)
    game_process = models.TextField(default="踩到監獄或是抽到監獄事件時你可能會被關到監獄(暫停回合)\n當有一位玩家破產時，遊戲結束", blank=True, max_length=500)
    
    def __str__(self):
        return str(self.money_initial)










