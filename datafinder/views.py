from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.conf import settings
# ...
#context = {'GV': settings.GV, 'LANG': settings.LANG}
context = {}
<<<<<<< HEAD

=======
>>>>>>> 860f2d4fdb8578a2dd7f2a1ac0b0c1f2dd380a29
def detail(request, data_id):
    context['data_id'] = data_id
    return render(request, 'fetchdata/detail.html', context)

def list(request, cate_id):
    context['cate_id'] = cate_id
    context['download_list'] = [];
    
    
    
    #context['download_list'].append()
    
    
    
    
    
    #output = _("Welcome to my site.")
    
    
    
    return render(request, 'fetchdata/list.html', context)


