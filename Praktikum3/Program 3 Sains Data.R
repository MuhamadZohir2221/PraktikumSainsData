#Visualisasi
##Line plot
library(ggplot2)
data(package = "ggplot2") #Mengecek dataset yang tersedia di package ggplot2

economic_dataset <- economics
x_economic <- economic_dataset$date[1:17]
y_economic <- economic_dataset$pce[1:17]

###base R
par(mfrow=c(2,4))
type=c("p","l","b","o","h","s","n")
for (i in type){
  plot(x_economic,
       y_economic,
       type= i,
       main=paste("Type=",i))
}

###ggplot2
library(ggplot2)

ggplot(economic_dataset, aes(x = date, y = pce))+
  geom_line()+
  geom_point()

ggplot_line_economic <- data.frame(x_economic, y_economic)
ggplot(ggplot_line_economic, aes(x = x_economic, y_economic))+
  geom_line()+
  geom_point()
#-----------------------------------------------------------------------------------------
##barplot
mpg_dataset <- mpg

###base R
par(mfrow = c(1,1))
barplot(height = table(mpg_dataset$manufacturer),
        main = "Barplot Dataset mpg",
        xlab = "manufacture",
        ylab = "count",
        col = "blue")

###ggplot2
ggplot(mpg_dataset, aes(x = manufacturer, fill = manufacturer))+
  geom_bar(position = "stack",
           width = 0.9,
           color = "black",
           alpha = 1)+
  theme_minimal()
#------------------------------------------------------------------------------------------
##Histogram
library("ggplot2")
txhousing_dataset <- txhousing

###Base R
hist(txhousing_dataset$median,
     main = "Median Housing sales in TX",
     xlab = "Median Score",
     ylab = "Frekuensi",
     col = "blue",
     border = "black",
     breaks = 10)

###ggplot2
ggplot(txhousing_dataset, aes(x = median)) +
  geom_histogram(binwidth = 11000, fill = "skyblue" ,color = "black", na.rm = TRUE) +
  theme_minimal()+
  labs(title = "Median Housing sales in TX",
       x = "Median Score",
       y = "Frekuensi")
#---------------------------------------------------------------------------------------
##Boxplot
library(ggplot2)

mpg_dataset <- mpg
###Base R
par(mfrow = c(1,2))
boxplot(mpg_dataset$displ,
        main = "Boxplot displ Dataset mpg",
        xlab = "displ",
        col = "skyblue",
        medcol = "black")

boxplot(mpg_dataset$hwy,
        main = "Boxplot hwy Dataset mpg",
        xlab = "hwy",
        col = "blue",
        medcol = "purple",
        horizontal = TRUE)

###ggplot2
par(mfrow = c(1,1))
ggplot(mpg_dataset, aes(x = manufacturer,y = displ))+
  geom_boxplot()+
  theme_minimal()+
  labs(
    title = "Boxplot Manufacture of displ in Dataset mpg"
  )
#------------------------------------------------------------------------------------
##Scatterplot
###R Base
jam_belajar <- c(1, 2, 3, 4, 5)
nilai <- c(50, 55, 65, 70, 80)

####Cara 1
plot(jam_belajar, nilai,
     main = "Hubungan Jam Belajar dan Nilai",
     xlab = "Jam Belajar",
     ylab = "Nilai",
     col = "blue",
     pch = 16)

####Cara2 (Dengan Garis regresi)
model <- lm(nilai ~ jam_belajar)
abline(model, col = "red", lwd = 2)

###ggplot2
library(ggplot2)

data <- data.frame(
  jam_belajar = c(1, 2, 3, 4, 5),
  nilai = c(50, 55, 65, 70, 80)
)

####Cara 1:
ggplot(data, aes(x = jam_belajar, y = nilai)) +
  geom_point(color = "blue", size = 3) +
  labs(title = "Hubungan Jam Belajar dan Nilai",
       x = "Jam Belajar",
       y = "Nilai")

####Cara 2 (Dengan garis regresi):
ggplot(data, aes(x = jam_belajar, y = nilai)) +
  geom_point(color = "blue", size = 3) +
  geom_smooth(method = "lm", color = "red", se = FALSE) +
  labs(title = "Hubungan Jam Belajar dan Nilai",
       x = "Jam Belajar",
       y = "Nilai")
#--------------------------------------------------------------------------------------
## Membuat density plot
###Base R
set.seed(123)
data_nilai <- rnorm(100, mean = 70, sd = 10)

####Cara 1:
plot(density(data_nilai),
     main = "Density Plot Nilai Mahasiswa",
     xlab = "Nilai",
     ylab = "Kepadatan",
     col = "blue",
     lwd = 2)

####Cara 2 (Dengan arsiran daerah)
polygon(density(data_nilai),
        col = rgb(0, 0, 1, 0.3),  # biru transparan
        border = "blue")

###ggplot2
library(ggplot2)

# Membuat data
library(ggplot2)

set.seed(123)
data_nilai <- data.frame(
  nilai = rnorm(100, mean = 70, sd = 10)
)

ggplot(data_nilai, aes(x = nilai)) +
  geom_density(fill = "blue", alpha = 0.5) +
  labs(title = "Density Plot Nilai Mahasiswa",
       x = "Nilai",
       y = "Kepadatan")
#--------------------------------------------------------------------------------------
##Pie Chart
###R Base
####Label Biasa
jumlah <- c(10, 20, 30, 40)
kategori <- c("A", "B", "C", "D")

pie(jumlah,
    labels = kategori,
    main = "Distribusi Kategori",
    col = c("red", "blue", "green", "yellow"))

####Label Persentasi
jumlah <- c(10, 20, 30)
persen <- paste0(round(jumlah/sum(jumlah)*100), "%")

pie(jumlah,
    labels = persen,
    main = "Pie Chart dengan Persentase")

###ggplot2
####Label Biasa
library(ggplot2)

data <- data.frame(
  kategori = c("A", "B", "C", "D"),
  jumlah = c(10, 20, 30, 40)
)

ggplot(data, aes(x = "", y = jumlah, fill = kategori)) +
  geom_bar(stat = "identity") +
  coord_polar(theta = "y") +
  labs(title = "Distribusi Kategori")

####Label Persentase
data$persen <- round(data$jumlah / sum(data$jumlah) * 100, 1)

ggplot(data, aes(x = "", y = jumlah, fill = kategori)) +
  geom_bar(stat = "identity") +
  coord_polar(theta = "y") +
  geom_text(aes(label = paste0(persen, "%")),
            position = position_stack(vjust = 0.5)) +
  labs(title = "Pie Chart dengan Persentase")
#================================================================================================
library(ggplot2)

df <- diamonds

head(df)
str(df)
summary(df)

write.csv(df, "C:\\Kuliah\\Praktikum\\asisten\\Sains Data\\Dataset\\diamonds_R.csv", row.names = FALSE)
