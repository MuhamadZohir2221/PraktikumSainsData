# SCRAPPING REVIEW PLAYSTORE
##Konfigurasi
import pandas as pd
path_game = r"https://play.google.com/store/apps/details?id=com.cygames.umamusume"
id_game = "com.cygames.umamusume"
start_date = pd.Timestamp("2025-06-26", tz="UTC")
end_date = pd.Timestamp("2025-12-12", tz="UTC")
path_ekspor = r"C:\Kuliah\Praktikum\asisten\Sains Data\PTK 6 Sains Data"

##Membuat Fungsi Scrapping
def scrape_review_playstore(id_game, the_startest):
    import pandas as pd
    from google_play_scraper import reviews, Sort
    
    all_reviews = []
    continuation_token = None
    start_date = the_startest
    
    while True:
        result, continuation_token = reviews(
            id_game,
            sort = Sort.NEWEST,
            count = 500,
            continuation_token=continuation_token
        )
    
        if not result:
            break
        all_reviews.extend(result)
        
        # Date Setting
        oldest_date = pd.to_datetime(
            result[-1]["at"],
            utc = True
        )
        
        print(
                f"Total sementara: {len(all_reviews)}, "
                f"review tertua: {oldest_date}"
        )
        
        # Berhenti jika sudah melewati tanggal mulai
        if oldest_date < start_date:
            break
        
        # Tidak ada halaman berikutnya
        if continuation_token is None:
            break
    
    return all_reviews

def df_to_csv(df_name, pathsave, name_file, encoding):
    df_name.to_csv(
        pathsave+name_file,
        index = False,
        encoding = encoding
    )

##Eksekusi fungsi scrapping
df_umamusume = pd.DataFrame(
    scrape_review_playstore(id_game,
                            start_date)
)

df_umamusume["at"] = pd.to_datetime(df_umamusume["at"], utc = True)
df_umamusume_filtered = df_umamusume[
    (df_umamusume["at"] >= start_date) &
    (df_umamusume["at"] < end_date)
]

print("Jumlah review:", len(df_umamusume_filtered))
print(df_umamusume_filtered[["content", "score", "at"]].head())
print(df_umamusume_filtered[["content", "score", "at"]].tail())

df_to_csv(
    df_umamusume_filtered, 
    path_ekspor, 
    r"\umamusume_reviews.csv", 
    "utf-8-sig")