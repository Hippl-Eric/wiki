import markdown2
import random

from django.shortcuts import render, redirect
from . import util


def index(request):
    """
    Render a list of all wiki entries.
    """

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    """
    Render the entry page requested via GET.  If entry does not exist, render appology message.
    """

    # Grab entry file
    entry_txt = util.get_entry(entry_name)

    # Return appology if entry does not exist
    if not entry_txt:
        return render(request, "encyclopedia/apology.html", {
            "message": "Sorry, the page you are looking for does not exist here."
        })

    # Else return entry page        
    entry_html = markdown2.markdown(entry_txt)
    return render(request, "encyclopedia/entry.html", {
        "entry_name": entry_name,
        "entry_content": entry_html
    })

def search(request):
    """
    Search bar located in sidebar.  Returns an entry page if user provides an exact match.  Otherwise, returns a list of possible entries.  Not case sensitive.
    """

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
    """
    Allow user to create new wiki entries via form submission.  If entry name is already taken, user is prompted with an error message.  Otherwise the new entry is created, and the user is redirected to the entry page.
    """

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
    """
    All entries include an edit entry link.  Existing entry content is loaded into a text area.  Submitted edits modify the existing entry file, and redirect user to updated entry page.
    """
    
    if request.method == "POST":

        # Grab form submission data
        content = request.POST.get("content")

        # Save modified entry
        util.save_entry(entry_name, content)

        # Redirect to entry page
        return redirect("entry", entry_name)

    else:

        # Return the edit entry page
        entry_content = util.get_entry(entry_name)
        return render(request, "encyclopedia/edit_ent.html", {
            "entry_name": entry_name,
            "entry_content": entry_content,
        })

def random_ent(request):
    """
    Random entry link in sidebar.  Return random entry page to user.
    """

    # Grab all entries
    all_entries = util.list_entries()

    # Choose a random index
    idx = random.randint(0, len(all_entries) - 1)

    # Return entry at index
    return redirect("entry", all_entries[idx])
