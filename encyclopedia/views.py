from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from . import util

entries = [
    "CSS","Django","Git","HTML","Python"
]

class NewFormEntry(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(max_length=500)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request,title):
    try:
        return HttpResponse(util.get_entry(title))
    except FileNotFoundError:
        return render(request,"encyclopedia/error.html",{
            "title":title
        })

def create(request):
    if request.method == "POST":
        form = NewFormEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            check = True
            for entry in entries:
                if f"{title}.md" == f"{entry}.md":
                    check = False
                    return render(request, "encyclopedia/duplication.html",{
                        "title":title
                    })
            if check == True:
                entries.append(f"{title}")
                util.save_entry(title,content)
                return HttpResponseRedirect("/wiki")
        else:
            return render(request, "/create", {
                "form" : form
            })     
    return render(request, "encyclopedia/create.html",{
        "form" : NewFormEntry()
    })