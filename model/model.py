# 📦 Gerekli kütüphaneler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

# 📁 Veriyi yükle ve sırala
df = pd.read_excel(r"C:\Users\alpgu\OneDrive\Desktop\DSA PROJECFT\train_data.xlsx")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# 📆 Ay bilgisi çıkar
df["Month"] = df["Date"].dt.month

# 🎯 Özellik ve hedef ayrımı
X = df[["CloudCover_%", "Month"]]
y = df["Üretim (kWh)"]

# 🔀 Eğitim-test ayrımı (%80 eğitim, %20 test)
n = len(df)
train_size = int(n * 0.8)
X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]

# ⚖️ Özellikleri standardize et
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 🧠 SVR modeli (en iyi parametrelerle)
svr_model = SVR(kernel="rbf", C=1000, epsilon=100, gamma=0.1)
svr_model.fit(X_train_scaled, y_train)

# 📈 Tahmin yap
y_pred = svr_model.predict(X_test_scaled)

# 📊 Hata metriklerini yazdır
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)  # elle karekök al
mae = mean_absolute_error(y_test, y_pred)

print(f"RMSE: {rmse:.2f} kWh")
print(f"MAE: {mae:.2f} kWh")

# 📉 Grafik: Gerçek vs Tahmin
plt.figure(figsize=(15, 6))
plt.plot(df["Date"].iloc[train_size:], y_test.values, label="Gerçek Üretim", color="orange", linewidth=2)
plt.plot(df["Date"].iloc[train_size:], y_pred, label="SVR Tahmini", color="blue", linestyle="--", linewidth=2)
plt.title("SVR Modeli ile Günlük Güneş Enerjisi Üretimi Tahmini")
plt.xlabel("Tarih")
plt.ylabel("Üretim (kWh)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()