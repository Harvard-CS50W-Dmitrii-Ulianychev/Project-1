import os, random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms

from . import util, forms

def index(request):
    search_query = request.GET.get("q")
    h1_title = "All Pages"
    entries = util.list_entries()
    entries_lower = [entry.lower() for entry in entries]
    if search_query:
        search_query = search_query.lower()
        if search_query in entries_lower:
            return redirect('entry', title=search_query)
        else:
            entries = [s for s in entries if search_query in s.lower()]
            if len(entries) > 0:
                h1_title = f"Search results matching your query '{search_query}'"
            else:
                h1_title = "The are no results matching your query"
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "h1_title": h1_title
    })

def entry(request, title):
    if util.get_entry(title) is not None:
        return util.render_entry(request, title)
    else:
        return render(request, "encyclopedia/404.html")
    
def get_random_entry(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return util.render_entry(request, random_entry)

def new(request):
    if request.method == "POST":
        form = forms.NewEntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data['entry_title']
            entry_content = form.cleaned_data['entry_content']

            entries = util.list_entries()

            if entry_title not in entries:
                # Create a new .md file with the entry_title as the file name
                file_path = os.path.join('entries', f"{entry_title}.md")
                with open(file_path, 'w') as file:
                    file.write(entry_content)
                return redirect('entry', title=entry_title)
            else:
                return render(request, "encyclopedia/new.html", {
                "title": "Entry with this name exists. Choose a different name.",
                "new_entry_form": form
                })
    else:
        return render(request, "encyclopedia/new.html", {
        "title": "Create New Encyclopedia Entry",
        "new_entry_form": forms.NewEntryForm()
    })


def edit(request, entry_title):
    if request.method == "POST":
        # Extract edited content from the form
        edited_content = request.POST.get('entry_content', '')

        # Save edited content to .md file
        util.save_entry(entry_title, edited_content)

        # Redirect to the edited page
        return redirect('entry', title=entry_title)
    else:
        entry_content = util.get_entry(entry_title)
        return render(request, "encyclopedia/edit.html", {
            "title": entry_title,
            "page_heading": f"Edit the entry '{entry_title}'",
            "edit_entry_form": forms.EditEntryForm(initial_content=entry_content)
        })