from django.contrib import admin

# Register your models here.
from .models import *

# Define the admin class
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'avatar')

@admin.register(Cardset)
class CardsetAdmin(admin.ModelAdmin):
    list_display = ('user', 'cardset_name', 'id')

@admin.register(ChanceCard)
class ChanceCardAdmin(admin.ModelAdmin):
    list_display = ('cardset', 'description', 'money_deduction', 'stop_round')

@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('creator', 'display_cardsets', 'map_name', 'id')

@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    list_display = ('_map', 'pos', 'description', 'land_type', 'value')

@admin.register(LandType)
class LandTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'land_type')

@admin.register(UserDefineVariable)
class UserDefineVariableAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'player_index', 'variable_1', 'variable_2', 'variable_3', 'variable_4', 'variable_5')

@admin.register(UserDefineVariableName)
class UserDefineVariableNameAdmin(admin.ModelAdmin):
    list_display = ('variable_1_name', 'variable_2_name', 'variable_3_name', 'variable_4_name', 'variable_5_name')

@admin.register(ScoreBoardSetting)
class ScoreBoardSettingAdmin(admin.ModelAdmin):
    list_display = ('prior_variable', 'is_descending_order', 'background_img_url', 'score_board_sound_effect')

@admin.register(MusicAuthor)
class MusicAuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'credit_url')

@admin.register(MusicCollection)
class MusicCollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'path')

@admin.register(MusicSetting)
class MusicSettingAdmin(admin.ModelAdmin):
    list_display = ('_map', 'background', 'money_deduction', 'money_addition')

@admin.register(BackGroundSetting)
class BackGroundSettingAdmin(admin.ModelAdmin):
    list_display = ('_map', 'background_img_url', 'tile_background_img')

@admin.register(BasicSetting)
class BackGroundSettingAdmin(admin.ModelAdmin):
    list_display = ('_map', 'money_initial', 'money_pass_start', 'house_construction_cost', 'ratio_rent_vs_price', 'ratio_rent_vs_price_for_house', 'rent_constant')

    