#========================================
# MODELLING
#========================================

# Supervised Learning(Regression)
## Pengumpulan Data
df_mtcars <- mtcars

head(df_mtcars)
str(df_mtcars)
summary(df_mtcars)
#---------------------------------------------------------------------
## Pra-pemrosesan Data
### Memeriksa data kosong
colSums(is.na(df_mtcars))

### Membuat fitur baru
df_mtcars$power_to_weight <- mtcars$hp / mtcars$wt

### Melihat hasil
head(df_mtcars)
#---------------------------------------------------------------------
## Pembagian Data
set.seed(123)

n <- nrow(df_mtcars)
train_index <- sample(
  1:n,
  size = 0.8 * n
)

train_data <- df_mtcars[train_index, ]
test_data <- df_mtcars[-train_index, ]

nrow(train_data)
nrow(test_data)
#---------------------------------------------------------------------
## Pelatihan Model
### Membuat model regresi
model_regresi <- lm(
  mpg ~ wt + hp + power_to_weight,
  data = train_data
)

### Melihat hasil model
summary(model_regresi)

### Melakukan prediksi pada data testing
prediksi <- predict(
  model_regresi,
  newdata = test_data
)

prediksi

### Membuat tabel perbandingan
hasil_prediksi <- data.frame(
  Aktual = test_data$mpg,
  Prediksi = prediksi
)

hasil_prediksi
#--------------------------------------------------------------------
##Evaluasi Model
###MAE
MAE <- mean(
  abs(test_data$mpg - prediksi)
)

MAE
###RMSE
RMSE <- sqrt(
  mean((test_data$mpg - prediksi)^2)
)

RMSE
###R2
SS_res <- sum(
  (test_data$mpg - prediksi)^2
)

SS_tot <- sum(
  (test_data$mpg - mean(test_data$mpg))^2
)

R2 <- 1 - (SS_res / SS_tot)
R2

###Hasil Evaluasi
hasil_evaluasi <- data.frame(
  MAE = MAE,
  RMSE = RMSE,
  R2 = R2
)

hasil_evaluasi
#----------------------------------------------------------------------
##Deployment
### Data baru
data_baru <- data.frame(
  wt = 3.0,
  hp = 150,
  power_to_weight = 150 / 3.0
)

### Prediksi
prediksi_baru <- predict(
  model_regresi,
  newdata = data_baru
)

prediksi_baru
#====================================================================
# Unsupervised Learning(Clustering)
##Pengumpulan Data
df_mtcars <- mtcars

head(df_mtcars)
str(df_mtcars)
summary(df_mtcars)
#-------------------------------------------------------------------
##Pemilihan Fitur
data_cluster <- df_mtcars[, c( "cyl", "disp", "hp", "wt", "qsec", "gear" )] 
head(data_cluster)
#-------------------------------------------------------------------
##Pra-Pemrosesan Data
###Pemeriksaan Missing Value
colSums(is.na(data_cluster))

###Pemeriksaan Data Duplikat
sum(duplicated(data_cluster))

###Pembagian Data
set.seed(123)
n <- nrow(data_cluster)

train_index <- sample(
  1:n, size = 0.8 * n
  )

train_data <- data_cluster[train_index, ] 
test_data <- data_cluster[-train_index, ]
nrow(train_data) 
nrow(test_data)

###Standardisasi Data
train_scaled <- scale(train_data)
head(train_scaled)
#--------------------------------------------------------------------
##Pemilihan Metode Pengukuran Jarak
jarak_euclidean <- dist(train_scaled, method = "euclidean")
head(as.matrix(jarak_euclidean))
#-------------------------------------------------------------------
##Algoritma Clustering
###K-Means Clustering
####Menentukan Jumlah Cluster
set.seed(123)
wss <- numeric(10)

for (k in 1:10){
  model_kmeans <- kmeans(
    train_scaled, 
    centers = k, 
    nstart = 25 ) 
  wss[k] <- model_kmeans$tot.withinss
  }

plot(1:10, 
     wss, 
     type = "b",
     xlab = "Jumlah Cluster (k)", 
     ylab = "Within-Cluster Sum of Squares", 
     main = "Elbow Method")

####Membuat Model K-Means
set.seed(123) 
model_kmeans <- kmeans(train_scaled, 
                       centers = 3, 
                       nstart = 25)

model_kmeans
model_kmeans$cluster
hasil_kmeans <- train_data
hasil_kmeans$cluster <- model_kmeans$cluster
hasil_kmeans
#-------------------------------------------------------------------------------
###Hierarchical Clustering
####Membuat model hierarchical clustering
model_hc <- hclust(jarak_euclidean, 
                   method = "complete")

####Membuat Dendogram
plot(model_hc, 
     main = "Dendrogram Hierarchical Clustering", 
     xlab = "Objek",
     ylab = "Jarak")
####Membentuk 3 Cluster
cluster_hc <- cutree(model_hc, k = 3)
cluster_hc
hasil_hc <- train_data
hasil_hc$cluster <- cluster_hc
hasil_hc
#===============================================================================
##Evaluasi Hasil Clustering
###K-Means
####Within-Cluster Sum of Squares
model_kmeans$tot.withinss
model_kmeans$withinss #wss untuk tiap cluster
####Silhouette Score
library(cluster)
sil_kmeans <- silhouette(model_kmeans$cluster, 
                         jarak_euclidean)
head(sil_kmeans)
mean( sil_kmeans[, "sil_width"])

###Hierarchical Clustering
sil_hc <- silhouette(
  cluster_hc,
  jarak_euclidean)

head(sil_hc)
mean(sil_hc[,"sil_width"] )
#===============================================================================
##Interpretasi dan Tindakan
###K-Means
#### Rata-rata setiap fitur berdasarkan cluster 
karakteristik_kmeans <- aggregate(
  train_data, 
  by = list(Cluster = model_kmeans$cluster), FUN = mean) 
karakteristik_kmeans
####Jumlah Anggota Cluster
table(model_kmeans$cluster)
#-------------------------------------------------------------------------------
###Hierarchical Clustering
#### Rata-rata setiap fitur berdasarkan cluster 
karakteristik_hc <- aggregate(
  train_data,
  by = list(Cluster = cluster_hc), FUN = mean)
karakteristik_hc
####Jumlah Anggota Cluster
table(cluster_hc)
