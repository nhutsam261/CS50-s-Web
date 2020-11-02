from django.shortcuts import render
from . import forms
from . import util
from random import choice
import markdown2

# insert the search to all page
form = forms.NewSearchForm()
def index(request):
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":form,
    })

def get_pages(request, entries):
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "form":form,
    })

def get_page(request, title):
    print("title: ", title)
    content = util.get_entry(title)
    print(content)
    if content is None:
        
        
        return render(request, "encyclopedia/error.html", {
            "title" : title,
            "form":form,
        })
    markdowner = markdown2.Markdown()
    md2html = markdowner.convert(content)
    return render(request, "encyclopedia/page.html", {
        'title' : title,
        "content" : md2html,
        "form":form,
    })

def search(request):
    if request.method == 'GET':
        form = forms.NewSearchForm(request.GET)
        if form.is_valid():
            
            title = form.cleaned_data['search'].lower()
            
            print(f'search the {title}')
            entries = util.list_entries()
            foundEntries = [entry for entry in entries if title in entry.lower()]
            if not foundEntries:
                return render(request, "encyclopedia/error.html", {
                    "title": title,
                    "form":form,
                })
            elif len(foundEntries)==1:
                return get_page(request, foundEntries[0])
            else:
                return get_pages(request, foundEntries)
                

    if len(foundEntries) == 0:
        return render(request, "encyclopedia/error.html", {
            "title" : title,
            "form":form,
        })
    else:
        return get_pages(request, foundEntries)


def create(request):
    if request.method == 'GET':
        # request for a new form
        create_form = forms.NewPageForm()
        return render(request, 'encyclopedia/create.html',{
            'create_form' : create_form,
            "form":form,

        })
    else:
        create_form = forms.NewPageForm(request.POST)
        if create_form.is_valid():
            title = create_form.cleaned_data['pagename']
            body = create_form.cleaned_data['body']
            entries = util.list_entries()
            for entry in entries:
                if entry == title:
                    error_message  ="This entry is existed, please try other entry's name "
                    return render(request, 'encyclopedia/error.html',{
                        'error' : error_message,
                        "form":form,
                    })

            util.save_entry(title, body)
            return get_page(request, title)
        else:
            return render(request, 'encyclopedia/create.html', {
                'create_form': create_form,
                "form":form,
            })


def edit(request):
    print("edit pageeeeeeeeeeee")
    title = request.POST.get('edit')
    print('title edit: ', title)
    content = util.get_entry(title)
    print('content edit:', content)

    edit_form = forms.EditPageForm(initial={'pagename':title, 'body':content})
    return render(request, 'encyclopedia/edit.html',{
            'title':title,
            'edit_form':edit_form,
            "form":form,
    })

def save(request):
    edit_form = forms.EditPageForm(request.POST)
    if edit_form.is_valid():
        title = edit_form.cleaned_data['pagename']
        body = edit_form.cleaned_data['body']
        util.save_entry(title, body)
        return get_page(request, title)
    return render(request, 'encyclopedia/edit.html', {
        'title': title,
        'edit_form' : edit_form,
        "form":form,
    })
def random(request):
    entries = util.list_entries()
    randomEntry = choice(entries)
    return get_page(request, randomEntry)