#Persiapan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder

##Library Modelling
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, silhouette_score, mean_absolute_percentage_error
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram

# Load Data
path = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
df_modelling = pd.read_csv(path)

# Pemeriksaan Data dan preprocessing data
df_modelling.describe()
df_modelling.dtypes
df_modelling.isna().sum()
df_modelling["horsepower"].fillna(df_modelling["horsepower"].mean(), inplace= True)
df_modelling.isna().sum()

unique_origin = df_modelling["origin"].unique()
##Encoding Nominal
df_modelling["encoding_origin"] = LabelEncoder().fit_transform(df_modelling["origin"])
##Encoding Ordinal
df_modelling[["ordinal_encoding"]] = OrdinalEncoder(categories=[["usa", "europe", "japan"]]).fit_transform(
    df_modelling[["origin"]]
)
##Pengecekan Encoding
pengecekan_encoding = df_modelling.groupby("origin")[["encoding_origin", "ordinal_encoding"]].first()
##Encoding Dummies
df_encoded = pd.get_dummies(df_modelling, columns=['origin'], drop_first=True)

#Kasus 1: Regresi, memprediksi efisiensi bahan bakar mobil
X = df_modelling[["cylinders", "displacement", "horsepower", "weight", "acceleration"]]
y = df_modelling["mpg"]

x_traine, x_test, y_traine, y_test = train_test_split(X, y, test_size =0.2, train_size = 0.8, random_state = 42)

##Standarisasi
scaler = StandardScaler()
norm_x_traine = scaler.fit_transform(x_traine)
norm_x_test = scaler.transform(x_test)
print(scaler.mean_)
print(scaler.scale_)
print(scaler.var_)

##Membuat Model
###Training Model
regresi = LinearRegression()
model_regresi = regresi.fit(norm_x_traine, y_traine)
coef_regresi = model_regresi.coef_
intercept_regresi = model_regresi.intercept_

###Mencari Y duga
y_predict_traine = model_regresi.predict(norm_x_traine)
y_predict_test = model_regresi.predict(norm_x_test)

###Menguji Model
r2_traine = r2_score(y_traine, y_predict_traine)
r2_test = r2_score(y_test, y_predict_test)
MSE_metric = mean_squared_error(y_test, y_predict_test)
RMSE_test = np.sqrt(MSE_metric)
MAPE_metric = mean_absolute_percentage_error(y_test, y_predict_test)
print("=== Akurasi Model Regresi ===")
print(f"R2 Traine: {r2_traine:.2f}")
print(f"R2 Test: {r2_test:.2f}")
print(f"Nilai MSE: {MSE_metric:.2f}")
print(f"Nilai RMSE: {RMSE_test:.2f}")
print(f"Nilai MAPE: {MAPE_metric:.2f}")

#Kasus 2: K-Means, segmentasi tipe mobil
list_fitur_kmeans = df_modelling[["mpg", "cylinders", "displacement", "horsepower", "weight", "acceleration"]]

traine_data_kmeans, test_data_kmeans = train_test_split(
    list_fitur_kmeans, test_size = 0.15, train_size=0.85,
    random_state=42
)
len(traine_data_kmeans)
len(test_data_kmeans)

##Standardisasi
scaler_kmeans = StandardScaler()
scale_traine_kmeans = scaler_kmeans.fit_transform(traine_data_kmeans)
scale_test_kmeans = scaler_kmeans.transform(test_data_kmeans)
print(scaler_kmeans.mean_)
print(scaler_kmeans.scale_)
print(scaler_kmeans.var_)

##Mencari Nilai K (Jumlah Cluster) terbaik
k_range = range(2, 11)
inertia_list = []
silhouette_list = []

for k in k_range:
    model = KMeans(n_clusters=k, n_init=10, random_state=42)
    model.fit(scale_traine_kmeans)
    inertia_list.append(model.inertia_)
    silhouette_list.append(silhouette_score(scale_traine_kmeans, model.labels_))

###Plot Elbow dan Silhoette
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(k_range, inertia_list, marker="o")
axes[0].set_title("Elbow Method")
axes[0].set_xlabel("Jumlah cluster (k)")
axes[0].set_ylabel("Inertia")

axes[1].plot(k_range, silhouette_list, marker="o", color="orange")
axes[1].set_title("Silhouette Score")
axes[1].set_xlabel("Jumlah cluster (k)")
axes[1].set_ylabel("Silhouette")
plt.tight_layout()
plt.show()

##Membuat Model K-Means
k_optimal = 3
kmeans_model = KMeans(n_clusters=k_optimal, n_init=10, random_state=42)
kmeans_model.fit(scale_traine_kmeans)
label_traine = kmeans_model.labels_
label_test = kmeans_model.predict(scale_test_kmeans)

##Evaluasi Model
sil_traine = silhouette_score(scale_traine_kmeans, label_traine)
sil_test = silhouette_score(scale_test_kmeans, label_test)
print(f"Nilai Silhouette Score Traine: {sil_traine:.2f}")
print(f"Nilai Silhouette Score Test: {sil_test:.2f}")

##Interpretasikan Cluster
hasil_traine_kmeans = traine_data_kmeans.copy()
hasil_traine_kmeans["cluster_kmeans"] = label_traine

inter_cluster_kmeans = hasil_traine_kmeans.groupby("cluster_kmeans").mean().round(2)
inter_cluster_kmeans["jumlah"] = hasil_traine_kmeans["cluster_kmeans"].value_counts().sort_index()
print(inter_cluster_kmeans)

hasil_traine_kmeans["origin"] = df_modelling.loc[hasil_traine_kmeans.index, "origin"]
pivot_inter_cluster_kmeans = pd.crosstab(hasil_traine_kmeans["cluster_kmeans"], hasil_traine_kmeans["origin"])
print(pivot_inter_cluster_kmeans)

#Kasus 3: Hierarchical clustering, segmentasi tipe mobil
list_fitur_HC = df_modelling[["mpg", "cylinders", "displacement", "horsepower", "weight", "acceleration"]]

##Mengambil splitting dari K-Means untuk HC
scale_traine_hc = scale_traine_kmeans.copy()
scale_test_hc = scale_test_kmeans.copy()
len(scale_traine_hc)
len(scale_test_hc)

##Menentukan Linkage dan Dendogram
"""
linkage ialah aturan untuk mengukur jarak antar dua cluster saat hierarchical clustering memutuskan cluster mana yang digabung berikutnya. (ward, single, complete, dan average)
"""
linkage_hc = linkage(scale_traine_hc, method = "ward")

"""
Dendrogram adalah diagram berbentuk pohon terbalik yang menunjukkan urutan penggabungan data dalam hierarchical clustering, beserta jarak saat penggabungan itu terjadi.
"""
dendrogram(linkage_hc, truncate_mode="lastp")
dendrogram(linkage_hc, truncate_mode="lastp", p = 7)
dendrogram(linkage_hc, truncate_mode="level")
dendrogram(linkage_hc, truncate_mode="level", p = 3)

##Membuat Model
k_optimal1 = 2
k_optimal2 = 3

aggromerative_model1 = AgglomerativeClustering(
    n_clusters= k_optimal1, linkage="ward"
    ).fit_predict(scale_traine_hc)

aggromerative_model2 = AgglomerativeClustering(
    n_clusters= k_optimal2, linkage="ward"
    ).fit_predict(scale_traine_hc)

##Evaluasi Model
sil_hc1 = silhouette_score(scale_traine_hc, aggromerative_model1)
sil_hc2 = silhouette_score(scale_traine_hc, aggromerative_model2)
print(f"Silhouette Hierarchical k=2: {sil_hc1:.2f}")
print(f"Silhouette Hierarchical k=3: {sil_hc2:.2f}")
print(f"Silhouette K-Means k=3     : {sil_traine:.2f}")

##Interpretasi Model
hasil_clustering_hc = hasil_traine_kmeans.copy()
hasil_clustering_hc["clustering_hc_model1"] = aggromerative_model1
hasil_clustering_hc["clustering_hc_model2"] = aggromerative_model2

inter_cluster_hc1 = hasil_clustering_hc.drop(columns="clustering_hc_model2").groupby("clustering_hc_model1")[["mpg", "cylinders", "displacement", "horsepower", "weight", "acceleration"]].mean().round(2)
inter_cluster_hc2 = hasil_clustering_hc.drop(columns="clustering_hc_model1").groupby("clustering_hc_model2")[["mpg", "cylinders", "displacement", "horsepower", "weight", "acceleration"]].mean().round(2)

print("=== Pivot Table Hasil Clustering Hierarchy ===")
print(pd.crosstab(hasil_clustering_hc["clustering_hc_model1"], hasil_clustering_hc["origin"]))
print("-"*60)
print(pd.crosstab(hasil_clustering_hc["clustering_hc_model2"], hasil_clustering_hc["origin"]))