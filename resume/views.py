from django.shortcuts import render

from .models import Portfolio


def resume(request):
    portfolios = Portfolio.objects.all()
    context = {'portfolios': portfolios}
    return render(request, 'resume/index.html', context=context)
