import markdown2
import random

from django.shortcuts import render, redirect
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    entry_txt = util.get_entry(entry_name)
    if not entry_txt:
        return render(request, "encyclopedia/apology.html", {
            "message": "Sorry, the page you are looking for does not exist here."
        })
        
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

def create_ent(request, entry_bool=True, entry_title=None):
    if request.method == "POST":
        
        # Grab form submission data
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Check if entry already exists
        all_entries = util.list_entries()
        for entry in all_entries:
            if title.upper() == entry.upper():
                return render(request, "encyclopedia/create_ent.html", {
                    "entry_bool": False,
                    "entry_title": entry,
                })

        # Save new entry
        util.save_entry(title, content)

        # Redirect to entry page
        return redirect("entry", title)

    else:
        return render(request, "encyclopedia/create_ent.html", {
            "entry_bool": True,
            "entry_title": None,
        })

def edit_ent(request, entry_name):
    if request.method == "POST":
        pass
    else:
        entry_content = util.get_entry(entry_name)
        return render(request, "encyclopedia/edit_ent.html", {
            "entry_name": entry_name,
            "entry_content": entry_content,
        })

def random_ent(request):

    # Grab all entries
    all_entries = util.list_entries()

    # Choose a random index
    idx = random.randint(0, len(all_entries) - 1)

    # Return entry at index
    return redirect("entry", all_entries[idx])
