from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.db.models import Q

from monopoly.models import Map, Cardset, Land, LandType, UserDefineVariable, UserDefineVariableName, ScoreBoardSetting, MusicSetting, BackGroundSetting, BasicSetting
from monopoly.forms.map_form import MapForm
from monopoly.forms.variable_form import VariableNameForm, VariableForm
from monopoly.forms.score_board_form import ScoreBoardForm
from monopoly.forms.music_setting_form import MusicSettingForm
from monopoly.forms.background_setting_form import BackGroundSettingForm
from monopoly.forms.basic_setting_form import BasicSettingForm
from monopoly.core.initial_value import INIT_MAP
from PIL import Image
from io import BytesIO
from django.conf import settings
import shutil
import json
import re

from azure.storage.blob import BlockBlobService
from monopoly_new.backend.custom_azure import get_account_key

class MapCreateView(View):
    #this view is for creating 
    template_name = 'map_create_view.html'

    def get(self, request, *args, **kwargs):
        form = MapForm(user=request.user)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        #create new map with default creator, id
        error_message = None
        form = MapForm(request.POST, user=request.user)
        if form.is_valid():
            print("valid")
            _map = Map.objects.create(creator=request.user)
            _map.map_name = form.cleaned_data['map_name']
            cardsets = form.cleaned_data['cardsets']
            print(cardsets)
            print(len(cardsets))
            _map.cardsets.add(*cardsets) 
            _map.save()
            self.make_default_lands(_map)
            self.make_default_user_define_variables(_map)
            self.make_default_user_define_variable_names(_map)
            self.make_default_score_board_setting(_map)
            self.make_default_music_setting(_map)
            self.make_default_background_setting(_map)
            self.make_default_basic_setting(_map)
            """if user does not select"""
            if len(cardsets) == 0:
                self.make_default_cardsets(_map)
            return HttpResponseRedirect(reverse('creator-my-maps') )
        else:
            error_message = list(form.errors.as_data()['map_name'][0])[0]
        
        context = {
            'form': form,
            'error_message': error_message,
        }
        return render(request, self.template_name, context)

    def make_default_lands(self, _map):
        for i in range(40):
            land_type = INIT_MAP[i][0]
            description = INIT_MAP[i][1]
            image_path = INIT_MAP[i][2]
            color = INIT_MAP[i][3]
            value = INIT_MAP[i][4]
            additional_parameter = ""
            variable_1_change = ""
            modal_message = ""
            if INIT_MAP[i][0] == "監獄":
                variable_1_change = INIT_MAP[i][5]
            elif INIT_MAP[i][0] == "基礎設施(不可蓋房子)":
                additional_parameter = INIT_MAP[i][5]
            elif INIT_MAP[i][0] == "自訂土地":
                modal_message = INIT_MAP[i][5]

            land_type = get_object_or_404(LandType, land_type=land_type)
            land = Land(_map = _map, pos = i, land_type = land_type, description = description, image = image_path, color=color, value = value, additional_parameter = additional_parameter, variable_1_change = variable_1_change, modal_message = modal_message)
            image_field = land.image
            img = Image.open(image_field)
            
            buffer = BytesIO()
            img.save(fp=buffer, format='PNG')
            pillow_image = ContentFile(buffer.getvalue())
            image_field.save(str(i) + ".png", InMemoryUploadedFile(
                 pillow_image,       # file
                 None,               # field_name
                 str(i) + ".png",           # file name
                 'image/png',       # content_type
                 pillow_image.tell,  # size
                 None)               # content_type_extra
            )
    def make_default_user_define_variables(self, _map):
        for i in range(4):
            UserDefineVariable.objects.create(_map = _map, player_name="Player" + str(i+1), player_index=i)
    def make_default_user_define_variable_names(self, _map):
        UserDefineVariableName.objects.create(_map = _map, variable_1_name="是否進監獄", variable_2_name="位置變數", is_variable_2_visible=False)
    def make_default_score_board_setting(self, _map):
        ScoreBoardSetting.objects.create(_map = _map)
    def make_default_music_setting(self, _map):
        MusicSetting.objects.create(_map = _map)
    def make_default_background_setting(self, _map):
        default_tile_background_img = "map/default/-1.png"
        BackGroundSetting.objects.create(_map = _map, tile_background_img = default_tile_background_img)
    def make_default_basic_setting(self, _map):
        BasicSetting.objects.create(_map = _map)
    def make_default_cardsets(self, _map):
        cardsets = Cardset.objects.filter(user = 1).filter(Q(cardset_name = "機會") | Q(cardset_name="命運"))
        _map.cardsets.add(*cardsets) 
        _map.save()


class MapEditView(View):
    #this view is for creating 
    template_name = 'map_edit_view.html'

    def get(self, request, *args, **kwargs):
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        if _map.creator != request.user:
            return HttpResponseRedirect(reverse('permission-required') )

        form = MapForm(instance=_map, user=request.user)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        #create new map with default creator, id
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        if _map.creator != request.user:
            return HttpResponseRedirect(reverse('permission-required') )
        is_delete = request.POST.get("delete", None) == "刪除"
        is_update = request.POST.get("update", None) == "更新"
        if is_update:
            form = MapForm(request.POST, user=request.user, allow_name_duplicate=True)
            if form.is_valid():
                print("valid")
                _map.map_name = form.cleaned_data['map_name']
                cardsets = form.cleaned_data['cardsets']
                _map.cardsets.clear()
                _map.cardsets.add(*cardsets) 
                _map.save()
                return HttpResponseRedirect(reverse('map-detail', kwargs={'stub': map_id}) )
        elif is_delete:
            block_blob_service = BlockBlobService(account_name='monopolyuserupload', account_key=get_account_key())
            containername = "userdata"
            foldername = "map/" + map_id
            self.delete_folder(block_blob_service, containername, foldername)
            # delete_path = settings.MEDIA_ROOT + "/map/" + map_id
            # shutil.rmtree(delete_path, ignore_errors=True)
            _map.delete()
            return HttpResponseRedirect(reverse('creator-my-maps') )

    def delete_folder(self, blob_client, containername, foldername):
        folders = [blob.name for blob in blob_client.list_blobs(containername, prefix=foldername)]
        print(folders)
        folders.sort(reverse=True, key=len)
        if len(folders) > 0:
            for folder in folders:
                blob_client.delete_blob(containername, folder)
                print("deleted folder",folder)

class MapVariableView(View):
    #this view is for creating 
    template_name = 'map_variable_view.html'

    def get(self, request, *args, **kwargs):
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        if _map.creator != request.user:
            return HttpResponseRedirect(reverse('permission-required'))

        form = VariableNameForm(instance = _map.userdefinevariablename)
        user_define_variable_name = _map.userdefinevariablename
        user_define_variables = UserDefineVariable.objects.filter(_map = _map)
        variable_form_list = []
        for i in range(len(user_define_variables)):
            variable_form = VariableForm(instance=user_define_variables[i], variable_1_name=user_define_variable_name.variable_1_name,
                variable_2_name=user_define_variable_name.variable_2_name, variable_3_name=user_define_variable_name.variable_3_name,
                variable_4_name=user_define_variable_name.variable_4_name, variable_5_name=user_define_variable_name.variable_5_name,
                player_index=i)
            variable_form_list.append(variable_form)
        context = {
            'form': form,
            'map_id': map_id,
            'user_define_variable_name': user_define_variable_name,
            'player1_variables': user_define_variables[0],
            'player2_variables': user_define_variables[1],
            'player3_variables': user_define_variables[2],
            'player4_variables': user_define_variables[3],
            'variable_form_list': variable_form_list,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        if _map.creator != request.user:
            return HttpResponseRedirect(reverse('permission-required') )

        is_update = request.POST.get("update", None) == "更新"
        is_update_player_0 = request.POST.get("update_0", None) == "更新"
        is_update_player_1 = request.POST.get("update_1", None) == "更新"
        is_update_player_2 = request.POST.get("update_2", None) == "更新"
        is_update_player_3 = request.POST.get("update_3", None) == "更新"
        user_define_variable_name = _map.userdefinevariablename
        user_define_variables = UserDefineVariable.objects.filter(_map = _map)
        if is_update:
            form = VariableNameForm(request.POST)
            if form.is_valid():
                print("valid")
                user_define_variable_name.variable_1_name = form.cleaned_data['variable_1_name']
                user_define_variable_name.variable_2_name = form.cleaned_data['variable_2_name']
                user_define_variable_name.variable_3_name = form.cleaned_data['variable_3_name']
                user_define_variable_name.variable_4_name = form.cleaned_data['variable_4_name']
                user_define_variable_name.variable_5_name = form.cleaned_data['variable_5_name']
                user_define_variable_name.variable_1_default = form.cleaned_data['variable_1_default']
                user_define_variable_name.variable_2_default = form.cleaned_data['variable_2_default']
                user_define_variable_name.variable_3_default = form.cleaned_data['variable_3_default']
                user_define_variable_name.variable_4_default = form.cleaned_data['variable_4_default']
                user_define_variable_name.variable_5_default = form.cleaned_data['variable_5_default']
                user_define_variable_name.is_variable_1_visible = form.cleaned_data['is_variable_1_visible']
                user_define_variable_name.is_variable_2_visible = form.cleaned_data['is_variable_2_visible']
                user_define_variable_name.is_variable_3_visible = form.cleaned_data['is_variable_3_visible']
                user_define_variable_name.is_variable_4_visible = form.cleaned_data['is_variable_4_visible']
                user_define_variable_name.is_variable_5_visible = form.cleaned_data['is_variable_5_visible']
                for user_define_variable in user_define_variables:
                    user_define_variable.variable_1 = user_define_variable_name.variable_1_default
                    user_define_variable.variable_2 = user_define_variable_name.variable_2_default
                    user_define_variable.variable_3 = user_define_variable_name.variable_3_default
                    user_define_variable.variable_4 = user_define_variable_name.variable_4_default
                    user_define_variable.variable_5 = user_define_variable_name.variable_5_default
                    user_define_variable.save()
                user_define_variable_name.save()
        elif is_update_player_0:
            self.update_player_variable(request, user_define_variable_name, user_define_variables, 0)
        elif is_update_player_1:
            self.update_player_variable(request, user_define_variable_name, user_define_variables, 1)
        elif is_update_player_2:
            self.update_player_variable(request, user_define_variable_name, user_define_variables, 2)
        elif is_update_player_3:
            self.update_player_variable(request, user_define_variable_name, user_define_variables, 3)
        
        return HttpResponseRedirect(reverse('map-making-variables', kwargs={'stub': map_id}) )

    def update_player_variable(self, request, user_define_variable_name, user_define_variables, player_index):
        form = VariableForm(request.POST, variable_1_name=user_define_variable_name.variable_1_name,
            variable_2_name=user_define_variable_name.variable_2_name, variable_3_name=user_define_variable_name.variable_3_name,
            variable_4_name=user_define_variable_name.variable_4_name, variable_5_name=user_define_variable_name.variable_5_name,
            player_index=0)
        if form.is_valid():
            print("valid")
            player_variable = user_define_variables.get(player_index = player_index)
            if 'variable_1' in form.cleaned_data:
                player_variable.variable_1 = form.cleaned_data['variable_1']
            if 'variable_2' in form.cleaned_data:
                player_variable.variable_2 = form.cleaned_data['variable_2']
            if 'variable_3' in form.cleaned_data:
                player_variable.variable_3 = form.cleaned_data['variable_3']
            if 'variable_4' in form.cleaned_data:
                player_variable.variable_4 = form.cleaned_data['variable_4']
            if 'variable_5' in form.cleaned_data:
                player_variable.variable_5 = form.cleaned_data['variable_5']
            player_variable.player_name = form.cleaned_data['player_name']
            player_variable.save()
  
class MapRuleView(View):
    #this view is for creating 
    template_name = 'map_rule_view.html'

    def get(self, request, *args, **kwargs):
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        variable_names = _map.userdefinevariablename
        variable_1_name = variable_names.variable_1_name
        variable_2_name = variable_names.variable_2_name
        variable_3_name = variable_names.variable_3_name
        variable_4_name = variable_names.variable_4_name
        variable_5_name = variable_names.variable_5_name
        rolled_rule_blockly = _map.rolled_rule_blockly
        context = {
            'variable_1_name': variable_1_name,
            'variable_2_name': variable_2_name,
            'variable_3_name': variable_3_name,
            'variable_4_name': variable_4_name,
            'variable_5_name': variable_5_name,
            'rolled_rule_blockly': json.dumps(rolled_rule_blockly),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        if _map.creator != request.user:
            return HttpResponseRedirect(reverse('permission-required') )
        rules = request.POST.get("rules", None)
        blockly_text = request.POST.get("blockly_text_area", None)
        _map.rolled_rule = rules
        _map.rolled_rule_blockly = blockly_text
        _map.save()
        print(rules)
        variable_names = _map.userdefinevariablename
        variable_1_name = variable_names.variable_1_name
        variable_2_name = variable_names.variable_2_name
        variable_3_name = variable_names.variable_3_name
        variable_4_name = variable_names.variable_4_name
        variable_5_name = variable_names.variable_5_name
        rolled_rule_blockly = _map.rolled_rule_blockly
        context = {
            'variable_1_name': variable_1_name,
            'variable_2_name': variable_2_name,
            'variable_3_name': variable_3_name,
            'variable_4_name': variable_4_name,
            'variable_5_name': variable_5_name,
            'rolled_rule_blockly': json.dumps(rolled_rule_blockly),
        }
        return render(request, self.template_name, context)

class MapScoreBoardView(View):
    template_name = 'map_score_board_view.html'

    def get(self, request, *args, **kwargs):
        try:
            avatar = request.user.profile.avatar
        except:
            avatar = "cat.jpeg"
        user_name = request.user.username
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        if _map.creator != request.user:
            return HttpResponseRedirect(reverse('permission-required') )
        user_define_variable_name = _map.userdefinevariablename
        form = ScoreBoardForm(instance=_map.scoreboardsetting, variable_1_name=user_define_variable_name.variable_1_name,
                variable_2_name=user_define_variable_name.variable_2_name, variable_3_name=user_define_variable_name.variable_3_name,
                variable_4_name=user_define_variable_name.variable_4_name, variable_5_name=user_define_variable_name.variable_5_name)
        score_board_setting = _map.scoreboardsetting
        other_audio_url = score_board_setting.audio_url
        background_music_setting = _map.musicsetting.background
        context = {
            'form': form,
            'map_id': map_id,
            'avatar': avatar,
            'user_name': user_name,
            'other_audio_url': other_audio_url,
            'background_music_setting': background_music_setting
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            avatar = request.user.profile.avatar
        except:
            avatar = "cat.jpeg"
        user_name = request.user.username
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        if _map.creator != request.user:
            return HttpResponseRedirect(reverse('permission-required') )

        error_message = None
        score_board_setting = _map.scoreboardsetting
        user_define_variable_name = _map.userdefinevariablename
        form = ScoreBoardForm(request.POST, variable_1_name=user_define_variable_name.variable_1_name,
                variable_2_name=user_define_variable_name.variable_2_name, variable_3_name=user_define_variable_name.variable_3_name,
                variable_4_name=user_define_variable_name.variable_4_name, variable_5_name=user_define_variable_name.variable_5_name)
        if form.is_valid():
                print("valid")
                score_board_setting.prior_variable = form.cleaned_data['prior_variable']
                score_board_setting.is_descending_order = form.cleaned_data['is_descending_order']
                score_board_setting.title = form.cleaned_data['title']
                score_board_setting.subtitle = form.cleaned_data['subtitle']
                score_board_setting.background_img_url = form.cleaned_data['background_img_url']
                score_board_setting.score_board_sound_effect = form.cleaned_data['score_board_sound_effect']                
                if score_board_setting.score_board_sound_effect == "others":
                    audio_url = request.POST.get("other_input", None)
                    if self.is_google_drive_audio(audio_url):
                        pattern = r"/d/(.*)/view\?"
                        google_id = re.search(pattern, audio_url).group(1)
                        audio_url = "https://docs.google.com/uc?export=download&id=" + google_id

                    score_board_setting.audio_url = audio_url
                elif score_board_setting.score_board_sound_effect == "background":
                    music_setting = _map.musicsetting
                    score_board_setting.audio_url = music_setting.background
                else:
                    score_board_setting.audio_url = "default/bgm/" + score_board_setting.score_board_sound_effect + ".mp3"

                score_board_setting.save()
                return HttpResponseRedirect(reverse('map-score-board-setting', kwargs={'stub': map_id}) )
        else:
            error_dict = form.errors.as_data()
            error_key = list(error_dict.keys())[0]
            error_message = list(error_dict[error_key][0])[0]
            print(error_message)
            other_audio_url = score_board_setting.audio_url
            context = {
                'form': form,
                'map_id': map_id,
                'avatar': avatar,
                'user_name': user_name,
                'error_message': error_message,
                'other_audio_url': other_audio_url
            }
            return render(request, self.template_name, context)

    def is_google_drive_audio(self, data):
        pattern = r"https://drive.google.com/.*"
        return re.match(pattern, data)

class MapMusicSettingView(View):
    template_name = 'map_music_setting_view.html'

    def get(self, request, *args, **kwargs):
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        if _map.creator != request.user:
            return HttpResponseRedirect(reverse('permission-required') )
        musicsetting = _map.musicsetting   
        form = MusicSettingForm(instance=musicsetting)
        volume_background = musicsetting.volume_background
        volume_money_deduction = musicsetting.volume_money_deduction
        volume_money_addition = musicsetting.volume_money_addition
        volume_dice = musicsetting.volume_dice
        volume_hover_button = musicsetting.volume_hover_button
        volume_build = musicsetting.volume_build
        volume_player_move = musicsetting.volume_player_move
        volume_player_teleport = musicsetting.volume_player_teleport
        volume_player_turn_over = musicsetting.volume_player_turn_over
        volume_wrong_answer = musicsetting.volume_wrong_answer
        volume_user_define_1 = musicsetting.volume_user_define_1
        volume_user_define_2 = musicsetting.volume_user_define_2
        volume_user_define_3 = musicsetting.volume_user_define_3
        volume_setting_info = {
            'volume_background': volume_background,
            'volume_money_deduction': volume_money_deduction,
            'volume_money_addition': volume_money_addition,
            'volume_dice': volume_dice,
            'volume_hover_button': volume_hover_button,
            'volume_build': volume_build,
            'volume_player_move': volume_player_move,
            'volume_player_teleport': volume_player_teleport,
            'volume_player_turn_over': volume_player_turn_over,
            'volume_wrong_answer': volume_wrong_answer,
            'volume_user_define_1': volume_user_define_1,
            'volume_user_define_2': volume_user_define_2,
            'volume_user_define_3': volume_user_define_3
        }

        context = {
            'form': form,
            'map_id': map_id,
            'volume_setting_info': json.dumps(volume_setting_info)
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        if _map.creator != request.user:
            return HttpResponseRedirect(reverse('permission-required') )

        music_setting = _map.musicsetting
        form = MusicSettingForm(request.POST)
        if form.is_valid():
            print("valid")
            music_setting.background = form.cleaned_data['background']
            music_setting.money_deduction = form.cleaned_data['money_deduction']
            music_setting.money_addition = form.cleaned_data['money_addition']
            music_setting.dice = form.cleaned_data['dice']
            music_setting.hover_button = form.cleaned_data['hover_button']
            music_setting.build = form.cleaned_data['build']
            music_setting.player_move = form.cleaned_data['player_move']
            music_setting.player_teleport = form.cleaned_data['player_teleport']
            music_setting.player_turn_over = form.cleaned_data['player_turn_over']
            music_setting.wrong_answer = form.cleaned_data['wrong_answer']
            music_setting.user_define_1 = form.cleaned_data['user_define_1']
            music_setting.user_define_2 = form.cleaned_data['user_define_2']
            music_setting.user_define_3 = form.cleaned_data['user_define_3']
            music_setting.volume_background = request.POST['vol_id_background']
            music_setting.volume_money_deduction = request.POST['vol_id_money_deduction']
            music_setting.volume_money_addition = request.POST['vol_id_money_addition']
            music_setting.volume_dice = request.POST['vol_id_dice']
            music_setting.volume_hover_button = request.POST['vol_id_hover_button']
            music_setting.volume_build = request.POST['vol_id_build']
            music_setting.volume_player_move = request.POST['vol_id_player_move']
            music_setting.volume_player_teleport = request.POST['vol_id_player_teleport']
            music_setting.volume_player_turn_over = request.POST['vol_id_player_turn_over']
            music_setting.volume_wrong_answer = request.POST['vol_id_wrong_answer']
            music_setting.volume_user_define_1 = request.POST['vol_id_user_define_1']
            music_setting.volume_user_define_2 = request.POST['vol_id_user_define_2']
            music_setting.volume_user_define_3 = request.POST['vol_id_user_define_3']
            print(request.POST)
            music_setting.save()
            return HttpResponseRedirect(reverse('music-setting', kwargs={'stub': map_id}) )
        else:
            error_dict = form.errors.as_data()
            error_key = list(error_dict.keys())[0]
            error_message = list(error_dict[error_key][0])[0]
            
        context = {
            'form': form,
            'map_id': map_id,
            'error_message': error_message
        }
        return render(request, self.template_name, context)

class MapBackgroundSettingView(View):
    template_name = 'map_background_setting_view.html'

    def get(self, request, *args, **kwargs):
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        if _map.creator != request.user:
            return HttpResponseRedirect(reverse('permission-required') )
        form = BackGroundSettingForm(instance=_map.backgroundsetting)
        context = {
            'form': form,
            'map_id': map_id,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        if _map.creator != request.user:
            return HttpResponseRedirect(reverse('permission-required') )
        background_setting = _map.backgroundsetting
        form = BackGroundSettingForm(request.POST, request.FILES)
        if form.is_valid():
            print("valid")
            background_setting.background_img_url = form.cleaned_data['background_img_url']
            if form.cleaned_data['tile_background_img']:
                background_setting.tile_background_img.delete()
                background_setting.tile_background_img = form.cleaned_data['tile_background_img']
            background_setting.modal_background_img_url = form.cleaned_data['modal_background_img_url']
            background_setting.land_background_color = form.cleaned_data['land_background_color']
            background_setting.land_text_color = form.cleaned_data['land_text_color']
            background_setting.save()
            return HttpResponseRedirect(reverse('background-setting', kwargs={'stub': map_id}) )
        else:
            error_dict = form.errors.as_data()
            error_key = list(error_dict.keys())[0]
            error_message = list(error_dict[error_key][0])[0]
            context = {
                'form': form,
                'map_id': map_id,
                'error_message': error_message
            }
            return render(request, self.template_name, context)

class MapBasicSettingView(View):
    template_name = 'map_basic_setting_view.html'

    def get(self, request, *args, **kwargs):
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        if _map.creator != request.user:
            return HttpResponseRedirect(reverse('permission-required') )
        basicsetting = _map.basicsetting
        form = BasicSettingForm(instance=basicsetting)
        ratio_rent_vs_price = basicsetting.ratio_rent_vs_price
        ratio_rent_vs_price_for_house = basicsetting.ratio_rent_vs_price_for_house
        rent_constant = basicsetting.rent_constant
        ratio_rent_vs_price_infra = basicsetting.ratio_rent_vs_price_infra
        ratio_rent_vs_price_infra_for_same_category = basicsetting.ratio_rent_vs_price_infra_for_same_category
        rent_constant_infra = basicsetting.rent_constant_infra
        context = {
            'form': form,
            'map_id': map_id,
            'ratio_rent_vs_price': ratio_rent_vs_price,
            'ratio_rent_vs_price_for_house': ratio_rent_vs_price_for_house,
            'rent_constant': rent_constant,
            'ratio_rent_vs_price_infra': ratio_rent_vs_price_infra,
            'ratio_rent_vs_price_infra_for_same_category': ratio_rent_vs_price_infra_for_same_category,
            'rent_constant_infra': rent_constant_infra
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        map_id = kwargs['stub']
        _map = Map.objects.get(id=map_id)
        if _map.creator != request.user:
            return HttpResponseRedirect(reverse('permission-required') )
        basicsetting = _map.basicsetting
        form = BasicSettingForm(request.POST)
        if form.is_valid():
            print("valid")
            basicsetting.money_initial = form.cleaned_data['money_initial']
            basicsetting.money_pass_start = form.cleaned_data['money_pass_start']
            basicsetting.house_construction_cost = form.cleaned_data['house_construction_cost']
            basicsetting.num_of_house_equal_hotel = form.cleaned_data['num_of_house_equal_hotel']
            basicsetting.welcome_info = form.cleaned_data['welcome_info']
            basicsetting.game_process = form.cleaned_data['game_process']
            basicsetting.ratio_rent_vs_price = request.POST['ratio_rent_vs_price']
            basicsetting.ratio_rent_vs_price_for_house = request.POST['ratio_rent_vs_price_for_house']
            basicsetting.rent_constant = request.POST['rent_constant']
            basicsetting.ratio_rent_vs_price_infra = request.POST['ratio_rent_vs_price_infra']
            basicsetting.ratio_rent_vs_price_infra_for_same_category = request.POST['ratio_rent_vs_price_infra_for_same_category']
            basicsetting.rent_constant_infra = request.POST['rent_constant_infra']
            is_post_valid = self.is_valid_from_post(request.POST['ratio_rent_vs_price'], request.POST['ratio_rent_vs_price_for_house'], request.POST['rent_constant'], request.POST['ratio_rent_vs_price_infra'], request.POST['ratio_rent_vs_price_infra_for_same_category'], request.POST['rent_constant_infra'])
            if is_post_valid:
                basicsetting.save()
                return HttpResponseRedirect(reverse('basic-setting', kwargs={'stub': map_id}) )
            else:
                error_message = "只可以輸入數字喔"
        else:
            error_dict = form.errors.as_data()
            error_key = list(error_dict.keys())[0]
            error_message = list(error_dict[error_key][0])[0]
        context = {
            'form': form,
            'map_id': map_id,
            'error_message': error_message,
            'ratio_rent_vs_price': request.POST['ratio_rent_vs_price'],
            'ratio_rent_vs_price_for_house': request.POST['ratio_rent_vs_price_for_house'],
            'rent_constant': request.POST['rent_constant'],
            'ratio_rent_vs_price_infra': request.POST['ratio_rent_vs_price_infra'],
            'rent_constant_infra': request.POST['rent_constant_infra']
        }
        return render(request, self.template_name, context)

    def is_valid_from_post(self, ratio_rent_vs_price, ratio_rent_vs_price_for_house, rent_constant, ratio_rent_vs_price_infra, ratio_rent_vs_price_infra_for_same_category, rent_constant_infra):
        ratio_rent_vs_price = ratio_rent_vs_price.replace(".", "", 1)
        ratio_rent_vs_price_for_house = ratio_rent_vs_price_for_house.replace(".", "", 1)
        rent_constant = rent_constant.replace(".", "", 1)
        ratio_rent_vs_price_infra = ratio_rent_vs_price_infra.replace(".", "", 1)
        ratio_rent_vs_price_infra_for_same_category = ratio_rent_vs_price_infra_for_same_category.replace(".", "", 1)
        rent_constant_infra = rent_constant_infra.replace(".", "", 1)
        return ratio_rent_vs_price.isdigit() and ratio_rent_vs_price_for_house.isdigit() and rent_constant.isdigit() and ratio_rent_vs_price_infra.isdigit() and ratio_rent_vs_price_infra_for_same_category.isdigit() and rent_constant_infra.isdigit()