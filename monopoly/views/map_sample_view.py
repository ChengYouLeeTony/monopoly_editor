from django.shortcuts import render
from django.views import View
from monopoly.models import Map
from django.db.models import Q

class MapSampleView(View):
	template_name = 'map_sample.html'

	def get(self, request, *args, **kwargs):
		sample_maps = Map.objects.filter(creator= 1).filter(Q(map_name = "機會與命運") | Q(map_name = "哈利波特魔法世界(選擇題)"))
		context = {
			'sample_maps':  sample_maps,
		}
		return render(request, self.template_name, context=context)