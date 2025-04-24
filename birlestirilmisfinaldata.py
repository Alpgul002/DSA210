import pandas as pd
from pathlib import Path

# -----------------------------------------
# DOSYA YOLLARI – ihtiyaca göre güncelle
energy_xlsx  = Path(r"C:\Users\alpgu\OneDrive\Desktop\DSA PROJECFT\ikitelli_daily_energy.xlsx")       # Üretim (Gün | Ay | Yıl | Üretim)
weather_xlsx = Path(r"C:\Users\alpgu\OneDrive\Desktop\DSA PROJECFT\daily_weather_2018-05_2019-05.xlsx")      # Hava   (Gün | Ay | Yıl | CloudCover_% | Temp_mean_C)
out_xlsx     = Path("train_data.xlsx")         # Birleşik çıktı
# -----------------------------------------

def add_date_col(df: pd.DataFrame) -> pd.DataFrame:
    """Gün-Ay-Yıl’dan güvenli şekilde Date sütunu üretir."""

    # 0) Ay adlarını numaraya map et (gerekiyorsa)
    if df["Ay"].dtype == object:
        month_map = {
                     "January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
                     "July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
        df["Ay"] = df["Ay"].str.strip().map(month_map)

    # Sayıya çevir, hatalıları NaN yap
    df["Ay"]  = pd.to_numeric(df["Ay"],  errors="coerce")
    df["Gün"] = pd.to_numeric(df["Gün"], errors="coerce")
    df["Yıl"] = pd.to_numeric(df["Yıl"], errors="coerce")

    # Eksikleri at
    df = df.dropna(subset=["Gün", "Ay", "Yıl"])

    # Int'e çevir
    df[["Gün","Ay","Yıl"]] = df[["Gün","Ay","Yıl"]].astype(int)

    # ---- Kritik SATIR (yeni) ----
    df["Date"] = pd.to_datetime(dict(year=df["Yıl"],
                                     month=df["Ay"],
                                     day=df["Gün"]))
    # ------------------------------
    return df
# 1) Dosyaları oku
df_energy  = pd.read_excel(energy_xlsx)
df_weather = pd.read_excel(weather_xlsx)

# 2) Tarih sütununu ekle
df_energy  = add_date_col(df_energy)
df_weather = add_date_col(df_weather)

# 3) INNER JOIN → yalnızca ortak günler
merged = (df_energy[["Date", "Üretim (kWh)"]]
          .merge(df_weather[["Date", "CloudCover_%", "Temp_mean_C"]],
                 on="Date", how="inner")
          .sort_values("Date")
          .reset_index(drop=True))

print("Son satır sayısı:", len(merged))

# Date sütununu 'YYYY-MM-DD' stringine çevir
merged["Date"] = merged["Date"].dt.strftime("%Y-%m-%d")

# (Opsiyonel) Date'i ilk sütuna al
cols = ["Date"] + [c for c in merged.columns if c != "Date"]
merged = merged[cols]

# 4) Excel çıktısı
merged.to_excel(out_xlsx, index=False)
print("✓ Birleşik veri kaydedildi →", out_xlsx)