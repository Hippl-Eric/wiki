import markdown2

from django.shortcuts import render
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    entry_txt = util.get_entry(entry_name)
    entry_html = markdown2.markdown(entry_txt)
    return render(request, "encyclopedia/entry.html", {
        "entry_name": entry_name,
        "entry_content": entry_html
    })