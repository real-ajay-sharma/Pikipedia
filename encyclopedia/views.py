from django.shortcuts import render
import markdown2

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

