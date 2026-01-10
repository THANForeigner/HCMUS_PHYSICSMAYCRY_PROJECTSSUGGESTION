from data.fb import fb_update

class FavService:
    def __init__(self, user):
        self.user = user
        self.favorites = user.get("favoriteProjects", [])
        self.uid = user.get("localId")
        self.id_token = user.get("idToken")

    def get_favorites(self):
        return self.favorites.copy()

    def is_favorite(self, pid):
        return pid in self.favorites

    def toggle_favorite(self, pid):
        if self.is_favorite(pid):
            self.favorites.remove(pid)
        else:
            self.favorites.append(pid)
        self._update_db()

    def _update_db(self):
        if self.uid and self.id_token:
            try:
                fb_update(
                    path=f"users/{self.uid}",
                    data={"favoriteProjects": self.favorites},
                    id_token=self.id_token,
                )
            except Exception as e:
                print(f"Error updating favorites: {e}")