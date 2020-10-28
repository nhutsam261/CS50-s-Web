from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.files import File
from . import util, forms
from random import choice


form = forms.NewSearchForm()


def index(request):
    entries = util.list_entries()

    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "form" : form,
    })

def get_page(request, title):

    entry = util.get_entry(title)
    if entry is None:
        return render(request, 'encyclopedia/error.html')

    return render(request, 'encyclopedia/titlepage.html',{
        "title": title,
        "entry": entry,
        "form": form,

    })

def search(request):
    
    if request.method == 'GET':
        form = forms.NewSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['search'].lower()
            entries = util.list_entries()
            foundFiles = [entry for entry in entries if query in entry.lower()]

            if not foundFiles:
                return render(request,"encyclopedia/search_results.html",{
                    'error' : "No results found",
                    "form":form
                })
            elif len(foundFiles) > 0 and foundFiles[0].lower() == query:
                title = foundFiles[0].lower()
                
                return get_page(request, title)
            else:
                title = [entry for entry in foundFiles if entry.lower() == query]
                if len(title) > 0:
                    return get_page(request, title[0])
                else:
                    return render(request, "encyclopedia/search_results.html",{
                        'result' : title,
                        'form' : form,
                    })



def new_page(request):
    if request.method == 'GET':
        create_form = forms.NewPageForm()
        return render(request, 'encyclopedia/create_page.html', {
            'form' : form,
            'create_form' : create_form,
        })
    else:
        create_form = forms.NewPageForm(request.POST)
        if create_form.is_valid():
            title = create_form.cleaned_data['title']
            body = create_form.cleaned_data['body']

            entries = util.list_entries()
            for entry in entries:
                if title == entry:
                    error_message = 'The title is existed\n'
                    return render(request, 'encyclopedia/create_page.html',{
                        'error_message': error_message,
                        'form':form,
                        'create_form':create_form,
                    })
            util.save_entry(title,body)
            return get_page(request, title)
        else:
            return render(request, 'encyclopedia/create_page.html',{
                'form': form,
                'create_form': create_form,
            })
def edit_page(request):
    
    pagename = request.POST.get('edit')
    content = util.get_entry(pagename)
    edit_form = forms.EditPageForm(initial={'pagename': pagename, 'body':content})
    if edit_form.is_valid():
        return render(request, 'encyclopedia/edit_page.html',{
            'title': pagename,
            'form':form,
            'edit_form': edit_form,
        })
    else:
        return render(request, 'encyclopedia/edit_page.html',{
            'title':pagename,
            'form':form,
            'edit_form': edit_form,
        })
def save_page(request):
    edit_form = forms.EditPageForm(request.POST)
    if edit_form.is_valid():
        pagename = edit_form.cleaned_data['pagename']
        body = edit_form.cleaned_data['body']

        savedPage = util.save_entry(pagename, body)
        return get_page(request, pagename)
    else:
        return render(request, 'encyclopedia/edit_page.html',{
            'form': form,
            'edit_form':edit_form,
        })
def random_page(request):

    entries = util.list_entries()

    return get_page(request, choice(entries))
