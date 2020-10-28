from django.shortcuts import render
from django import forms
from django.db import models 
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

class MarkDownModel(forms.Form): 
    # fields of the model 
    title = forms.CharField(max_length = 200) 
    description = forms.Textarea()

def index(request):
    if 'encyclopedia' not in request.session:
        print("debug2\n")
        request.session['encyclopedia'] = util.list_entries()

    return render(request, "encyclopedia/index.html", {
        "entries": request.session['encyclopedia']
    })

def title(request, title):
    entry = util.get_entry(title)
    return render(request, 'encyclopedia/content.html',{
        "entry":entry,
    })


def newpage(request):
    if request.method == 'POST':
        form = MarkDownModel(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["encyclopedia"]["title"]
            request.session["encyclopedia"] += [entry]
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request, "encyclopedia/newpage.html",{
                "form": form
            })

    return render(request, "encyclopedia/newpage.html",
    {
        "form" : MarkDownModel()
()
    })