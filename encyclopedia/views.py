from django.shortcuts import render
import markdown2
from django import forms
from django.shortcuts import redirect
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label = 'Enter Title ', max_length = 20)
    content = forms.CharField(label = 'Description', widget = forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display(request, title):
    content = util.get_entry(title)
    
    if(content is None):
        return render(request, "encyclopedia/page_not_found_error.html", {
            "title" : title + " - Wiki"
        })
    return render(request, "encyclopedia/content.html", {
        "content" : markdown2.markdown(content),"title" : title + " - Wiki"
    })

def search(request):
    title = request.GET.get('q','')
    all_entries = util.list_entries()
    if title in all_entries:
        return redirect('display', title = title)
    else:
        liist = []
        for entry in all_entries:
            if entry.find(title) is not  -1:
                liist.append(entry)
        
        return render(request, "encyclopedia/search_results.html", {
        "entries": liist
        })

def create_new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.entry_exist(title):
                return render(request, "encyclopedia/entry_already_exist_error.html", {
                "title": title
                })

            util.create_new_entry(title, content)
            return render(request, "encyclopedia/new_entry.html",{
                "form" : NewEntryForm()
            })

        return render(request, "encyclopedia/new_entry.html",{
                "form" : form
        })

    return render(request, "encyclopedia/new_entry.html", {
        "form" : NewEntryForm()
    })
