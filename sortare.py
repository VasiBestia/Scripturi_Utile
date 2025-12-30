from ytmusicapi import YTMusic
import time


def sort_playlist_artist_only():
    print("Se pregătește autentificarea...")

    # 1. Autentificare
    try:
        yt = YTMusic("headers.json")
    except Exception as e:
        print(f"Eroare la autentificare. Verifică fișierul headers.json! Eroare: {e}")
        return

    # --- CONFIGURARE ---
    SOURCE_PLAYLIST_ID = "PL3Vv-eAOQCVE1-dG0tYu8lG991cV3kUVT"
    NEW_PLAYLIST_NAME = "Manele - Sortat Artist"

    print(f"1. Descarc melodiile din sursă...")
    try:
        playlist = yt.get_playlist(SOURCE_PLAYLIST_ID, limit=None)
        tracks = playlist["tracks"]
        print(f"   Am găsit {len(tracks)} melodii în total.")
    except Exception as e:
        print(f"Eroare la citirea playlist-ului: {e}")
        return

    def get_artist(track):

        if track.get("artists") and len(track["artists"]) > 0:
            return track["artists"][0]["name"].strip().lower()
        return "zzz_necunoscut"

    print("2. Procesez și sortez lista...")

    processed_tracks = []
    seen_ids = set()

    for t in tracks:
        vid = t.get("videoId")

        if not vid or vid in seen_ids:
            continue

        seen_ids.add(vid)

        processed_tracks.append(
            {
                "videoId": vid,
                "artist_sort": get_artist(t),
                "title": t.get("title", "Unknown"),
            }
        )

    # --- SORTARE STRICT DUPĂ ARTIST ---
    processed_tracks.sort(key=lambda x: x["artist_sort"])

    print(f"   Au rămas {len(processed_tracks)} melodii unice.")

    # 3. Creare Playlist
    print(f"3. Creez playlistul: '{NEW_PLAYLIST_NAME}'...")
    try:
        new_id = yt.create_playlist(
            NEW_PLAYLIST_NAME, "Playlist generat automat - Sortat A-Z Artist"
        )
        print(f"   Playlist creat cu succes! ID: {new_id}")
    except Exception as e:
        print(f"   [EROARE FATALĂ] Nu am putut crea playlist-ul: {e}")
        print(
            "   Sfat: Verifică dacă headers.json e valid sau dacă ai atins limita zilnică de playlist-uri."
        )
        return

    # 4. Adăugare Melodii
    final_ids = [t["videoId"] for t in processed_tracks]

    print("4. Încep popularea playlist-ului (câte 50 de piese)...")
    for i in range(0, len(final_ids), 50):
        batch = final_ids[i : i + 50]
        try:
            yt.add_playlist_items(new_id, batch)
            print(f"   -> Adăugat lotul {i // 50 + 1} ({len(batch)} piese)...")
            time.sleep(1.5)
        except Exception as e:
            print(f"   [EROARE] Eșec la lotul {i // 50 + 1}: {e}")

    print("\nSucces! Proces finalizat.")


if __name__ == "__main__":
    sort_playlist_artist_only()
