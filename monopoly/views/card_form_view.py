from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from monopoly.models import Cardset, ChanceCard
from monopoly.forms.card_form import CardForm

class CardCreateView(View):
    #this view is for creating 
    template_name = 'card_create_view.html'

    def get(self, request, *args, **kwargs):
        form = CardForm()
        cardset = get_object_or_404(Cardset, id = kwargs['stub'])
        """test if the user is same as cardsetowner"""
        if cardset.user != request.user:
            return HttpResponseRedirect(reverse('permission-required') )
        background_img_url = cardset.background_img_url
        context = {
            'form': form,
            'uuid': kwargs['stub'],
            'background_img_url': background_img_url
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        #create new card with default cardset
        cardset = get_object_or_404(Cardset, id = kwargs['stub'])
        """test if the user is same as cardsetowner"""
        if cardset.user != request.user:
            return HttpResponseRedirect(reverse('permission-required') )
        card = ChanceCard(cardset = cardset)
        form = CardForm(request.POST, instance = card)
        if form.is_valid():
            print("valid")
            card.title = form.cleaned_data['title']
            card.subtitle = form.cleaned_data['subtitle']
            card.description = form.cleaned_data['description']
            card.money_addition = form.cleaned_data['money_addition']
            card.money_deduction = form.cleaned_data['money_deduction']
            card.stop_round = form.cleaned_data['stop_round']
            card.variable_1_change = form.cleaned_data['variable_1_change']
            card.variable_2_change = form.cleaned_data['variable_2_change']
            card.variable_3_change = form.cleaned_data['variable_3_change']
            card.variable_4_change = form.cleaned_data['variable_4_change']
            card.variable_5_change = form.cleaned_data['variable_5_change']
            card.is_multiple_choice = form.cleaned_data['is_multiple_choice']
            if card.is_multiple_choice == True:
                card.multiple_choice_1 = form.cleaned_data['multiple_choice_1']
                card.multiple_choice_2 = form.cleaned_data['multiple_choice_2']
                card.multiple_choice_3 = form.cleaned_data['multiple_choice_3']
                card.multiple_choice_4 = form.cleaned_data['multiple_choice_4']
                card.multiple_choice_answer = form.cleaned_data['multiple_choice_answer']
                card.money_deduction_when_wrong_answer = form.cleaned_data['money_deduction_when_wrong_answer']
            card.save()
            return HttpResponseRedirect(reverse('cardset-detail', kwargs={'stub': cardset.id}) )
        else:
            error_message = '算式有誤請重新輸入'
            background_img_url = card.cardset.background_img_url
        
            context = {
                'form': form,
                'error_message': error_message,
                'uuid': kwargs['stub'],
                'background_img_url': background_img_url
            }
            return render(request, self.template_name, context)

class CardEditView(View):
    #this view is for updating and delete
    template_name = 'card_edit_view.html'

    def get(self, request, *args, **kwargs):
        cardset = get_object_or_404(Cardset, id = kwargs['stub'])
        """test if the user is same as cardsetowner"""
        if cardset.user != request.user:
            return HttpResponseRedirect(reverse('permission-required'))
        background_img_url = cardset.background_img_url

        card = get_object_or_404(cardset.chancecard_set, id = kwargs['card_id'])
        form = CardForm(instance = card)
        context = {
            'form': form,
            'uuid': kwargs['stub'],
            'background_img_url': background_img_url
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """determine if the request is delete or update"""
        is_delete = request.POST.get("delete", None) == "刪除卡片"
        is_update = request.POST.get("update", None) == "確認更新"

        cardset = get_object_or_404(Cardset, id = kwargs['stub'])
        card = get_object_or_404(cardset.chancecard_set, id = kwargs['card_id'])
        """test if the user is same as cardsetowner"""
        if cardset.user != request.user:
            return HttpResponseRedirect(reverse('permission-required') )

        if is_update:
            form = CardForm(request.POST, instance = card)
            if form.is_valid():
                print("valid")
                card.title = form.cleaned_data['title']
                card.subtitle = form.cleaned_data['subtitle']
                card.description = form.cleaned_data['description']
                card.money_addition = form.cleaned_data['money_addition']
                card.money_deduction = form.cleaned_data['money_deduction']
                card.stop_round = form.cleaned_data['stop_round']
                card.variable_1_change = form.cleaned_data['variable_1_change']
                card.variable_2_change = form.cleaned_data['variable_2_change']
                card.variable_3_change = form.cleaned_data['variable_3_change']
                card.variable_4_change = form.cleaned_data['variable_4_change']
                card.variable_5_change = form.cleaned_data['variable_5_change']
                card.is_multiple_choice = form.cleaned_data['is_multiple_choice']
                if card.is_multiple_choice == True:
                    card.multiple_choice_1 = form.cleaned_data['multiple_choice_1']
                    card.multiple_choice_2 = form.cleaned_data['multiple_choice_2']
                    card.multiple_choice_3 = form.cleaned_data['multiple_choice_3']
                    card.multiple_choice_4 = form.cleaned_data['multiple_choice_4']
                    card.multiple_choice_answer = form.cleaned_data['multiple_choice_answer']
                    card.money_deduction_when_wrong_answer = form.cleaned_data['money_deduction_when_wrong_answer']
                card.save()
                return HttpResponseRedirect(reverse('cardset-detail', kwargs={'stub': cardset.id}) )
            else:
                error_dict = form.errors.as_data()
                error_key = list(error_dict.keys())[0]
                error_message = list(error_dict[error_key][0])[0]
                background_img_url = card.cardset.background_img_url
                context = {
                    'form': form,
                    'error_message': error_message,
                    'uuid': kwargs['stub'],
                    'background_img_url': background_img_url
                }
                return render(request, self.template_name, context)
        elif is_delete:
            print('delete')
            card.delete()
            return HttpResponseRedirect(reverse('cardset-detail', kwargs={'stub': cardset.id}) )
            
     