from django.shortcuts import render
import markdown2

from django.shortcuts import redirect
from . import util


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

