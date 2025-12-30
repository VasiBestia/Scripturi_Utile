import os
import sys
from datetime import datetime

# Importăm unelte pentru metadate video
try:
    from hachoir.parser import createParser
    from hachoir.metadata import extractMetadata
except ImportError:
    print("❌ EROARE: Librăria 'hachoir' lipsește.")
    print("👉 Rulează în terminal: pip install hachoir")
    sys.exit()


def extrage_data_video(cale_fisier):
    parser = None
    try:
        parser = createParser(cale_fisier)
        if not parser:
            return None

        metadata = extractMetadata(parser)
        if not metadata:
            if parser and hasattr(parser, "stream"):
                parser.stream._input.close()
            return None

        data_creare = metadata.get("creation_date")

        # ÎNCHIDEM FIȘIERUL imediat după citire (rezolvă WinError 32)
        if parser and hasattr(parser, "stream"):
            parser.stream._input.close()

        if data_creare:
            an = data_creare.year
            # DACĂ ANUL ESTE 1904, îl ignorăm (e eroare de metadata)
            if an <= 1904:
                return None
            return data_creare.strftime("%Y-%m-%d")

    except Exception:
        if parser and hasattr(parser, "stream"):
            parser.stream._input.close()
        return None
    return None


def redenumire_video_only():
    folder_curent = os.getcwd()

    # Doar extensii video
    extensii_video = [".mov", ".mp4", ".avi", ".mkv", ".3gp", ".m4v"]

    print(f"🎬 Scanez folderul DOAR pentru videoclipuri...")

    # Colectăm fișierele video
    toate_fisierele = [
        f
        for f in os.listdir(folder_curent)
        if os.path.isfile(os.path.join(folder_curent, f))
    ]

    lista_video = []
    for f in toate_fisierele:
        if os.path.splitext(f)[1].lower() in extensii_video:
            lista_video.append(f)

    # Sortare cronologică după modificarea fișierului (ca să fie numerotate în ordine)
    lista_video.sort(key=lambda x: os.path.getmtime(os.path.join(folder_curent, x)))

    if not lista_video:
        print("❌ Nu am găsit videoclipuri.")
        return

    print(f"✅ Am găsit {len(lista_video)} videoclipuri. Încep redenumirea...\n")

    contor = 1
    succes_count = 0

    for nume_vechi in lista_video:
        cale_veche = os.path.join(folder_curent, nume_vechi)
        _, extensie = os.path.splitext(nume_vechi)
        extensie = extensie.lower()

        # 1. Extragem data
        data_gasita = extrage_data_video(cale_veche)

        # 2. Stabilim PREFIXUL
        if data_gasita:
            prefix = data_gasita
        else:
            prefix = "Iphone13ProMax"  # Fallback

        # 3. Generăm numele nou: PREFIX_0001.ext
        nume_nou = f"{prefix}_{contor:04d}{extensie}"
        cale_noua = os.path.join(folder_curent, nume_nou)

        # Evităm redenumirea inutilă
        if nume_vechi == nume_nou:
            print(f" . {nume_vechi} (deja ok)")
            contor += 1
            continue

        # Gestionare duplicate (dacă fișierul țintă există deja)
        while os.path.exists(cale_noua):
            # Dacă există deja un video cu numele ăsta (ex: al 2-lea video din ziua respectivă),
            # scriptul va trece la următorul număr din contorul global.
            # Totuși, dacă rulăm scriptul peste un folder deja parțial redenumit,
            # trebuie să fim atenți.
            if nume_nou == nume_vechi:
                break  # E fișierul curent

            # Verificare simplă: dacă ținta există, creștem contorul și încercăm următorul număr
            # Dar aici ne bazăm pe un contor global unic.
            # Dacă "2023-12-25_0001.mov" există și e alt fișier, scriptul de mai jos va crăpa
            # la os.rename.
            # Soluție rapidă: adăugăm un sufix random sau incrementăm contorul
            print(f"⚠️ {nume_nou} ocupat. Sar peste numărul {contor}.")
            contor += 1
            nume_nou = f"{prefix}_{contor:04d}{extensie}"
            cale_noua = os.path.join(folder_curent, nume_nou)

        try:
            os.rename(cale_veche, cale_noua)
            print(f"✅ {nume_vechi} -> {nume_nou}")
            succes_count += 1
        except Exception as e:
            print(f"❌ Eroare la {nume_vechi}: {e}")

        contor += 1

    print(f"\n🎉 Gata! Am redenumit {succes_count} videoclipuri.")


if __name__ == "__main__":
    # Ascundem mesajele de avertizare enervante din hachoir
    sys.stderr = open(os.devnull, "w")
    redenumire_video_only()
