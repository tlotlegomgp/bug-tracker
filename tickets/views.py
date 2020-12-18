from django.shortcuts import render

# Create your views here.

def tickets_view(request):
    context = {}
    return render(request, "tickets/tickets.html", context)