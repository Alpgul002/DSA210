# -------------------------------------------------------------
# GEREKLİ PAKETLER
import requests, pandas as pd
from pathlib import Path
from datetime import date
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
# -------------------------------------------------------------
# AYARLAR
LAT, LON     = 41.087643, 28.765575        # İkitelli / İstanbul ÜRETİM TESİSİ
START_DATE   = date(2018, 5, 1)            # 1 Mayıs 2018
END_DATE     = date(2019, 5, 31)           # 31 Mayıs 2019
OUT_DIR      = Path(".")                   # Çıktı klasörü
# -------------------------------------------------------------
# Türkçe ay isimleri
AY_TR = {1:"January", 2:"February", 3:"March ", 4:"April ", 5:"May ", 6:"June ",
         7:"July ", 8:"August ", 9:"September", 10:"October ", 11:"November ", 12:"December "}

def fetch_month(year:int, month:int) -> pd.DataFrame:
    """Belirtilen ayın (yyyy-mm) günlük verilerini Open-Meteo’dan indirir."""
    start = date(year, month, 1)
    end   = start + relativedelta(months=1) - pd.Timedelta(days=1)

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={LAT}&longitude={LON}"
        f"&start_date={start:%Y-%m-%d}&end_date={end:%Y-%m-%d}"
        "&daily=cloud_cover_mean,temperature_2m_mean"
        "&timezone=Europe%2FIstanbul"
    )
    r = requests.get(url, timeout=30)
    r.raise_for_status()

    df = pd.DataFrame(r.json()["daily"])
    df["time"] = pd.to_datetime(df["time"])
    return df

# ------------------ İSTENEN AYLARI LİSTELE --------------------
months = []
cur = START_DATE.replace(day=1)
while cur <= END_DATE:
    months.append((cur.year, cur.month))
    cur += relativedelta(months=1)

# ------------------- TÜM AYLARI İNDİR ------------------------
frames = []
for y, m in tqdm(months, desc="Veriler indiriliyor"):
    frames.append(fetch_month(y, m))

data = (pd.concat(frames, ignore_index=True)
          .sort_values("time")
          .reset_index(drop=True))

# ------------------- GÜN / AY / YIL EKLE ---------------------
data["Gün"] = data["time"].dt.day
data["Ay"]  = data["time"].dt.month.map(AY_TR)
data["Yıl"] = data["time"].dt.year

final = (data[["Gün", "Ay", "Yıl",
               "cloud_cover_mean", "temperature_2m_mean"]]
         .rename(columns={"cloud_cover_mean":"CloudCover_%",
                          "temperature_2m_mean":"Temp_mean_C"}))

# ---------------------- EXCEL'E YAZ ---------------------------
tag   = f"{START_DATE:%Y-%m}_{END_DATE:%Y-%m}"
excel = OUT_DIR / f"daily_weather_{tag}.xlsx"
final.to_excel(excel, index=False)

print("✓ Dosya hazır →", excel)