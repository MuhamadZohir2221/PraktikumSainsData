#==============================
#DATA COLLECTING IN R
#==============================

# Mengimport library yang dibutuhkan (Pastikan semua library terinstall sebelum dijalankan)
library(jsonlite)
library(readxl)

# Memasukkan path dataset yang akan diimport
path_csv <- "C:/Kuliah/Praktikum/asisten/Sains Data/Dataset/bank_transactions_data_edited.csv"
path_excel <- "C:/Kuliah/Praktikum/asisten/Sains Data/Dataset/bank_transactions_data_edited.xlsx"
path_json <- "C:/Kuliah/Praktikum/asisten/Sains Data/Dataset/Dataset Json.json"
path_txt <- "C:/Kuliah/Praktikum/asisten/Sains Data/Dataset/Dataset txt.txt"

# Cara 1: Mengimport dataset ke dalam environment dari Path
df_csv <- read.csv(path_csv)
df_excel <- read_excel(path_excel)
df_json <- read_json(path_json)
df_json2 <- fromJSON(path_json)
df_txt <- read.table(path_txt, sep = "")

list_dataset <- list(df_csv, df_excel, df_json, df_json2, df_txt)
name_dataset <- c("Dataset CSV", "Dataset excel", "Dataset JSON", "Dataset JSON2", "Dataset TXT")

print("=== Hasil Import Masing-Masing Format Data ===")
for(i in seq_along(list_dataset)){
  cat("\n",name_dataset[i],":\n")
  print(list_dataset[[i]])
  cat("==========================================================================================")
}

# Cara 2: Mengumpulkan Data dengan Cara Membangkitkan Data
set.seed(123)
df_rep <- c(rep(c(80, 08, 5), times = 7))
df_seq <- c(seq(from = 7, to = 21, by = 2))
df_seq2 <- c(seq(from = 7, to = 21, length.out = 11))
sample1 <- c(sample(1:10, size = 5))
sample2 <- c(sample(c("A", "B", "C"), size = 6, replace = TRUE))
df_unif <- runif(5, min = 0, max = 1)
df_norm <-rnorm(5, mean = 10, sd = 2)
df_binom <-rbinom(5, size = 10, prob = 0.4)
df_pois <- rpois(5, lambda = 3)

list_dataset2 <- list(df_rep, df_seq, df_seq2, sample1, sample2,
                      df_unif, df_norm, df_binom, df_pois)
name_dataset2 <- c("Dataset fungsi rep()", "Dataset fungsi seq()", "Dataset fungsi seq() 2", 
                   "Dataset fungsi sample()1", "Dataset fungsi sample()2", "Dataset fungsi Uniform",
                   "Dataset fungsi Normal", "Dataset fungsi Binomial", "Dataset fungsi Poisson")

print("=== Hasil Import Masing-Masing Format Data ===")
for(i in seq_along(list_dataset2)){
  cat("\n",name_dataset2[i],":\n")
  print(list_dataset2[[i]])
  cat("==========================================================================================")
}

# Cara 3: Mengimport Dataset Deafault R
data()
df_airpassenger <- AirPassengers
df_airpassenger2 <- data.frame(matrix(AirPassengers, ncol = 12, byrow = TRUE))
rownames(df_airpassenger2) <- 1949:1960
colnames(df_airpassenger2) <- month.abb
df_titanic <- Titanic
df_titanic2 <- data.frame(Titanic)

list_dataset3 <- list(df_airpassenger, df_airpassenger2, 
                     df_titanic, df_titanic2)
name_dataset3 <- c("Dataset Air Passenger 1", "Dataset Air Passenger 2", 
                  "Dataset Titanic 1", "Dataset Titanic 2")

print("=== Hasil Import Masing-Masing Format Data ===")
for(i in seq_along(list_dataset3)){
  cat("\n",name_dataset3[i],":\n")
  print(list_dataset3[[i]])
  cat("==========================================================================================")
}

# Validasi Data yang Dikumpulkan
##Menggunakan Dataset CSV dan Titanic
df_csv
df_titanic2

## Mengecek Tipe Data Setiap Variabel
cat("=== Validasi Data ===\n")
cat("Struktur Dataset df_csv:\n")
str(df_csv)
cat("\nStruktur Dataset df_titanic2:\n")
str(df_titanic2)

## Menampilkan Ringkasan Statistik dari Dataset
cat("\n=== Ringkasan Dataset ===\n")
cat("\nRingkasan Dataset df_csv:\n")
summary(df_csv)
cat("\nRingkasan Dataset df_titanic2:\n")
summary(df_titanic2)

