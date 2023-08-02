from django.contrib import admin
from review.models import Ticket, Review, UserFollows

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'author')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)