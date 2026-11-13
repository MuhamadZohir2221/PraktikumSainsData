#===========================================
# STATISTIKA
#===========================================

# 1. Distribusi Probabilitas
##Normalitas
dnorm(70, mean = 0, sd = 1)
pnorm(70, mean = 0, sd = 1)
qnorm(0.95, mean = 0, sd = 1)
rnorm(10, mean = 0, sd = 1)
##Binomial
dbinom(3, size = 10, prob = 0.5)
pbinom(3, size = 10, prob = 0.5)
qbinom(0.8, size = 10, prob = 0.5)
rbinom(10, size = 10, prob = 0.5)
##Poisson
dpois(2, lambda = 4)
ppois(2, lambda = 4)
qpois(0.8, lambda = 4)
rpois(10, lambda = 4)
#===============================================================================

# 2.Analisis Korelasi
df_iklim = na.omit(airquality) 

## Korelasi Pearson
###Menghitung koefisien korelasi pearson
nilai_pearson <- cor(df_iklim$Wind, df_iklim$Temp, method = "pearson")
cat("Koefisien Pearson:", nilai_pearson, "\n\n")
###Melakukan Uji signifikan Peason
uji_pearson <- cor.test(df_iklim$Wind, df_iklim$Temp, method = "pearson")
print(uji_pearson)
###Fungsi Uji korelasi pearson
ujipearson <- function(x, y){
  xbar = mean(x)
  ybar = mean(y)
  
  pembilang= sum((x-xbar)*(y-ybar))
  penyebut = sqrt(sum((x-xbar)**2) * sum((y-ybar)**2))
  
  r = pembilang / penyebut
  cat("Nilai Korelasi Pearson:", r)
  return(r)
}
ujipearson(df_iklim$Wind, df_iklim$Temp)
#-------------------------------------------------------------------------------

##Korelasi Spearman
### Menghitung koefisien korelasi Spearman (Rank)
nilai_spearman <- cor(df_iklim$Wind, df_iklim$Temp, method = "spearman")
cat("Koefisien Spearman:", nilai_spearman, "\n")
### Melakukan uji signifikansi Spearman (p-value)
uji_spearman <- cor.test(df_iklim$Wind, df_iklim$Temp, method = "spearman")
print(uji_spearman)
###Fungsi Uji korelasi spearman
ujispearman <- function(x, y){
  n = length(x)
  di = rank(x) - rank(y)
  
  di_sum = sum(di**2)
  pembilang = 6 * di_sum
  penyebut = n * (n**2 - 1)
  
  rho = 1 - (pembilang/penyebut)
  cat("Nilai Korelasi Spearman:", rho, "\n")
  return(rho)
}
ujispearman(df_iklim$Wind, df_iklim$Temp)

#===============================================================================

# 3. Uji Hipotesis
## Uji T-test
cat("
H0: Tidak terdapat perbedaan nilai rata-rata yang signifikan antar kelompok yang diuji
H1: Terdapat perbedaan nilai rata-rata yang signifikan antar kelompok yang diuji.
    ")
### Memuat Dataset
df_iklim <- na.omit(airquality)
### Uji Manual
df_ttest <- subset(df_iklim, Month %in% c(5, 8))
uji_t <- t.test(Temp ~ Month, data = df_ttest)
print(uji_t)

### Uji Dengan Function
ujit_function <- function(dataset, x, y, alpha){
  H0_t = "\nTidak terdapat perbedaan nilai rata-rata yang signifikan antar kelompok yang diuji"
  H1_t = "\nTerdapat perbedaan nilai rata-rata yang signifikan antar kelompok yang diuji."
  hasil_uji = t.test(x ~ y, data = dataset)
  p_value = hasil_uji$p.value
  
  
  if(p_value < alpha){
    cat("=== Hasil Keputusan Uji ===")
    cat("\nNilai P-Value:", p_value,
        "\nNilai Alpha:", alpha,
        "\nTolak H0",H1_t)
    return(hasil_uji)
  }else if(p_value >= alpha){
    cat("=== Hasil Keputusan Uji ===")
    cat("\nNilai P-Value:", p_value,
        "\nNilai Alpha:", alpha,
        "\nGagal Tolak H0",H0_t)
    return(hasil_uji)
  }
}

ujit_function(df_ttest, df_ttest$Temp, df_ttest$Month, 0.05)

#-------------------------------------------------------------------------------
## Uji Normalitas (Shapiro-Wilk)
cat("
H0: Populasi atau sampel data berdistribusi normal.
H1: Populasi atau sampel data tidak berdistribusi normal.
    ")

### Memuat Dataset
df_iklim <- na.omit(airquality)

### Uji Manual
uji_normalitas <- shapiro.test(df_iklim$Wind)
print(uji_normalitas)

### Uji Dengan Function
ujinorm_function <- function(x, alpha){
  H0_t = "\nPopulasi atau sampel data berdistribusi normal."
  H1_t = "\nPopulasi atau sampel data tidak berdistribusi normal."
  hasil_uji = shapiro.test(x)
  p_value = hasil_uji$p.value
  
  
  if(p_value < alpha){
    cat("=== Hasil Keputusan Uji ===")
    cat("\nNilai P-Value:", p_value,
        "\nNilai Alpha:", alpha,
        "\nTolak H0",H1_t)
    return(hasil_uji)
  }else if(p_value >= alpha){
    cat("=== Hasil Keputusan Uji ===")
    cat("\nNilai P-Value:", p_value,
        "\nNilai Alpha:", alpha,
        "\nGagal Tolak H0",H0_t)
    return(hasil_uji)
  }
}

ujinorm_function(df_iklim$Temp, 0.05)
#-------------------------------------------------------------------------------
## Uji Korelasi
cat("
H0: Tidak terdapat hubungan atau korelasi yang signifikan antarvariabel.
H1: Terdapat hubungan atau korelasi yang signifikan antarvariabel.
    ")
### Memuat Dataset
df_iklim <- na.omit(airquality)

### Uji Manual
uji_pearson <- cor.test(df_iklim$Ozone, df_iklim$Wind, method = "pearson")
cat("Hasil Uji Korelasi Pearson:\n")
print(uji_pearson)

uji_spearman <- cor.test(df_iklim$Ozone, df_iklim$Wind, method = "spearman")
cat("Hasil Uji Korelasi Spearman:\n")
print(uji_spearman)

### Uji Dengan Function
ujicorr_function <- function(x, y, method, alpha){
  H0_t = "\nTidak terdapat hubungan atau korelasi yang signifikan antarvariabel."
  H1_t = "\nTerdapat hubungan atau korelasi yang signifikan antarvariabel."
  
  method_uji = tolower(method)
  
  if(method_uji == "pearson"){
    hasil_uji = cor.test(x, y, method = method_uji)
    p_value = hasil_uji$p.value
    
    if(p_value < alpha){
      cat("=== Hasil Keputusan Uji ===")
      cat("\nNilai P-Value:", p_value,
          "\nNilai Alpha:", alpha,
          "\nTolak H0",H1_t)
      return(hasil_uji)
    }else if(p_value >= alpha){
      cat("=== Hasil Keputusan Uji ===")
      cat("\nNilai P-Value:", p_value,
          "\nNilai Alpha:", alpha,
          "\nGagal Tolak H0", H0_t)
      return(hasil_uji)
    }
    
  }else if(method_uji == "spearman"){
    hasil_uji = cor.test(x, y, method = method_uji)
    p_value = hasil_uji$p.value
    
    if(p_value < alpha){
      cat("=== Hasil Keputusan Uji ===")
      cat("\nNilai P-Value:", p_value,
          "\nNilai Alpha:", alpha,
          "\nTolak H0",H1_t)
      return(hasil_uji)
    }else if(p_value >= alpha){
      cat("=== Hasil Keputusan Uji ===")
      cat("\nNilai P-Value:", p_value,
          "\nNilai Alpha:", alpha,
          "\nGagal Tolak H0", H0_t)
      return(hasil_uji)
    }
  }else{
    print("Metode Gak Bisa Ditemukan, Pilih Antara Pearson dan Spearman")
  }
}
ujicorr_function(df_iklim$Temp, df_iklim$Month, method = "Pearson", 0.05)
ujicorr_function(df_iklim$Temp, df_iklim$Month, method = "Spearman", 0.05)
#-------------------------------------------------------------------------------
## Uji Chi-Square
cat("
H0: Tidak terdapat hubungan dependensi (variabel saling independen/bebas) antara dua kelompok kategori.
H1: Terdapat hubungan dependensi (saling terkait) antara dua kelompok kategori.
    ")
### Memuat Dataset
df_mobil <- mtcars
### Membuat tabel kontingensi antara Jumlah Silinder (cyl) dan Jenis Transmisi (am)
tabel_kategori <- table(df_mobil$cyl, df_mobil$am)
cat("Tabel Kontingensi (Silinder vs Transmisi):\n")
print(tabel_kategori)
### Melakukan Uji Chi-Square Manual
uji_chisquare <- chisq.test(tabel_kategori)
print(uji_chisquare)
### Melakukan Uji Chi-Square dengan Function
ujichi2 <- function(x, y, alpha){
  tabel_kontingensi = table(x, y)
  
  hasil_uji = chisq.test(tabel_kontingensi)
  p_value = hasil_uji$p.value
  
  if(p_value < alpha){
    cat("=== Hasil Keputusan Uji ===")
    cat("\nNilai P-Value:", p_value,
        "\nNilai Alpha:", alpha,
        "\nTolak H0", "\nTerdapat hubungan dependensi (saling terkait) antara dua kelompok kategori.")
    return(hasil_uji)
  }else if(p_value >= alpha){
    cat("=== Hasil Keputusan Uji ===")
    cat("\nNilai P-Value:", p_value,
        "\nNilai Alpha:", alpha,
        "\nGagal Tolak H0", "\nTidak terdapat hubungan dependensi (variabel saling independen/bebas) antara dua kelompok kategori.")
    return(hasil_uji)
  }
}

ujichi2(df_mobil$cyl, df_mobil$am, 0.05)

