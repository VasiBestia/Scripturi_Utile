import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS
from pillow_heif import register_heif_opener


register_heif_opener()


def extrage_data_completa(cale_fisier):
    """
    Extrage data completă (YYYY-MM-DD) din metadate.
    Exemplu returnat: "2023-12-25"
    """
    try:
        with Image.open(cale_fisier) as img:
            exif = img.getexif()
            if not exif:
                return None

            for tag_id in [36867, 306]:
                if tag_id in exif:
                    data_raw = exif[tag_id]

                    if " " in data_raw:
                        data_doar_zi = data_raw.split(" ")[0]
                    else:
                        data_doar_zi = data_raw

                    data_finala = data_doar_zi.replace(":", "-")

                    if len(data_finala) >= 10 and data_finala[0].isdigit():
                        return data_finala
    except Exception:
        return None
    return None


def redenumire_data_completa():
    folder_curent = os.getcwd()
    extensii_acceptate = [".heic", ".heif", ".jpg", ".jpeg", ".png"]

    print(f"📂 Scanez folderul curent pentru poze...")

    toate_fisierele = [
        f
        for f in os.listdir(folder_curent)
        if os.path.isfile(os.path.join(folder_curent, f))
    ]

    fisiere_foto = []
    for f in toate_fisierele:
        ext = os.path.splitext(f)[1].lower()
        if ext in extensii_acceptate:
            fisiere_foto.append(f)

    fisiere_foto.sort(key=lambda x: os.path.getmtime(os.path.join(folder_curent, x)))

    if not fisiere_foto:
        print("❌ Nu am găsit poze.")
        return

    print(f"✅ Am găsit {len(fisiere_foto)} poze. Încep redenumirea (YYYY-MM-DD)...\n")

    contor = 1

    for nume_vechi in fisiere_foto:
        cale_veche = os.path.join(folder_curent, nume_vechi)
        _, extensie = os.path.splitext(nume_vechi)
        extensie = extensie.lower()

        data_gasita = extrage_data_completa(cale_veche)

        if data_gasita:
            prefix = data_gasita
        else:
            prefix = "Iphone13ProMax"

        nume_nou = f"{prefix}_{contor:04d}{extensie}"
        cale_noua = os.path.join(folder_curent, nume_nou)

        temp_contor = contor
        while os.path.exists(cale_noua) and nume_nou != nume_vechi:

            pass

        if nume_nou == nume_vechi:
            print(f" . {nume_vechi} (deja ok)")
        else:
            try:

                if os.path.exists(cale_noua):
                    nume_nou = f"{prefix}_{contor:04d}_copy{extensie}"
                    cale_noua = os.path.join(folder_curent, nume_nou)

                os.rename(cale_veche, cale_noua)
                print(f"✅ {nume_vechi} -> {nume_nou}")
            except Exception as e:
                print(f"❌ Eroare: {e}")

        contor += 1

    print("\n🎉 Gata! Toate pozele au fost redenumite.")


if __name__ == "__main__":
    redenumire_data_completa()
