from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from monopoly.models import Cardset, ChanceCard
from monopoly.forms.cardset_form import CardsetForm

class CardsetCreateView(View):
    #this view is for creating 
    template_name = 'cardset_create_view.html'

    def get(self, request, *args, **kwargs):
        form = CardsetForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        #create new cardset with default user, id
        error_message = None
        cardset_name = request.POST.get("cardset_name", None)
        cardset = Cardset(user = request.user, cardset_name=cardset_name)
        form = CardsetForm(request.POST, instance=cardset, user=request.user)
        if form.is_valid():
            print("valid")
            cardset.cardset_name = form.cleaned_data['cardset_name']
            cardset.save()
            return HttpResponseRedirect(reverse('creator-my-cardsets') )
        else:
            error_message = list(form.errors.as_data()['cardset_name'][0])[0]
        
        context = {
            'form': form,
            'cardset': cardset,
            'error_message': error_message,
        }
        return render(request, self.template_name, context)