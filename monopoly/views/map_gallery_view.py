from django.shortcuts import render, get_object_or_404
from django.views import View
from monopoly.models import User, Map
from django.db.models import Q

class MapGalleryView(View):
	template_name = 'map_gallery.html'

	def get(self, request, *args, **kwargs):
		query = self.request.GET.get('q')
		no_search_result = ""
		if query:
			creator = User.objects.filter(Q(username=query) | Q(first_name=query)).first()
			queryset = Map.objects.filter(Q(map_name__icontains=query) | Q(creator=creator))
			if len(queryset) == 0:
				no_search_result = "查無搜尋結果"
		else:
			queryset = []
			no_search_result = ""
		"""query author"""
		query_author = self.request.GET.get('author')
		if query_author:
			creator = User.objects.filter(Q(username=query_author)).first()
			queryset = Map.objects.filter(Q(creator=creator))
			if len(queryset) == 0:
				no_search_result = "查無搜尋結果"
		
		
		context = {
		'queryset': queryset,
		'no_search_result': no_search_result,
		'query_author': query_author
		}
		return render(request, self.template_name, context=context)