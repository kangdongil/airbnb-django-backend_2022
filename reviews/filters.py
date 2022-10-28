from django.contrib.admin import SimpleListFilter

class PopularityFilter(SimpleListFilter):

    title = "popularity"

    parameter_name = "popular"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good(>3)"),
            ("bad", "Bad(<3)"),
            ("neutral", "Neutral(=3)"),
        ]
    
    def queryset(self, request, reviews):
        param = self.value()
        match = {
            "good": reviews.filter(rating__gt=3),
            "bad": reviews.filter(rating__lt=3),
            "neutral": reviews.filter(rating__exact=3),
        }
        return match.get(param, reviews)