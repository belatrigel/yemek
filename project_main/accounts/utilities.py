

def get_profil_redirect(user):
    if user.is_ustyonetici:
        myurl = "/admin"
    elif user.role == 1:
        myurl = "accounts:restoranDashboard"
    elif user.role == 2:
        myurl = "accounts:musterinDashboard"
    return myurl 