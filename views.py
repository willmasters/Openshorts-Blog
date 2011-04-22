from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from blog.models import Entry, Category
from tagging.models import Tag, TaggedItem
 
def entries_index(request):
	return render_to_response('entry_index.html', {
	'categories': Category.objects.all(), 'entry_list': Entry.objects.all() [:5] 
	})
	
def site_about(request):
	return render_to_response('about.html', {
	'categories': Category.objects.all()
	})
        
def entries_archive(request):
	return render_to_response('entry_archive.html', { 
	'categories': Category.objects.all(), 'entry_list': Entry.objects.all() })

def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render_to_response('view_category.html', {
    	'categories': Category.objects.all(),
        'object_list': category.entry_set.all(),
        'category': category,
    })
 
def entry_detail(request, year, month, day, slug):
	import datetime, time
	date_stamp = time.strptime(year+month+day, "%Y%b%d")
	pub_date = datetime.date(*date_stamp[:3])
	entry = get_object_or_404(Entry, pub_date__year=pub_date.year,
		pub_date__month=pub_date.month, pub_date__day=pub_date.day,
		slug=slug)
	return render_to_response('entry_detail.html', {
		'categories': Category.objects.all(), 'entry': entry })
	
def tag_detail(request, slug):
	unslug = slug.replace('-', ' ')
	tag = Tag.objects.get(name=unslug)
	qs = TaggedItem.objects.get_by_model(Entry, tag)
	return object_list(request, queryset=qs, extra_context={'tag':slug}, template_name='tags_detail.html')