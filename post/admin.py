from django.contrib import admin

from .models import Post, Author, Category, Comment, Document


admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'description', 'timestamp']

    class Meta:
        model = Document

admin.site.register(Document, DocumentAdmin)