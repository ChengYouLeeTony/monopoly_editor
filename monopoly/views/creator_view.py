from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from django.views import generic
from monopoly.models import Profile, Cardset, ChanceCard, Map, Land, UserDefineVariable, UserDefineVariableName
from django.urls import reverse
from monopoly.forms.cardset_form import CardsetForm
from monopoly.forms.land_form import LandForm
from django.http import HttpResponseRedirect
import json
from monopoly.core.make_land_image import *
from copy import deepcopy
from PIL import Image
from io import BytesIO
from django.conf import settings

class CreatorHomeView(View):
	template_name = 'creator_home.html'

	def get(self, request, *args, **kwargs):
		print("request.path:", request.path)
		user_name = request.user.username
		user_id = request.user.id
		user_cardsets = Cardset.objects.filter(user= user_id)
		context = {
			'user_name':  user_name,
			'user_cardsets':  user_cardsets,
		}

		return render(request, self.template_name, context=context)

class CreatorMyCardsetsListView(View):
	template_name = 'creator_my_cardsets_list.html'

	def get(self, request, *args, **kwargs):
		user_cardsets = Cardset.objects.filter(user= request.user)
		context = {
			'user_cardsets':  user_cardsets,
		}
		return render(request, self.template_name, context=context)

	def post(self, request, *args, **kwargs):
		cardset_id = request.POST.get("carset-id", None)
		error_message = None
		user_cardsets = Cardset.objects.filter(user= request.user)
		try:
			external_cardset = Cardset.objects.get(id=cardset_id)
			new_cardset_name = external_cardset.cardset_name + "({creator_name})".format(creator_name=external_cardset.user)
			new_cardset = Cardset.objects.create(user = request.user, cardset_name = new_cardset_name)
			external_cards = ChanceCard.objects.filter(cardset=external_cardset)
			for card in external_cards:
				chance_card_object = deepcopy(card)
				card.id = None
				card.cardset = new_cardset
				card.save()
		except:
			error_message = "此卡片集ID不存在"
		context = {
			'user_cardsets':  user_cardsets,
			'error_message': error_message,
		}
		return render(request, self.template_name, context=context)

class CreatorCardsetDetailView(View):
	template_name = 'creator_cardset_detail.html'

	def get(self, request, *args, **kwargs):
		cardset = get_object_or_404(Cardset, id = kwargs['stub'])
		chance_card_len = len(cardset.chancecard_set.all())
		is_self_cardset = (cardset.user == request.user)
		uuid = cardset.id
		context = {
			'cardset': cardset,
			'is_self_cardset': is_self_cardset,
			'uuid': uuid,
			'chance_card_len': chance_card_len
		}
		return render(request, self.template_name, context=context)

	def post(self, request, *args, **kwargs):
		#update, delete cardset
		is_delete = request.POST.get("delete", None) == "刪除"
		is_update = request.POST.get("update", None) == "更新"
		delete_card_id = request.POST.get("delete-card", None)
		cardset = get_object_or_404(Cardset, id = kwargs['stub'])
		chance_card_len = len(cardset.chancecard_set.all())
		uuid = cardset.id
		
		error_message = None
		success_message = None
		if is_delete:
			if len(cardset.map_set.all()) == 0:
				cardset.delete()
				return HttpResponseRedirect(reverse('creator-my-cardsets'))
			else:
				error_message = "此卡片集與地圖相關聯，無法刪除請先取消和地圖的關聯"
		elif is_update:
			form = CardsetForm(request.POST, instance=cardset, user=request.user)
			if form.is_valid():
				print("valid")
				cardset.cardset_name = form.cleaned_data['cardset_name']
				cardset.background_img_url = form.cleaned_data['background_img_url']
				cardset.save()
				success_message = "已成功更新卡片集名稱"
			else:
				error_message = list(form.errors.as_data()['background_img_url'][0])[0]
		elif delete_card_id != None:
			try:
				related_cards = cardset.chancecard_set.all()
				delete_card = related_cards.get(id = delete_card_id)
				delete_card.delete()
			except:
				pass


		context = {
			'is_self_cardset': True,
			'cardset': cardset,
			'error_message': error_message,
			'success_message': success_message,
			'uuid': uuid,
			'chance_card_len': chance_card_len
		}
		return render(request, self.template_name, context)

class PermissionRequiredView(View):
	template_name = 'creator_permission_required.html'

	def get(self, request, *args, **kwargs):
		permission_required_message = '您沒有此項目的編輯權限'
		context = {
			'permission_required_message':  permission_required_message,
		}
		return render(request, self.template_name, context=context)

class CreatorMyMapsListView(View):
	template_name = 'creator_my_maps_list.html'

	def get(self, request, *args, **kwargs):
		user_maps = Map.objects.filter(creator= request.user)
		context = {
			'user_maps':  user_maps,
		}
		return render(request, self.template_name, context=context)

	def post(self, request, *args, **kwargs):
		map_id = request.POST.get("map-id", None)
		error_message = None
		user_maps = Map.objects.filter(creator= request.user)
		try:
			external_map = Map.objects.get(id=map_id)
			new_map_name = external_map.map_name + "({creator_name})".format(creator_name=external_map.creator)
			new_map_rolled_rule = external_map.rolled_rule
			new_map_rolled_rule_blockly = external_map.rolled_rule_blockly
			new_map = Map.objects.create(creator = request.user, map_name = new_map_name, rolled_rule = new_map_rolled_rule, rolled_rule_blockly = new_map_rolled_rule_blockly)
			"""copy related cardsets"""
			external_map_cardsets = external_map.cardsets.all()
			for external_cardset in external_map_cardsets:
				new_cardset_name = external_cardset.cardset_name + "({creator_name})".format(creator_name=external_cardset.user)
				new_cardset = Cardset.objects.create(user = request.user, cardset_name = new_cardset_name)
				external_cards = ChanceCard.objects.filter(cardset=external_cardset)
				for card in external_cards:
					chance_card_object = deepcopy(card)
					card.id = None
					card.cardset = new_cardset
					card.save()
				new_map.cardsets.add(new_cardset)
			"""copy related lands"""
			external_lands = Land.objects.filter(_map=external_map)
			for i, land in enumerate(external_lands):
				land_object = deepcopy(land)
				land_object.id = None
				land_object._map = new_map
				"""copy land images from external lands"""
				image_field = land_object.image
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
			"""copy related UserDefineVariable"""
			external_user_define_variables = UserDefineVariable.objects.filter(_map=external_map)
			for external_user_define_variable in external_user_define_variables:
				user_define_variable_object = deepcopy(external_user_define_variable)
				user_define_variable_object.id = None
				user_define_variable_object._map = new_map
				user_define_variable_object.save()

			"""copy related UserDefineVariableName"""
			external_user_define_variable_name = external_map.userdefinevariablename
			new_user_define_variable_name = deepcopy(external_user_define_variable_name)
			new_user_define_variable_name.id = None
			new_user_define_variable_name._map = new_map
			new_user_define_variable_name.save()

			"""copy related ScoreBoardSetting"""
			external_score_board_setting = external_map.scoreboardsetting
			new_score_board_setting = deepcopy(external_score_board_setting)
			new_score_board_setting.id = None
			new_score_board_setting._map = new_map
			new_score_board_setting.save()

			"""copy related BackGroundSetting"""
			external_background_setting = external_map.backgroundsetting
			new_background_setting = deepcopy(external_background_setting)
			new_background_setting.id = None
			new_background_setting._map = new_map
			new_background_setting.save()

			"""copy related BasicSetting"""
			external_basic_setting = external_map.basicsetting
			new_basic_setting = deepcopy(external_basic_setting)
			new_basic_setting.id = None
			new_basic_setting._map = new_map
			new_basic_setting.save()

			"""copy related MusicSetting"""
			external_music_setting = external_map.musicsetting
			new_music_setting = deepcopy(external_music_setting)
			new_music_setting.id = None
			new_music_setting._map = new_map
			new_music_setting.save()
		except Exception as e:
			print(e)
			error_message = "此地圖ID不存在"
		context = {
			'user_maps':  user_maps,
			'error_message': error_message,
		}
		return render(request, self.template_name, context=context)

class CreatorMapDetailView(View):
	template_name = 'creator_map_detail.html'

	def get(self, request, *args, **kwargs):
		_map = get_object_or_404(Map, id= kwargs['stub'])
		lands = Land.objects.filter(_map= _map)
		land_form_list = []
		"""only owner can edit"""
		if _map.creator != request.user:
			self.template_name = 'creator_map_detail_guest.html'
		else:
			"""land form"""
			for i in range(len(lands)):
				user_define_variable_name = _map.userdefinevariablename
				land_form = LandForm(instance=lands[i], pos="pos" + str(lands[i].pos), variable_1_name=user_define_variable_name.variable_1_name,
                variable_2_name=user_define_variable_name.variable_2_name, variable_3_name=user_define_variable_name.variable_3_name,
                variable_4_name=user_define_variable_name.variable_4_name, variable_5_name=user_define_variable_name.variable_5_name)
				land_form_list.append(land_form)

		lands_list = []
		for i in range(len(lands)):
			pos = lands[i].pos
			description = lands[i].description
			land_type = lands[i].land_type.land_type
			value = lands[i].value
			color = lands[i].color
			is_use_upload_image = lands[i].is_use_upload_image
			image = str(lands[i].image)
			additional_parameter = lands[i].additional_parameter
			lands_list.append((pos, description, land_type, value, color, is_use_upload_image, image, additional_parameter))
		lands_list.sort(key = lambda s: s[0])
		cardsets = _map.cardsets.all().order_by('cardset_name')
		uuid = _map.id
		context = {
			'map': _map,
			'lands_list': json.dumps(lands_list),
			'cardsets': cardsets,
			'uuid': uuid,
			'land_form_list': land_form_list,
			'user': request.user,
		}
		return render(request, self.template_name, context=context)

	def post(self, request, *args, **kwargs):
		"""when the creator press update button"""
		_map = get_object_or_404(Map, id= kwargs['stub'])
		lands = Land.objects.filter(_map= _map)
		land_form_list = []
		"""update land and make new image"""
		update_pos_str = list(request.POST.items())[-1][0]
		# print(list(request.POST.items()))
		update_pos = int(update_pos_str[10:])
		update_land = lands.get(pos=update_pos)

		error_message = None
		user_define_variable_name = _map.userdefinevariablename
		form = LandForm(request.POST, request.FILES, pos=update_land.pos, variable_1_name=user_define_variable_name.variable_1_name,
            variable_2_name=user_define_variable_name.variable_2_name, variable_3_name=user_define_variable_name.variable_3_name,
            variable_4_name=user_define_variable_name.variable_4_name, variable_5_name=user_define_variable_name.variable_5_name)
		if form.is_valid():
			print("valid")
			update_land.description = form.cleaned_data['description']
			update_land.land_type = form.cleaned_data['land_type']
			update_land.value = form.cleaned_data['value']
			update_land.color = form.cleaned_data['color']
			if form.cleaned_data['modal_message']:
				update_land.modal_message = form.cleaned_data['modal_message']
			update_land.is_use_upload_image = form.cleaned_data['is_use_upload_image']
			if form.cleaned_data['image'] and form.cleaned_data['is_use_upload_image'] == True:
				print("change the new image")
				update_land.image.delete()
				update_land.image = form.cleaned_data['image']
			if 'variable_1_change' in form.cleaned_data:
				update_land.variable_1_change = form.cleaned_data['variable_1_change']
			if 'variable_2_change' in form.cleaned_data:
				update_land.variable_2_change = form.cleaned_data['variable_2_change']
			if 'variable_3_change' in form.cleaned_data:
				update_land.variable_3_change = form.cleaned_data['variable_3_change']
			if 'variable_4_change' in form.cleaned_data:
				update_land.variable_4_change = form.cleaned_data['variable_4_change']
			if 'variable_5_change' in form.cleaned_data:
				update_land.variable_5_change = form.cleaned_data['variable_5_change']
			update_land.additional_parameter = form.cleaned_data['additional_parameter']

			update_land.save()
			if str(update_land.land_type) != "自訂土地" and form.cleaned_data['is_use_upload_image'] == False:
				make_one_land_image(update_land, _map.backgroundsetting.land_background_color, _map.backgroundsetting.land_text_color)

			return HttpResponseRedirect(reverse('map-detail', kwargs={'stub': kwargs['stub']}) )
		else:
			error_message = '算式有誤請重新輸入'
			"""land form"""
			for i in range(len(lands)):
				user_define_variable_name = _map.userdefinevariablename
				land_form = LandForm(instance=lands[i], pos="pos" + str(lands[i].pos), variable_1_name=user_define_variable_name.variable_1_name,
                variable_2_name=user_define_variable_name.variable_2_name, variable_3_name=user_define_variable_name.variable_3_name,
                variable_4_name=user_define_variable_name.variable_4_name, variable_5_name=user_define_variable_name.variable_5_name)
				land_form_list.append(land_form)
			
			lands_list = []
			for i in range(len(lands)):
				pos = lands[i].pos
				description = lands[i].description
				land_type = lands[i].land_type.land_type
				value = lands[i].value
				color = lands[i].color
				is_use_upload_image = lands[i].is_use_upload_image
				image = str(lands[i].image)
				additional_parameter = lands[i].additional_parameter
				lands_list.append((pos, description, land_type, value, color, is_use_upload_image, image, additional_parameter))
			lands_list.sort(key = lambda s: s[0])
			cardsets = _map.cardsets.all().order_by('cardset_name')
			uuid = _map.id
			context = {
				'map': _map,
				'lands_list': json.dumps(lands_list),
				'cardsets': cardsets,
				'uuid': uuid,
				'land_form_list': land_form_list,
				'user': request.user,
				'error_message': error_message,
			}
			return render(request, self.template_name, context=context)