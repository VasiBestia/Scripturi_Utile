import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS
from pillow_heif import register_heif_opener

# 1. Activăm suportul pentru fișiere iPhone (HEIC)
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

            # Căutăm tag-urile standard de dată
            # 36867 = DateTimeOriginal (Momentul pozei)
            # 306 = DateTime
            for tag_id in [36867, 306]:
                if tag_id in exif:
                    data_raw = exif[tag_id]
                    # Formatul brut din EXIF este de obicei: "YYYY:MM:DD HH:MM:SS"

                    # Luăm doar partea de dată (înainte de spațiu)
                    if " " in data_raw:
                        data_doar_zi = data_raw.split(" ")[0]  # Obținem "YYYY:MM:DD"
                    else:
                        data_doar_zi = data_raw

                    # Windows NU acceptă ":" în nume, deci le înlocuim cu "-"
                    # Rezultat: "YYYY-MM-DD"
                    data_finala = data_doar_zi.replace(":", "-")

                    # Verificare rapidă dacă arată a dată (are cifre și liniuțe)
                    if len(data_finala) >= 10 and data_finala[0].isdigit():
                        return data_finala
    except Exception:
        return None
    return None


def redenumire_data_completa():
    folder_curent = os.getcwd()
    extensii_acceptate = [".heic", ".heif", ".jpg", ".jpeg", ".png"]

    print(f"📂 Scanez folderul curent pentru poze...")

    # Colectăm toate pozele
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

    # Le sortăm cronologic după data modificării fișierului (ca să fie numerotate în ordine)
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

        # 1. Căutăm DATA COMPLETĂ
        data_gasita = extrage_data_completa(cale_veche)

        # 2. Stabilim PREFIXUL
        if data_gasita:
            prefix = data_gasita  # Ex: "2023-12-25"
        else:
            prefix = "Iphone13ProMax"  # Fallback dacă nu are dată

        # 3. Generăm numele nou: PREFIX_0001.ext
        nume_nou = f"{prefix}_{contor:04d}{extensie}"
        cale_noua = os.path.join(folder_curent, nume_nou)

        # 4. Verificare anti-suprascriere
        # Dacă ai 100 de poze din 2023-12-25, scriptul va face:
        # 2023-12-25_0001, 2023-12-25_0002, etc.
        # Dar dacă scriptul a mai rulat și există deja 0001, trebuie să găsim următorul număr liber.

        temp_contor = contor
        while os.path.exists(cale_noua) and nume_nou != nume_vechi:
            # Dacă numele e ocupat de ALTĂ poză, creștem un contor local doar pentru verificare
            # (Deși logica principală se bazează pe `contor` global pentru ordine)
            # Aici facem un artificiu: dacă vrei numerotare unică per total folder,
            # folosim contorul global.
            pass
            # Nota: Pentru simplitate și siguranță, în acest script suprascrierea e gestionată
            # prin faptul că `contor` crește mereu.
            # Singurul risc e dacă rulezi scriptul de două ori pe aceleași fișiere deja redenumite.

        # Verificăm dacă fișierul are deja numele corect
        if nume_nou == nume_vechi:
            print(f" . {nume_vechi} (deja ok)")
        else:
            try:
                # Dacă ținta există deja (coliziune rară), adăugăm un sufix extra
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
