import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.neighbors import LocalOutlierFactor
from statsmodels.tsa.arima.model import ARIMA
import warnings


warnings.filterwarnings("ignore")

# Veri setini yükle
file_path = 'Shipping_Accidents.csv'
df = pd.read_csv(file_path)

# Eksik kritik verileri düşür
critical_cols = ['Acc_Type', 'Sh1_Categ', 'Country', 'IceCondit']
df_clean = df.dropna(subset=critical_cols)

# Kategorik değişkenleri sayısallaştır
le_acc_type = LabelEncoder()
le_ship_cat = LabelEncoder()
le_country = LabelEncoder()
le_ice_cond = LabelEncoder()

df_clean['Acc_Type_Code'] = le_acc_type.fit_transform(df_clean['Acc_Type'])
df_clean['Sh1_Categ_Code'] = le_ship_cat.fit_transform(df_clean['Sh1_Categ'])
df_clean['Country_Code'] = le_country.fit_transform(df_clean['Country'])
df_clean['IceCondit_Code'] = le_ice_cond.fit_transform(df_clean['IceCondit'])

# ------------------ 1️⃣ Logistic Regression ------------------
X = df_clean[['Sh1_Categ_Code', 'Country_Code', 'IceCondit_Code']]
y = df_clean['Acc_Type_Code']
log_reg = LogisticRegression(max_iter=500)
log_reg.fit(X, y)
y_pred = log_reg.predict(X)

plt.figure(figsize=(8, 5))
sns.scatterplot(x=df_clean['Acc_Type_Code'], y=y_pred, hue=df_clean['Cluster'], palette='viridis')
plt.xlabel('Gerçek Kaza Türü (Kod)')
plt.ylabel('Tahmin Edilen Kaza Türü (Kod)')
plt.title('Sınıflandırma: Logistic Regression Çıktısı')
plt.grid(True)
plt.show()

# ------------------ 2️⃣ K-means Kümeleme ------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df_clean['Cluster'] = kmeans.fit_predict(X_scaled)

plt.figure(figsize=(8, 5))
sns.scatterplot(x=df_clean['Sh1_Categ_Code'], y=df_clean['Country_Code'], hue=df_clean['Cluster'], palette='tab10')
plt.xlabel('Gemi Kategorisi (Kod)')
plt.ylabel('Ülke (Kod)')
plt.title('Kümeleme Analizi: K-means Sonuçları')
plt.grid(True)
plt.show()

# ------------------ 3️⃣ Anomali Tespiti ------------------
lof = LocalOutlierFactor(n_neighbors=20)
df_clean['Anomaly'] = lof.fit_predict(X_scaled)

plt.figure(figsize=(8, 5))
sns.scatterplot(x=df_clean['Sh1_Categ_Code'], y=df_clean['Country_Code'], hue=df_clean['Anomaly'], palette='coolwarm')
plt.xlabel('Gemi Kategorisi (Kod)')
plt.ylabel('Ülke (Kod)')
plt.title('Anomali Tespiti: LOF Sonuçları')
plt.grid(True)
plt.show()

# ------------------ 4️⃣ Zaman Serisi Analizi ------------------
yearly_counts = df.groupby('Year')['Unique_ID'].count()

plt.figure(figsize=(10, 5))
plt.plot(yearly_counts.index, yearly_counts.values, marker='o')
plt.title('Yıllık Kaza Sayısı (1989–2025)')
plt.xlabel('Yıl')
plt.ylabel('Kaza Sayısı')
plt.grid(True)
plt.show()

# ------------------ 5️⃣ ARIMA Tahminleme ------------------
model = ARIMA(yearly_counts, order=(1, 1, 1))
model_fit = model.fit()
forecast = model_fit.forecast(steps=5)

plt.figure(figsize=(10, 5))
plt.plot(yearly_counts.index, yearly_counts.values, label='Gerçek')
plt.plot(range(int(yearly_counts.index.max()) + 1, int(yearly_counts.index.max()) + 6), forecast, label='Tahmin', linestyle='--')
plt.title('ARIMA ile Gelecek 5 Yıl İçin Kaza Tahmini')
plt.xlabel('Yıl')
plt.ylabel('Kaza Sayısı')
plt.legend()
plt.grid(True)
plt.show()
