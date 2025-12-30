import os
import sys
from datetime import datetime


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

        if parser and hasattr(parser, "stream"):
            parser.stream._input.close()

        if data_creare:
            an = data_creare.year

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

    extensii_video = [".mov", ".mp4", ".avi", ".mkv", ".3gp", ".m4v"]

    print(f"🎬 Scanez folderul DOAR pentru videoclipuri...")

    toate_fisierele = [
        f
        for f in os.listdir(folder_curent)
        if os.path.isfile(os.path.join(folder_curent, f))
    ]

    lista_video = []
    for f in toate_fisierele:
        if os.path.splitext(f)[1].lower() in extensii_video:
            lista_video.append(f)

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

        data_gasita = extrage_data_video(cale_veche)

        if data_gasita:
            prefix = data_gasita
        else:
            prefix = "Iphone13ProMax"

        nume_nou = f"{prefix}_{contor:04d}{extensie}"
        cale_noua = os.path.join(folder_curent, nume_nou)

        if nume_vechi == nume_nou:
            print(f" . {nume_vechi} (deja ok)")
            contor += 1
            continue

        while os.path.exists(cale_noua):

            if nume_nou == nume_vechi:
                break
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
    sys.stderr = open(os.devnull, "w")
    redenumire_video_only()
