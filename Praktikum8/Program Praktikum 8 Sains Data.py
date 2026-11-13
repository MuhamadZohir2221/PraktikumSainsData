#PERSIAPAN
import pandas as pd
import numpy as np

path = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
df_ptk8 = pd.read_csv(path)

df_ptk8.isnull().sum()
df_ptk8.describe(include = "all")
df_ptk8.dtypes
#===================================================================
#DISTRIBUSI PROBABILITAS
from scipy.stats import binom, poisson, hypergeom, norm, lognorm, expon

##Diskrit
p_smoker = (df_ptk8["smoker"] == "Yes").mean()
n_binom = 13
k_binom = np.arange(0, n_binom+1)
pmf_binom = binom.pmf(k = k_binom, n = n_binom, p = p_smoker)
print(pmf_binom)

lam = df_ptk8["size"].mean()
k_poiss = np.arange(0, 12)
pmf_poisson = poisson.pmf(k = k_poiss, mu = lam)
print(pmf_poisson)

n_populasi = len(df_ptk8["smoker"])
n_sample = 42
k_hypergeom = np.arange(0, n_sample + 1)
sukses_populasi = ((df_ptk8["smoker"] == "Yes").sum())
pmf_hypergeom = hypergeom.pmf(k = k_hypergeom, M = n_populasi, 
                              n = sukses_populasi, N = n_sample)
print(pmf_hypergeom)

##Kontinu
miu_norm = df_ptk8["total_bill"].mean()
sigma_norm = df_ptk8["total_bill"].std()
x_norm = np.linspace(-21, 21, 212)
pdf_norm = norm.pdf(x_norm, loc = miu_norm, scale = sigma_norm)
print(pdf_norm[112:121])

shape_lognorm, loc_lognorm, scale_lognorm = lognorm.fit(df_ptk8["total_bill"], floc = 0)
x_lognorm = np.linspace(1, 21, 112)
pdf_lognorm = lognorm.pdf(x_lognorm, loc = loc_lognorm, 
                          s = shape_lognorm,
                          scale = scale_lognorm)
print(pdf_lognorm[:21])

loc_e, scale_e = expon.fit(df_ptk8["tip"])
x_expon = np.linspace(1, 21, 112)
pdf_expon = expon.pdf(x_expon, loc_e, scale_e)
print(pdf_expon[:21])

##CDF
cdf_binom = binom.cdf(k = k_binom, n = n_binom, p = p_smoker)
cdf_norm = norm.cdf(x = x_norm, loc = miu_norm, scale = sigma_norm)
print(f"CDF Normal: {cdf_norm[:7]}")
print(f"CDF Binomial: {cdf_binom[:7]}")
#===================================================================
#UJI HIPOTESIS
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
alpha = 0.05

def keputusan(p, alpha=alpha):
    return "Tolak H0" if p < alpha else "Gagal tolak H0"
## Uji T
###Uji 1 Sampel
t1, p1 = stats.ttest_1samp(df_ptk8['tip'], popmean=3)
print("=== One-Sample T-Test (tip vs 3) ===")
print(f"t = {t1:.4f}, p-value = {p1:.4f} -> {keputusan(p1)}")

###Uji Sampel Berpasangan
t2, p2 = stats.ttest_rel(df_ptk8['total_bill'], df_ptk8['tip'])
print("\n=== Paired T-Test (total_bill vs tip) ===")
print(f"t = {t2:.4f}, p-value = {p2:.4f} -> {keputusan(p2)}")

## Uji Normalitas
"""
H0: data berdistribusi normal  |  H1: data tidak normal
"""
for kolom in ['total_bill', 'tip']:
    sh_stat, sh_p = stats.shapiro(df_ptk8[kolom])
    dp_stat, dp_p = stats.normaltest(df_ptk8[kolom])
    print(f"{kolom}:")
    print(f"  Shapiro-Wilk: W = {sh_stat:.4f}, p = {sh_p:.4f} -> {keputusan(sh_p)}")
    print(f"  D'Agostino-Pearson: stat = {dp_stat:.4f}, p = {dp_p:.4f} -> {keputusan(dp_p)}")

## Uji ANOVA
###One Way ANOVA
"""
H0: rata-rata total_bill sama di semua day  |  H1: minimal ada satu day yang berbeda
"""
kelompok = [g['total_bill'] for _, g in df_ptk8.groupby('day')]
f1, p1 = stats.f_oneway(*kelompok)
print("=== One-Way ANOVA (total_bill berdasarkan day) ===")
print(f"F = {f1:.4f}, p-value = {p1:.4f} -> {keputusan(p1)}")

###Two Way ANOVA
"""
Faktor: day dan sex (beserta interaksinya)
"""
model = ols('total_bill ~ C(day) * C(sex)', data=df_ptk8).fit()
hasil = sm.stats.anova_lm(model, typ=2)
print("\n=== Two-Way ANOVA (total_bill ~ day * sex) ===")
print(hasil)

## Uji Chi-Square
"""
H0: dua variabel kategorik independen | H1: ada hubungan (dependen)
"""
pasangan = [('sex', 'smoker'), ('day', 'time')]

for a, b in pasangan:
    tabel = pd.crosstab(df_ptk8[a], df_ptk8[b])
    chi2, p_chi, dof, expected = stats.chi2_contingency(tabel)
    print(f"\n{a} vs {b}")
    print(tabel)
    print(f"chi2 = {chi2:.4f}, dof = {dof}, p-value = {p_chi:.4f} -> {keputusan(p_chi)}")
    print(f"Ada expected < 5? {(expected < 5).any()}")
#===================================================================
#UJI KORELASI
from scipy import stats
alpha = 0.05
def keputusan(p, alpha=alpha):
    return "Tolak H0" if p < alpha else "Gagal tolak H0"
"""
H0: tidak ada korelasi (rho = 0)  |  H1: ada korelasi
"""
r, p_r = stats.pearsonr(df_ptk8['total_bill'], df_ptk8['tip'])
rho, p_rho = stats.spearmanr(df_ptk8['total_bill'], df_ptk8['tip'])
print(f"Pearson : r = {r:.4f}, p = {p_r:.4f} -> {keputusan(p_r)}")
print(f"Spearman: rho = {rho:.4f}, p = {p_rho:.4f} -> {keputusan(p_rho)}")