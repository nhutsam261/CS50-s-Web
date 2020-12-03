from .models import Watchlist

def add_context(request):
    watchlist = None
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user).first()
    
    return {
        'watchlist': watchlist
    }