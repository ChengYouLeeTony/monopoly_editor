from django.shortcuts import render, get_object_or_404
from django.views import View

class TutorialView(View):
	template_name = 'tutorial.html'

	def get(self, request, *args, **kwargs):
		context = {
		}
		return render(request, self.template_name, context=context)