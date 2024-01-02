from django.core.exceptions import ValidationError
import os

def file_extension_validation(value):
    # value demek resmen o girdi alanı demektir. form sayfasındaki input elementi yani
    this_uzanti = os.path.splitext(value.name)[1]
    valid_uzantilar = [".jpg", ".jpeg", ".png", ".bmp"]
    if (this_uzanti.lower() not in valid_uzantilar):
        raise ValidationError("Dosya uzantınız yanlış. bunlardan biri olmalı -->" + str(valid_uzantilar))
    
