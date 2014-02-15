from account.models import Account
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from easydata.func.function_core import download

class HomeView(TemplateView):
    template_name="homepage.html"
    
    def get(self, *args, **kwargs):
        return super(HomeView, self).get(*args, **kwargs)
        

def change_account_language(request, pk, code):
    account = Account.objects.get(pk=pk)
    account.language = code
    account.save()
    return redirect(request.GET['next'])

def download_file(request):
    filepath = request.GET.get('filepath')
    mimetype = request.GET.get('mimetype')
    filetype = request.GET.get('filetype')
    return download(filepath, filetype=filetype, mimetype=mimetype)
