from django.shortcuts import render
from django.views import View
from monopoly.models import Map
import json

class GameView(View):
    template_name = 'game_view.html'

    def get(self, request, *args, **kwargs):
        host_name = kwargs.get('host_name', None)
        print(host_name)
        mode = kwargs.get('mode', None)
        """viewer mode"""
        if mode[:6] == "viewer":
            url_list = mode.split('/')
            hash_code = url_list[1]
            map_id = url_list[2]
        else:
            map_id = request.session['latest_map_id']
        print("debug007")
        print(mode)
        print(map_id)
        _map = Map.objects.get(id = map_id)
        lands_objects = _map.land_set.all().order_by('pos')
        lands_image_url = []
        tile_background_img = _map.backgroundsetting.tile_background_img
        for i in range(len(lands_objects)):
            image_url = lands_objects[i].image.url
            lands_image_url.append(image_url)
            if i == len(lands_objects) - 1:
                lands_image_url.append(tile_background_img.url)

        """music setting"""
        music_setting_object = _map.musicsetting
        scoreboard_bgm = _map.scoreboardsetting.audio_url
        music_setting_info = {
            'background': music_setting_object.background,
            'money_deduction': music_setting_object.money_deduction,
            'money_addition': music_setting_object.money_addition,
            'dice': music_setting_object.dice,
            'hover_button': music_setting_object.hover_button,
            'build': music_setting_object.build,
            'player_move': music_setting_object.player_move,
            'player_teleport': music_setting_object.player_teleport,
            'player_turn_over': music_setting_object.player_turn_over,
            'wrong_answer': music_setting_object.wrong_answer,
            'user_define_1': music_setting_object.user_define_1,
            'user_define_2': music_setting_object.user_define_2,
            'user_define_3': music_setting_object.user_define_3,
            'scoreboard_bgm': scoreboard_bgm,
            'volume_background': music_setting_object.volume_background,
            'volume_money_deduction': music_setting_object.volume_money_deduction,
            'volume_money_addition': music_setting_object.volume_money_addition,
            'volume_dice': music_setting_object.volume_dice,
            'volume_hover_button': music_setting_object.volume_hover_button,
            'volume_build': music_setting_object.volume_build,
            'volume_player_move': music_setting_object.volume_player_move,
            'volume_player_teleport': music_setting_object.volume_player_teleport,
            'volume_player_turn_over': music_setting_object.volume_player_turn_over,
            'volume_wrong_answer': music_setting_object.wrong_answer,
            'volume_user_define_1': music_setting_object.volume_user_define_1,
            'volume_user_define_2': music_setting_object.volume_user_define_2,
            'volume_user_define_3': music_setting_object.volume_user_define_3,
        }


        """send user define variable name to template"""
        user_define_variable_name = _map.userdefinevariablename
        """change background img"""
        background_img_url = _map.backgroundsetting.background_img_url
        """modal background img url"""
        modal_background_img_url = _map.backgroundsetting.modal_background_img_url
        """change game process and welcome_info"""
        basicsetting = _map.basicsetting
        game_process = basicsetting.game_process
        welcome_info = basicsetting.welcome_info
        game_process_list = game_process.split("\n")
        """basic setting"""
        money_pass_start = self.make_money_pass_start_readable(_map, basicsetting.money_pass_start)
        house_construction_cost = basicsetting.house_construction_cost
        num_of_house_equal_hotel = basicsetting.num_of_house_equal_hotel
        ratio_rent_vs_price = basicsetting.ratio_rent_vs_price
        ratio_rent_vs_price_for_house = basicsetting.ratio_rent_vs_price_for_house
        rent_constant = basicsetting.rent_constant
        ratio_rent_vs_price_infra = basicsetting.ratio_rent_vs_price_infra
        ratio_rent_vs_price_infra_for_same_category = basicsetting.ratio_rent_vs_price_infra_for_same_category
        rent_constant_infra = basicsetting.rent_constant_infra
        




        return render(request, self.template_name, {
            "username": request.user.username,
            "hostname": kwargs.get("host_name"),
            "map_id": map_id,
            'lands_image_url': json.dumps(lands_image_url),
            'player_variable_1_name': user_define_variable_name.variable_1_name,
            'player_variable_2_name': user_define_variable_name.variable_2_name,
            'player_variable_3_name': user_define_variable_name.variable_3_name,
            'player_variable_4_name': user_define_variable_name.variable_4_name,
            'player_variable_5_name': user_define_variable_name.variable_5_name,
            'is_variable_1_visible': user_define_variable_name.is_variable_1_visible,
            'is_variable_2_visible': user_define_variable_name.is_variable_2_visible,
            'is_variable_3_visible': user_define_variable_name.is_variable_3_visible,
            'is_variable_4_visible': user_define_variable_name.is_variable_4_visible,
            'is_variable_5_visible': user_define_variable_name.is_variable_5_visible,
            'music_setting_info': json.dumps(music_setting_info),
            'background_img_url': background_img_url,
            'game_process_list': game_process_list,
            'welcome_info': welcome_info,
            'money_pass_start': money_pass_start,
            'house_construction_cost': house_construction_cost,
            'num_of_house_equal_hotel': num_of_house_equal_hotel,
            'ratio_rent_vs_price': ratio_rent_vs_price,
            'ratio_rent_vs_price_for_house': ratio_rent_vs_price_for_house,
            'rent_constant': rent_constant,
            'ratio_rent_vs_price_infra': ratio_rent_vs_price_infra,
            'ratio_rent_vs_price_infra_for_same_category': ratio_rent_vs_price_infra_for_same_category,
            'rent_constant_infra': rent_constant_infra,
            'mode': mode,
            'modal_background_img_url': modal_background_img_url
        })
    def make_money_pass_start_readable(self, _map, money_pass_start_str):
        user_define_variable_name = _map.userdefinevariablename
        if user_define_variable_name.variable_1_name != "":
            money_pass_start_str = money_pass_start_str.replace("x1", user_define_variable_name.variable_1_name)
        if user_define_variable_name.variable_2_name != "":
            money_pass_start_str = money_pass_start_str.replace("x2", user_define_variable_name.variable_2_name)
        if user_define_variable_name.variable_3_name != "":
            money_pass_start_str = money_pass_start_str.replace("x3", user_define_variable_name.variable_3_name)
        if user_define_variable_name.variable_4_name != "":
            money_pass_start_str = money_pass_start_str.replace("x4", user_define_variable_name.variable_4_name)
        if user_define_variable_name.variable_5_name != "":
            money_pass_start_str = money_pass_start_str.replace("x5", user_define_variable_name.variable_5_name)
        return money_pass_start_str

