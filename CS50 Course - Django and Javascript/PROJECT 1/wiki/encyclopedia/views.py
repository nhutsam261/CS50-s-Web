from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from markdown2 import Markdown
from random import choice
from . import util

from . import form

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": form.SearchForm()

    })

# Display content given title
def entry(request, title):
    markdowner = Markdown()
    content_md = util.get_entry(title)
    if content_md is not None:
        content_html = markdowner.convert(content_md)

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "form": form.SearchForm(),
            "entry": content_html
        })
    return HttpResponse("NONE")


def search(request):
    if request.method == "GET":
        f = form.SearchForm(request.GET)
        if f.is_valid():
            entries = util.list_entries()
        
            print(entries)

            keyword = f.cleaned_data["keyword"] .lower()
            searchResult = [entry for entry in entries if keyword in entry.lower()]

            if len(searchResult) == 1:
                if len(keyword) == len(searchResult[0]): # keyword matches the entry name
                    return HttpResponseRedirect(reverse("wiki:entry", 
                                            args= [searchResult[0]]))
                # if keyword is a substring of the entry name, direct to search.html
                return render(request,"encyclopedia/search.html",{
                    "entries": searchResult,
                    "form": f
                })
            else:
                return HttpResponse("No result found")
    
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": form.SearchForm()   
        })


def create(request):
    if request.method == "POST":
        f = form.CreatePageForm(request.POST)
        if f.is_valid():
            title = f.cleaned_data["title"]
            content = f.cleaned_data["content"]

            if title in util.list_entries():
                return HttpResponse("The entry is available already")
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("wiki:index"))

    else:
        return render(request, "encyclopedia/create.html", {
            "form": form.SearchForm(),
            "create_form": form.CreatePageForm()
        })


def edit(request, title):
    if request.method == "POST":
        f = form.EditPageForm(request.POST)
        if f.is_valid():
            content = f.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:index"))
        else: return HttpResponse("Error")


    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form.SearchForm(),
        "edit_form": form.EditPageForm(initial={'content': util.get_entry(title)})
    })


def random(request):
    entries = util.list_entries()
    randomEntry = choice(entries)
    return HttpResponseRedirect(reverse("wiki:entry", args=[randomEntry]))