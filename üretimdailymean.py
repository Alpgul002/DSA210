import pandas as pd, os, pathlib


# --- Ay isimleri ---
ay_tr = {1:"January", 2:"February", 3:"March ", 4:"April ", 5:"May ", 6:"June ",
         7:"July ", 8:"August ", 9:"September", 10:"October ", 11:"November ", 12:"December "}

# Girdiler / çıktılar
src    = r"C:\Users\alpgu\Downloads\ikitelli-gune-enerjisi-santrali-elektrik-uretim-miktarlar (2).xlsx"
dest  = r'C:\Users\alpgu\OneDrive\ikitelli_daily_energy.xlsx'



# Üretim sütunu olası adlar
kolonlar = ["Üretim (kWh)",
            "İkitelli Inverterler Toplam (kWh)",
            "Toplam (kWh)"]

# 1) Tüm sayfaları tek DataFrame’ de birleştir
frames = []
for sh in pd.ExcelFile(src).sheet_names:
    df = pd.read_excel(src, sheet_name=sh)

    # Tarih & üretim kolonlarını bul
    if "Tarih" not in df.columns:          # bazı sayfalarda farklıysa ek kontrol yap
        continue
    prod = next((c for c in kolonlar if c in df.columns), None)
    if prod is None:                       # üretim kolonu yoksa atla
        continue

    df = df[["Tarih", prod]].rename(columns={prod: "kWh"})
    df["Tarih"] = pd.to_datetime(df["Tarih"], errors="coerce")
    df.dropna(subset=["Tarih"], inplace=True)
    frames.append(df)

raw = pd.concat(frames, ignore_index=True)

# 2) İstenen tarih aralığı
mask = (raw["Tarih"] >= "2018-05-01 04:55") & (raw["Tarih"] <= "2019-05-31 22:45")
raw  = raw.loc[mask]

# 3) Günü normalize et → 2024-05-01 13:45 → 2024-05-01 00:00
raw["Date"] = raw["Tarih"].dt.normalize()

# 4) Günlük toplama (tekilleştirme tam burada!)
daily = (raw.groupby("Date", as_index=False)["kWh"]
             .sum()
             .rename(columns={"kWh": "Üretim (kWh)"}))

# 5) Ay / gün / yıl kolonlarını çıkar
daily["Gün"] = daily["Date"].dt.day
daily["Ay"]  = daily["Date"].dt.month.map(ay_tr)
daily["Yıl"] = daily["Date"].dt.year

# 6) İstenen kolon sırası ve kronolojik sıralama
final = daily.sort_values("Date")[["Gün", "Ay", "Yıl", "Üretim (kWh)"]]

# 7) Kaydet
final.to_excel(dest, index=False)
print("✔ Günlük eşsiz liste yazıldı →", dest)