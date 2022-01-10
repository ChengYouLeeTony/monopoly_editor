from django.shortcuts import render, get_object_or_404
from django.views import View
from monopoly.models import MusicAuthor, MusicCollection
from django.core.paginator import Paginator

class MusicListView(View):
	template_name = 'music_list.html'

	def get(self, request, *args, **kwargs):
		author_capitalize = ""
		if "_" in kwargs['author']:
			author_capitalize = " ".join([name.capitalize() for name in kwargs['author'].split("_")])
		elif "-" in kwargs['author']:
			author_capitalize = "".join([name.capitalize() for name in kwargs['author'].split("-")])
		elif kwargs['author'] == "se":
			author_capitalize = "default/se"
		author = get_object_or_404(MusicAuthor, name=author_capitalize)
		credit_url = author.credit_url
		music_collection = MusicCollection.objects.filter(author=author)
		paginator = Paginator(music_collection, 7)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context = {
			'music_collection':  music_collection,
			'author': author,
			'credit_url': credit_url,
			'page_obj': page_obj
		}
		return render(request, self.template_name, context=context)