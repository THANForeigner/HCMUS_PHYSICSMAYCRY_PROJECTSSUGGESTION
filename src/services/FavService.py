_favorites = []

def get_favorites():
    return _favorites.copy()

def toggle_favorite(pid):
    global _favorites
    if pid in _favorites:
        _favorites.remove(pid)
    else:
        _favorites.append(pid)
