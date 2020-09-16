import markdown2
import random

from django.shortcuts import render, redirect
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    if not util.get_entry(entry_name):
        return render(request, "encyclopedia/apology.html", {
            "message": "Sorry, the page you are looking for does not exist here."
        })
        
    entry_txt = util.get_entry(entry_name)
    entry_html = markdown2.markdown(entry_txt)
    return render(request, "encyclopedia/entry.html", {
        "entry_name": entry_name,
        "entry_content": entry_html
    })

def search(request):
    query = request.GET.get("q")
    if query:
        # Grab all entries
        all_entries = util.list_entries()

        # Check for an exact match
        for entry in all_entries:
            if query.upper() == entry.upper():
                return redirect("entry", entry)
        
        # Check for partial matches
        partial_match_list = []
        for entry in all_entries:
            if query.upper() in entry.upper():
                partial_match_list.append(entry)
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "search_results": partial_match_list,
        })

    # User did not specify a search query
    else:
        return redirect("index")

def create_ent(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "encyclopedia/create_ent.html")

def random_ent(request):

    # Grab all entries
    all_entries = util.list_entries()

    # Choose a random index
    idx = random.randint(0, len(all_entries) - 1)

    # Return entry at index
    return redirect("entry", all_entries[idx])
