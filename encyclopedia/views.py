from django.shortcuts import render
from django.http import HttpResponse
from . import util
import html2text
from random import choice
def convert_html_to_markdown(html_content):
    """
    Convert HTML content to Markdown format.

    :param html_content: str, HTML content to be converted
    :return: str, converted Markdown content
    """
    h = html2text.HTML2Text()
    h.ignore_links = False  # Optionally, set to True to ignore converting links
    markdown_content = h.handle(html_content)
    return markdown_content
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def title(request,title):
    content=util.md_to_html(title)
    #print(content)
    if content is not None:
        return render(request,"encyclopedia/title.html",{
            "title":title,
            "content":content
        })
    else:
        return render(request,"encyclopedia/error.html",{
            "message":"Invalid URL Requested Page does not exist!",
        })
def search(request):
    if request.method=="POST":
        query=request.POST.get('q')
    allEntries=util.list_entries()
    result=[]
    if query in allEntries: 
        result.append(query)
        return render(request,"encyclopedia/search.html",{
            "result":result
        })
    for  i in allEntries:
        if query.lower() in i.lower():
            result.append(i)
    if(len(result)):
        return render(request,"encyclopedia/search.html",{
            "result":result
        })
    else:
         return render(request,"encyclopedia/error.html",{
            "message":"Does not match any entry!"
        })
def new(request):
    return render(request,"encyclopedia/new.html")
def save(request):
    if request.method=="POST":
        title=request.POST.get("title")
        content=request.POST.get("content")
    AllEntries=util.list_entries()
    if title in AllEntries:
        return render(request,"encyclopedia/error.html",{
            "message":"Entry already exists!"
        })
    else:
        
        util.save_entry(title,content)
        return render(request, "encyclopedia/title.html", {
        "title":title,
        "content":content
    })
    
def edit(request,title):
    content=util.get_entry(title)
    content=convert_html_to_markdown(content)
    return render(request, "encyclopedia/edit.html", {
        "title":title,
        "content":content
    })

def save_edit(request):
    if request.method=="POST":
        title=request.POST.get("title")
        content=util.md_to_html_txt(request.POST.get("content"))
    util.save_entry(title,content)
    return render(request, "encyclopedia/title.html", {
    "title":title,
    "content":content
    })
def random(request):
    allEntries=util.list_entries()
    title=choice(allEntries)
    content=util.md_to_html(title)
    return render(request,"encyclopedia/title.html",{
            "title":title,
            "content":content
        })



    
     




        
        
