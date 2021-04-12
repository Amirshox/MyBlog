from django.shortcuts import render


def resume(request):
    context = {}
    return render(request, 'resume/index.html', context=context)
