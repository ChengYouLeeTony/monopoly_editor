from django.shortcuts import render
from django.views import View

class ThanksView(View):
	template_name = 'thanks.html'

	def get(self, request, *args, **kwargs):	
		context = {

		}
		return render(request, self.template_name, context=context)