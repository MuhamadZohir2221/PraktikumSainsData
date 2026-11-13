# ===============================
# Data Preparation
# ===============================

# Mengimport Data Default R
df_air_quality <- airquality
df_attenu <- attenu

#==========================================================================================================

# 1.Memeriksa Struktur dan Deskripsi Data
cat("=== Struktur Data ===\n")
str(df_air_quality)
str(df_attenu)
cat(strrep("=", 121))

cat("\n=== Deskripsi Data ===\n")
summary(df_air_quality)
summary(df_attenu)
cat(strrep("=", 121))

#====================================================================================================

# 2.Mengatasi Missing Value
##=== Mendeteksi dan Menghitung Nilai Missing ===
summary(df_air_quality)
summary(df_attenu)

cat("Jumlah missing value df_air_quality:", sum(is.na(df_air_quality)), "\n")
cat("Jumlah missing value df_attenu:", sum(is.na(df_attenu)))

##=== Mengatasi Nilai Missing Value ===
###Cara 1: Menghapus Nilai Missing Value
df_cleanNa_airquality1 <- na.omit(df_air_quality)
df_cleanNa_attenu <- na.omit(df_attenu)

cat("Jumlah missing value df_air_quality:", sum(is.na(df_air_quality)),
    "\nJumlah missing value df_cleanNA_airquality:", sum(is.na(df_cleanNa_airquality1)),"\n")
cat("Jumlah missing value df_attenu:", sum(is.na(df_attenu)),
    "\nJumlah missing value df_cleanNa_attenu:", sum(is.na(df_cleanNa_attenu)), "\n")

###Cara 2: Mengganti Nilai Missing Value
rata_rata_Ozone = mean(df_air_quality$Ozone, na.rm = TRUE)
rata_rata_solar = mean(df_air_quality$Ozone, na.rm = TRUE)

df_cleanNA_airquality2 <- df_air_quality
df_cleanNA_airquality2$Ozone[is.na(df_cleanNA_airquality2$Ozone)] <- rata_rata_Ozone
df_cleanNA_airquality2$Solar.R[is.na(df_cleanNA_airquality2$Solar.R)] <- rata_rata_Ozone
cat("Jumlah missing value df_air_quality:", sum(is.na(df_air_quality)),
    "\nJumlah missing value df_cleanNA_airquality:", sum(is.na(df_cleanNA_airquality2)),"\n")

#=======================================================================================================

# 3.Mengatasi Outliers
## Menghitung nilai Q1, Q3, IQR, Batas Bawah, dan Batas Atas
cat("Notes: Gunakan Kolom dist pada dataset df_cleanNa_attenu\n")
Q1 <- quantile(df_cleanNa_attenu$dist, 0.25)
Q3 <- quantile(df_cleanNa_attenu$dist, 0.75)
IQR <- Q3 - Q1
bb <- Q1 - (1.5 * IQR)
ba <- Q3 + (1.5 * IQR)

## Menghitung dan mengecek Jumlah Outlier
sum_outliers <- sum(df_cleanNa_attenu$dist < bb | df_cleanNa_attenu$dist > ba)
boxplot(df_cleanNa_attenu$dist)
cat("Jumlah outliers:", sum_outliers,"\n")

## Mengatasi Outliers
### Cara1: Menghapus outliers
df_cleanoutliers_attenu <- subset(df_cleanNa_attenu,
                                  df_cleanNa_attenu$dist >= bb & df_cleanNa_attenu$dist <= ba)

### Cara2: Mengganti nilai outliers dengan batas rentang terdekat
df_cleanoutliers_attenu2 <- df_cleanNa_attenu
df_cleanoutliers_attenu2$dist[df_cleanoutliers_attenu2$dist < bb] <- bb
df_cleanoutliers_attenu2$dist[df_cleanoutliers_attenu2$dist > ba] <- ba

### Mengecek Outliers Kembali
df_cleanoutliers_attenu
q1_new <- quantile(df_cleanoutliers_attenu$dist, 0.25)
q3_new <- quantile(df_cleanoutliers_attenu$dist, 0.75)
iqr_new <- q3_new - q1_new
bb_new <- q1_new - (1.5 * iqr_new)
ba_new <- q3_new + (1.5 * iqr_new)
cat("Jumlah outliers:", sum_outliers,
    "\nJumlah outliers", sum(df_cleanoutliers_attenu$dist < bb_new | df_cleanoutliers_attenu$dist > ba_new))
boxplot(df_cleanoutliers_attenu$dist)

df_cleanoutliers_attenu2
q1_new2 <- quantile(df_cleanoutliers_attenu2$dist, 0.25)
q3_new2 <- quantile(df_cleanoutliers_attenu2$dist, 0.75)
iqr_new2 <- q3_new2 - q1_new2
bb_new2 <- q1_new2 - (1.5 * iqr_new2)
ba_new2 <- q3_new2 + (1.5 * iqr_new2)
cat("Jumlah outliers:", sum_outliers,
    "\nJumlah outliers", sum(df_cleanoutliers_attenu2$dist < bb_new2 | df_cleanoutliers_attenu2$dist > ba_new2))
boxplot(df_cleanoutliers_attenu2$dist)

#========================================================================================

# 4.Normalisasi dan Standardisasi Data
df_attenu_clear <- df_cleanoutliers_attenu2

# Cara 1: Standarisasi (Z-Score)
df_attenu_clear$dist_standard <- scale(df_attenu_clear$dist)
df_attenu_clear$accel_standard <- scale(df_attenu_clear$accel)

# Cara 2: Normalisasi (Min-Max)
minmax_norm <- function(feature){
  (feature - min(feature)) / (max(feature) - min(feature))
}

df_attenu_clear$dist_norm <- minmax_norm(df_attenu_clear$dist)
df_attenu_clear$accel_norm <- minmax_norm(df_attenu_clear$accel)

# Menampilkasi hasil normalisasi dan standardisasi data
head(df_attenu_clear)

#======================================================================

# 5.Mengatasi Data Duplikat
## Mensimulasikan baris duplikat secara sengaja untuk latihan praktikum
baris_ganda <- df_attenu_clear[1:5, ]
df_attenu_clear <- rbind(df_attenu_clear, baris_ganda)

## Mengecek data duplikat
cat("Total baris duplikat:", sum(duplicated(df_attenu_clear)), "\n")

## Menghapus data duplikat
df_attenu_clear <- unique(df_attenu_clear)
cat("Total baris duplikat:", sum(duplicated(df_attenu_clear)), "\n")

#======================================================================

# 6. Mengonversi Tipe Data(Encoding)
##Melihat struktur tipe data awal setiap kolom
str(df_attenu_clear)
df_attenu_clear_encoding <- df_attenu_clear

#a. Mengubah kolom 'event' dari numerik menjadi Factor (Kategorikal)
df_attenu_clear_encoding$event <- as.factor(df_attenu_clear_encoding$event)

#b. Mengubah kolom 'mag' (numerik desimal) menjadi Integer (bilangan bulat)
df_attenu_clear_encoding$mag_int <- as.integer(df_attenu_clear_encoding$mag)

#c. Mengubah kolom tertentu menjadi Character (Teks) jika diperlukan
df_attenu_clear_encoding$station_char <- as.character(df_attenu_clear_encoding$station)

# Memeriksa kembali struktur data untuk memastikan konversi berhasil
str(df_attenu_clear_encoding)

# Mengecek kelas dari kolom tertentu secara spesifik dan mengecek dataset keseluruhan
head(df_attenu_clear)
head(df_attenu_clear_encoding)

class(df_attenu_clear_encoding$event)
class(df_attenu_clear$event)

#menyimpan dataset
write.csv(df_attenu_clear_encoding, "C:/Kuliah/Praktikum/asisten/Sains Data/PTK 2 Sains Data/Data_Cleaning_Attenu.csv", row.names = FALSE)

