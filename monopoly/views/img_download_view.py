from django.shortcuts import render
from django.views import View

class ImgDownloadView(View):
	template_name = 'img_download.html'

	def get(self, request, *args, **kwargs):	
		context = {

		}
		return render(request, self.template_name, context=context)