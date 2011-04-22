from django.db import models
import datetime
from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag
from markdown import markdown
 
class Category(models.Model):
	title = models.CharField(max_length=250, verbose_name=u'Title',
		help_text=u'Maximum 250 characters.')
	slug = models.SlugField(unique=True, verbose_name=u'Unique Identifier',
		help_text=u"May contain letters, underscores and hyphens. Must be unique.")
	description = models.TextField(verbose_name=u'Category Description')
 
	class Meta:
		ordering = ['title']
		verbose_name = u"Category"
		verbose_name_plural = u"Categories"
 
	def __unicode__(self):
		return self.title
 
	def get_absolute_url(self):
		return "/category/%s/" % self.slug
 
class Entry(models.Model):
	LIVE_STATUS = 1
	DRAFT_STATUS = 2
	HIDDEN_STATUS = 3
	STATUS_CHOICES = ((LIVE_STATUS, u'Live'),
			  (DRAFT_STATUS, u'Draft'),
			  (HIDDEN_STATUS, u'Hidden'))
 
	# article core
	title = models.CharField(max_length=250,  verbose_name=u'Title', help_text=u'Maximum 250 characters.')
	excerpt = models.TextField(blank=True, verbose_name=u'Excerpt', help_text=u'Can be left blank.')
	body = models.TextField(verbose_name=u'Body')
	pub_date = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'Publication date.')
 
	# cached HTML
	excerpt_html = models.TextField(editable=False, blank=True)	# excerpt is Markdown, excerpt_html is HTML
	body_html = models.TextField(editable=False, blank=True)		# body is Markdown, body_html is HTML
 
	# some metadata
	slug = models.SlugField(unique_for_date='pub_date',
			verbose_name=u'Unique Identifier',
			help_text=u"May contain letters, underscores and hyphens. Must be unique.")
	author = models.ForeignKey(User,  verbose_name=u'By')
	enable_comments = models.BooleanField(default=True,  verbose_name=u'Allow Comments.')
	featured = models.BooleanField(default=False,  verbose_name=u'Featured Article')
	status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS,  verbose_name=u'Status')
 
	# categorization
	categories = models.ManyToManyField(Category,  verbose_name=u'Categories')
	tags = TagField(verbose_name=u'Tags', help_text=u'Article tags separated by spaces or commas.')
 
	class Meta:
		verbose_name = u"Article"
		verbose_name_plural = u"Articles"
		ordering = ['-pub_date']
 
	def __unicode__(self):
		return self.title
 
	def save(self):	# override models.Model.save()
		self.body_html = markdown(self.body)
		if self.excerpt:
			self.excerpt_html = markdown(self.excerpt)
		super(Entry, self).save()
 
	def get_absolute_url(self): # view on admin site
		return "/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)
		
	def get_tags(self):
		return TagField.objects.get_for_object(self)