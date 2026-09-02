from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404,render
from .models import Card,Set
def catalog(request):
 qs=Card.objects.public().select_related("set"); q=request.GET.get("q","").strip(); set_slug=request.GET.get("set",""); card_type=request.GET.get("type","")
 if q: qs=qs.filter(Q(name__icontains=q)|Q(collector_number__icontains=q))
 if set_slug: qs=qs.filter(set__slug=set_slug)
 if card_type in Card.CardType.values: qs=qs.filter(card_type=card_type)
 return render(request,"cards/catalog.html",{"page_obj":Paginator(qs,24).get_page(request.GET.get("page")),"sets":Set.objects.filter(is_active=True),"q":q,"set_slug":set_slug,"card_type":card_type,"types":Card.CardType.choices})
def detail(request,slug): return render(request,"cards/detail.html",{"card":get_object_or_404(Card.objects.public().select_related("set"),slug=slug)})
