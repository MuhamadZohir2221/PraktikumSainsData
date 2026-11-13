# SCRAPPING KOMEN IG
import os
import time
import random
import pandas as pd
from instagrapi import Client
from getpass import getpass

## Konfigurasi
link_ig = "https://www.instagram.com/reel/DcRH8H9T914/"
path_save = r"C:\Kuliah\Praktikum\asisten\Sains Data\PTK 6 Sains Data"
nama_file = "scrapping_ig.csv"
target_komentar_ig = 100
SESSION_FILE = "session.json"

## Membuat fungsi scrapping
def login_ig(sessionid):
    cl = Client()

    if os.path.exists(SESSION_FILE):
        cl.load_settings(SESSION_FILE)

    cl.login_by_sessionid(sessionid)
    cl.dump_settings(SESSION_FILE)
    return cl

def scrapping_ig(cl, LINK_IG, target_komentar, path, namafile):
    penyimpanan = os.path.join(path, namafile)
    all_comments = []
    id_comment = None

    media_pk = cl.media_pk_from_url(LINK_IG)

    while len(all_comments) < target_komentar:
        try:
            comments_chunk, id_comment = cl.media_comments_chunk(
                media_pk, max_amount=20, min_id=id_comment
            )
        except Exception as e:
            print(f"Terjadi Error:\n {e}")
            print("Berhenti sementara, coba lagi nanti progres tersimpan.")
            break

        if not comments_chunk:
            print("Tidak ada komentar baru / Scrapping udah habis")
            break

        all_comments.extend(comments_chunk)
        print(f"Progres: {len(all_comments)}/{target_komentar}")

        data = [{
            "username": c.user.username,
            "komentar": c.text,
            "tanggal": c.created_at_utc
        } for c in all_comments]
        pd.DataFrame(data).to_csv(penyimpanan, index=False, encoding="utf-8-sig")

        if id_comment is None:
            print("Semua komentar sudah terambil (post habis)")
            break

        jeda = random.uniform(15, 45)
        print(f"Jeda {jeda:.1f} detik...")
        time.sleep(jeda)

    print(f"Selesai. Total: {len(all_comments)} komentar tersimpan di {penyimpanan}")

## Eksekusi Fungsi Scrapping
sessionid = getpass("Session ID:")
cl = login_ig(sessionid)

scrapping_ig(cl, LINK_IG = link_ig,
             target_komentar = target_komentar_ig,
             path = path_save, namafile = nama_file)