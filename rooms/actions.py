from django.contrib import admin

@admin.action(description="Set all prices to 100")
def adjust_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 100
        room.save()