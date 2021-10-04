from django.contrib import admin
from wordpress.models import *
from photologue.admin import GalleryAdmin

from mptt.admin import DraggableMPTTAdmin,MPTTModelAdmin
# class NewsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published')
#     list_display_links = ('id','title')
#     search_fields = ('title','content')
#     list_editable = ('is_published',)
#     list_filter = ('is_published', 'category')
# admin.site.register(News, NewsAdmin)

class TypesAdmin(admin.ModelAdmin):
    list_display = ('id','title','slug')
    list_display_links = ('id','title')
    search_fields = ('title','slug')
    list_filter = ('id', 'title')

    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Types, TypesAdmin)


class EntitiesAdmin(admin.ModelAdmin):
    list_display = ('id','title','slug','type','created_at','updated_at')
    list_display_links = ('id','title')
    search_fields = ('title','slug')
    list_filter = ('id', 'title', 'type')
    # summernote_fields = ('content',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Entities, EntitiesAdmin)


class TermsAdmin(DraggableMPTTAdmin):
    # list_display = ('id','type','title','slug','created_at','updated_at')
    # list_display_links = ('id','title')
    # search_fields = ('title','slug')
    # list_filter = ('id', 'title', 'type')
    # summernote_fields = 'description'
    prepopulated_fields = {"slug": ("title",)}

# admin.site.register(Terms, TermsAdmin)
admin.site.register(Terms, TermsAdmin)


class FieldsAdmin(admin.ModelAdmin):
    list_display = ('id','type', 'title', 'selector', 'entityType')
    list_display_links = ('id','title')
    search_fields = ('title','slug')
    list_filter = ('id', 'title', 'type')
    prepopulated_fields = {"selector": ("title",)}

admin.site.register(Fields, FieldsAdmin)


# class FieldsValueAdmin(admin.ModelAdmin):
#     list_display = ('id','field', 'post', 'term')
#     list_display_links = ('id','field')
#     search_fields = ('post','term', 'field')
#     list_filter = ('id', 'post', 'term', 'field')
#
# admin.site.register(FieldsValues, FieldsValueAdmin)


# Register your models here.
