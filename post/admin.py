from django.contrib import admin

from .models import Post, Author, Category, Comment, Document, DocumentDownload


admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)

# class DocumentDownloadInline(admin.TabularInline):
#     model = DocumentDownload
#     fields = ['id', 'title', 'document', 'file']
#     extra = 0

class DocumentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'description', 'timestamp']

    # inlines = [
    #         DocumentDownloadInline,
    # ]

    class Meta:
        model = Document

admin.site.register(Document, DocumentAdmin)