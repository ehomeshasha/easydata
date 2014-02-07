from account.models import Account
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name="homepage.html"
    
    def get(self, *args, **kwargs):
        return super(HomeView, self).get(*args, **kwargs)
        

def change_account_language(request, pk, code):
    account = Account.objects.get(pk=pk)
    account.language = code
    account.save()
    return redirect(request.GET['next'])

