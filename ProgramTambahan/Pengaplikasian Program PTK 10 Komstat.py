import pandas as pd
import numpy as np
from scipy.stats import pearsonr, norm
import seaborn as sns
import matplotlib.pyplot as plt

# ======================================================
# Histogram
# ======================================================
np.random.seed(321)
data_norm = norm.rvs(size = 300, loc = 0, scale = 1)
# Matplotlib
plt.figure(figsize= (7,4))
sns.set_theme(style= "ticks")
plt.hist(x = data_norm)
plt.title("Histogram Graph of Matplotlib")
plt.xlabel("Norm Data")
plt.show()

# Seaborn
plt.figure(figsize = (7,4))
sns.set_theme(style= "ticks")
sns.histplot(data = data_norm)
plt.title("Histogram Graph of Seaborn")
plt.xlabel("Norm Data")
plt.show()

# =======================================================
# Line Plot
# =======================================================
time_series = pd.DataFrame(
    {
    'Bulan': pd.date_range('2023-01-01', periods=12, freq='M'),
    'Penjualan': [120, 135, 128, 145, 160, 155, 170, 180, 175, 190, 210, 230]
}
)

# Matplotlib
plt.figure(figsize = (11,4))
sns.set_theme(style= "darkgrid")
plt.plot(time_series["Bulan"], time_series["Penjualan"])
plt.title("Line plot of Matplotlib")
plt.xlabel("Bulan")
plt.ylabel("Penjualan")
plt.show()

# Seaborn
plt.figure(figsize = (11,4))
sns.set_theme(style= "darkgrid")
sns.lineplot(data = time_series, x = "Bulan", y = "Penjualan")
plt.title("Line plot of Seaborn")
plt.xlabel("Bulan")
plt.ylabel("Penjualan")
plt.show()

# =======================================================
# Scatter Plot
# =======================================================
The_Df = pd.DataFrame(
    {
        "Name": [
            "Deep Impact",
            "Orfevre",
            "Kitasan Black",
            "Contrail",
            "Vodka",
            "Symboli Rudolf",
            "T M Opera O"
        ],
        "Earns": [
            1455000000,
            1576000000,
            1876000000,
            1195000000,
            1335000000,
            1023000000,
            1835000000
        ],
        "The_G1": [7, 6, 9, 5, 6, 4, 8],
        "Race_Starts": [20, 21, 24, 16, 18, 14, 23],
        "Wins": [11, 12, 15, 8, 10, 7, 14],
        "Retire_Age": [5, 5, 6, 4, 5, 4, 6]
    }
)

X_variabel = The_Df.loc[:,["The_G1", "Race_Starts", "Wins", "Retire_Age"]]
X = np.array(The_Df.loc[:,["The_G1", "Race_Starts", "Wins", "Retire_Age"]])
Y = np.array(The_Df.loc[:,"Earns"])
X_columns = X_variabel.columns

#Matplotlib
plt.figure(figsize = (7,4))
sns.set_theme(style="dark")
plt.scatter(x = X[:,0], y = Y)
plt.title("Scatterplot of Matplotlib")
plt.xlabel("The G1")
plt.ylabel("Earns")
plt.show()

# Seaborn
plt.figure(figsize=(7,4))
sns.set_theme(style = "dark")
sns.scatterplot(data = The_Df, x = "Wins", y = "Earns")
plt.title("Scatterplot of Seaborn")
plt.xlabel("Wins")
plt.ylabel("Earns")
plt.show()

# Gabungan Grafik
fig, ax = plt.subplots(2, 2, figsize = (10,6))
sns.set_theme(style = "dark")
ax[0,0].scatter(X[:,0], Y)
ax[0,0].set_title("The G1 Vs Earns Graph")

ax[0,1].scatter(X[:,1], Y)
ax[0,1].set_title("Race Starts Vs Earns Graph")

ax[1,0].scatter(X[:,2], Y)
ax[1,0].set_title("Wins Vs Earns Graph")

ax[1,1].scatter(X[:,3], Y)
ax[1,1].set_title("Retire Age Vs Earns Graph")

plt.tight_layout()
plt.show()

# =======================================================
# Bar plot
# =======================================================
bar_df = The_Df

# Matplotlib
plt.figure(figsize = (11,4))
sns.set_theme(style = "whitegrid")
plt.bar(x = bar_df["Name"], height= bar_df["Race_Starts"])
plt.title("Bar Plot of Matplotlib")
plt.xlabel("Name of Horse")
plt.ylabel("Count of Race Starts")
plt.show()

# Seaborn
plt.figure(figsize = (11,4))
sns.set_theme(style = "whitegrid")
sns.barplot(data = bar_df, x = "Name", y = "Race_Starts")
plt.title("Bar Plot of Seaborn")
plt.xlabel("Name of Horse")
plt.ylabel("Count of Race Starts")
plt.show()

# =======================================================
# Box Plot
# =======================================================

box_df = list(data_norm)
box_df.append(10)

# Matplotlib
plt.figure(figsize=(7,4))
sns.set_theme(style = "white")
plt.boxplot(box_df)
plt.title("Boxplot of Matplotlib")
plt.show()

# Seaborn
plt.figure(figsize=(7,4))
sns.set_theme(style = "white")
sns.boxplot(box_df)
plt.title("Boxplot of Seaborn")
plt.show()

# =======================================================
# Pie Chart
# =======================================================

plt.figure(figsize=(7,4))
sns.set_theme(style = "ticks")
plt.pie(The_Df["The_G1"], 
        labels = The_Df["Name"], 
        autopct= "%1.1f%%",
        shadow = True)
plt.title("Pie Chart Graph")
plt.show()

# Gabungan Chart
fig, ax = plt.subplots(2,2, figsize = (9, 7))
sns.set_theme(style = "ticks")
ax[0,0].pie(The_Df["The_G1"],
            labels = The_Df["Name"],
            autopct = "%1.1f%%",
            shadow = True)
ax[0,0].set_title("The G1 Graph")

ax[0,1].pie(The_Df["Race_Starts"],
            labels = The_Df["Name"],
            autopct = "%1.1f%%",
            shadow = False)
ax[0,1].set_title("Race Starts Graph")

ax[1,0].pie(The_Df["Wins"],
            labels = The_Df["Name"],
            autopct = "%1.1f%%",
            shadow = True)
ax[1,0].set_title("The Wins Graph")

ax[1,1].pie(The_Df["Retire_Age"],
            labels = The_Df["Name"],
            autopct = "%1.1f%%",
            shadow = False)
ax[1,1].set_title("The Retire Age Graph")

plt.tight_layout()
plt.show()