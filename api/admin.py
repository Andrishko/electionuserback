from django.contrib import admin
from .models import *
from django.contrib import admin
# Register your models here.


def generate_unique_string():
    # Define the characters to use for generating the string
    characters = string.ascii_letters + string.digits

    while True:
        # Generate a random string of length 50
        random_string = ''.join(random.choices(characters, k=255))

        # Check if the string exists in the `uniq` table
        if not codeVote.objects.filter(code=random_string).exists():
            return random_string

def get_code(modeladmin, request, queryset):
    for u in queryset:
        if u.code == ' ' :
            u.code = generate_unique_string()
            u.save()

class codeVoteAdmin(admin.ModelAdmin):
    list_display = ['name']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.username[0].upper() != 'J':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False
    actions = [get_code]


admin.site.register(codeVote, codeVoteAdmin)
