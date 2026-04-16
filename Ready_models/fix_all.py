"""
Patch all 4 cells in hf_analiza_parametryczna.ipynb:
  cell 11 - profiles (add CPK, remove serum_sodium), bootstrap CI, correct title
  cell 13 - probability plots (add R2 + slope explanation)
  cell 22 - bootstrap median (LogNormal -> Weibull)
  cell 25 - KOD 7 bar chart (auto Y-axis, ARTEFAKT annotation)
"""
import json, copy

NB = 'hf_analiza_parametryczna.ipynb'

with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# ── CELL 11 ──────────────────────────────────────────────────────────────────
cells[11]['source'] = ["""# Profile pacjentow (zmienne modelu zredukowanego Weibull AFT)
# Zmienne w modelu finalnym: age, creatinine_phosphokinase,
#   ejection_fraction, serum_creatinine, anaemia, high_blood_pressure
profiles = pd.DataFrame({
    'anaemia':                  [0,   1,   0,   1],
    'high_blood_pressure':      [0,   0,   1,   1],
    'age':                      [55,  65,  75,  55],
    'creatinine_phosphokinase': [250, 500, 1000, 750],
    'ejection_fraction':        [45,  30,  20,  25],
    'serum_creatinine':         [1.0, 1.5, 2.0, 1.2],
})
labels = [
    'Pacjent A \\u2013 niskie ryzyko',
    'Pacjent B \\u2013 srednie ryzyko',
    'Pacjent C \\u2013 wysokie ryzyko',
    'Pacjent D \\u2013 wysokie ryzyko'
]

t_grid = np.linspace(1, df['time'].max(), 300)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

# ── Bootstrap 95% CI ───────────────────────────────────────────────────────
N_BOOT = 200
np.random.seed(42)
boot_sf = {i: [] for i in range(len(profiles))}
for _ in range(N_BOOT):
    sample = model_final.sample(frac=1, replace=True).reset_index(drop=True)
    m = WeibullAFTFitter()
    try:
        m.fit(sample, duration_col='time', event_col='DEATH_EVENT')
        for i, (_, row) in enumerate(profiles.iterrows()):
            sf_b = m.predict_survival_function(row.to_frame().T, times=t_grid)
            boot_sf[i].append(sf_b.values.flatten())
    except Exception:
        pass

# ── Funkcja przezycia z CI ─────────────────────────────────────────────────
plt.figure(figsize=(10, 6))
for i, (_, row) in enumerate(profiles.iterrows()):
    sf = aft_final.predict_survival_function(row.to_frame().T, times=t_grid)
    plt.plot(t_grid, sf.values.flatten(),
             label=labels[i], color=colors[i], linewidth=2)
    if boot_sf[i]:
        arr = np.array(boot_sf[i])
        lo = np.percentile(arr, 2.5, axis=0)
        hi = np.percentile(arr, 97.5, axis=0)
        plt.fill_between(t_grid, lo, hi, alpha=0.15, color=colors[i])
plt.title('Funkcja przezycia \\u2013 model Weibull AFT (z 95% CI bootstrap)')
plt.xlabel('Czas (dni)')
plt.ylabel('Prawdopodobienstwo przezycia S(t)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('hf_aft_survival_profiles.png', dpi=150)
plt.show()

# ── Funkcja hazardu ────────────────────────────────────────────────────────
def compute_hazard(model, profile, t_vals):
    sf_vals = model.predict_survival_function(profile, times=t_vals)
    S = np.clip(sf_vals.values.flatten(), 1e-10, 1.0)
    return -np.gradient(np.log(S), t_vals)

plt.figure(figsize=(10, 6))
for i, (_, row) in enumerate(profiles.iterrows()):
    h = compute_hazard(aft_final, row.to_frame().T, t_grid)
    plt.plot(t_grid, h, label=labels[i], color=colors[i], linewidth=2)
plt.title('Funkcja hazardu \\u2013 model Weibull AFT')
plt.xlabel('Czas (dni)')
plt.ylabel('Hazard h(t)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('hf_aft_hazard_profiles.png', dpi=150)
plt.show()
"""]

# ── CELL 13 ──────────────────────────────────────────────────────────────────
cells[13]['source'] = ["""from lifelines import KaplanMeierFitter
from scipy.stats import norm as scipy_norm
from scipy.stats import pearsonr

# 1. Estymata Kaplana-Meiera surowych danych (marginalnie, bez kowariabli)
kmf = KaplanMeierFitter()
kmf.fit(df['time'], event_observed=df['DEATH_EVENT'])

t_km = kmf.survival_function_.index.values
S_km = kmf.survival_function_['KM_estimate'].values

# Filtrujemy: t > 0, 0 < S < 1
mask = (S_km > 0) & (S_km < 1) & (t_km > 0)
t_km, S_km = t_km[mask], S_km[mask]
log_t = np.log(t_km)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# --- Weibull Probability Plot ---
# Linearyzacja: log(-log(S(t))) = rho*log(t) + const
# Slope = rho (parametr ksztaltu Weibulla; rho < 1 => malejacy hazard)
y_weib = np.log(-np.log(S_km))
slope_w, intercept_w = np.polyfit(log_t, y_weib, 1)
r_sq_w, _ = pearsonr(log_t, y_weib)
y_fit_w = slope_w * log_t + intercept_w
axes[0].scatter(log_t, y_weib, s=20, alpha=0.6, label='KM')
axes[0].plot(log_t, y_fit_w, 'r--', linewidth=2,
             label=f'slope={slope_w:.3f} (=\\u03c1)\\nR\\u00b2={r_sq_w**2:.3f}')
axes[0].set_xlabel('log(t)')
axes[0].set_ylabel('log(-log(S(t)))')
axes[0].set_title('Weibull Probability Plot')
axes[0].legend(fontsize=9)
axes[0].grid(True)

# --- Log-Normal Probability Plot ---
# Linearyzacja: Phi^-1(1-S(t)) = (log(t) - mu) / sigma
# Slope = 1/sigma
y_lnorm = scipy_norm.ppf(1 - S_km)
slope_n, intercept_n = np.polyfit(log_t, y_lnorm, 1)
r_sq_n, _ = pearsonr(log_t, y_lnorm)
y_fit_n = slope_n * log_t + intercept_n
axes[1].scatter(log_t, y_lnorm, s=20, alpha=0.6, label='KM')
axes[1].plot(log_t, y_fit_n, 'r--', linewidth=2,
             label=f'slope={slope_n:.3f} (=1/\\u03c3)\\nR\\u00b2={r_sq_n**2:.3f}')
axes[1].set_xlabel('log(t)')
axes[1].set_ylabel('\\u03a6\\u207b\\u00b9(1 \\u2212 S(t))')
axes[1].set_title('Log-Normal Probability Plot')
axes[1].legend(fontsize=9)
axes[1].grid(True)

# --- Log-Logistic Probability Plot ---
# Linearyzacja: log(S^-1(t) - 1) = -alpha*log(t) + const
# Slope = -alpha (= -1/sigma); |slope| = 1/sigma
y_llogt = np.log(1/S_km - 1)
slope_l, intercept_l = np.polyfit(log_t, y_llogt, 1)
r_sq_l, _ = pearsonr(log_t, y_llogt)
y_fit_l = slope_l * log_t + intercept_l
axes[2].scatter(log_t, y_llogt, s=20, alpha=0.6, label='KM')
axes[2].plot(log_t, y_fit_l, 'r--', linewidth=2,
             label=f'slope={slope_l:.3f} (=-1/\\u03c3)\\nR\\u00b2={r_sq_l**2:.3f}')
axes[2].set_xlabel('log(t)')
axes[2].set_ylabel('log(S(t)\\u207b\\u00b9 \\u2212 1)')
axes[2].set_title('Log-Logistic Probability Plot')
axes[2].legend(fontsize=9)
axes[2].grid(True)

plt.suptitle('Probability Plots \\u2013 ocena dopasowania rozkladow', fontsize=13)
plt.tight_layout()
plt.savefig('hf_probability_plots.png', dpi=150)
plt.show()

print('Dopasowanie rozkladow (R\\u00b2 z linearyzacji KM):')
print(f'  Weibull:       R\\u00b2 = {r_sq_w**2:.4f}  | slope = {slope_w:.4f} (= rho, parametr ksztaltu)')
print(f'  Log-Normal:    R\\u00b2 = {r_sq_n**2:.4f}  | slope = {slope_n:.4f} (= 1/sigma)')
print(f'  Log-Logistic:  R\\u00b2 = {r_sq_l**2:.4f}  | slope = {slope_l:.4f} (= -1/sigma)')
print()
print('Interpretacja slope:')
print('  Weibull:      slope = rho (parametr ksztaltu). rho < 1 => malejacy hazard.')
print('  Log-Normal:   slope = 1/sigma (odwrotnosc skali log-czasu).')
print('  Log-Logistic: slope = -1/sigma (znak ujemny bo os Y jest odwrocona).')
print('  Im blizej R2=1.0, tym lepiej dany rozklad pasuje do danych KM.')
"""]

# ── CELL 22 ──────────────────────────────────────────────────────────────────
cells[22]['source'] = ["""n_iterations = 100
all_medians  = []

np.random.seed(42)
for i in range(n_iterations):
    sample = model_final.sample(frac=1, replace=True).reset_index(drop=True)
    aft_bs = WeibullAFTFitter()   # spojny z modelem finalnym
    aft_bs.fit(sample, duration_col='time', event_col='DEATH_EVENT')
    all_medians.append(aft_bs.predict_median(model_final).median())

ci_low  = np.percentile(all_medians, 2.5)
ci_high = np.percentile(all_medians, 97.5)
mean_m  = np.mean(all_medians)

plt.figure(figsize=(8, 4))
plt.hist(all_medians, bins=20, color='steelblue', edgecolor='white')
plt.axvline(mean_m,  color='red',    linewidth=2, label=f'Srednia: {mean_m:.1f} dni')
plt.axvline(ci_low,  color='orange', linewidth=2, linestyle='--', label=f'2.5%: {ci_low:.1f} dni')
plt.axvline(ci_high, color='orange', linewidth=2, linestyle='--', label=f'97.5%: {ci_high:.1f} dni')
plt.title('Bootstrap: mediana czasu przezycia (Weibull AFT)')
plt.xlabel('Mediana czasu przezycia (dni)')
plt.ylabel('Liczba iteracji')
plt.legend()
plt.tight_layout()
plt.savefig('hf_aft_bootstrap_median.png', dpi=150)
plt.show()

print(f'Bootstrap 95% CI mediany: [{ci_low:.1f}, {ci_high:.1f}] dni')
print(f'Srednia bootstrap:         {mean_m:.1f} dni')
"""]

# ── CELL 25 ──────────────────────────────────────────────────────────────────
cells[25]['source'] = ["""# KOD 7: Dane w formacie dlugim z podzialem na okresy (jak SAS quarter=CEIL(week/13))
# Tutaj uzywamy 30-dniowych okresow dla zbioru Heart Failure

PERIOD_LEN = 30  # dlugosc okresu w dniach (odpowiednik 13 tygodni w SAS)

long_rows = []
for _, row in df.iterrows():
    T     = row['time']
    event = row['DEATH_EVENT']
    n_periods = int(np.ceil(T / PERIOD_LEN))
    n_periods = max(n_periods, 1)
    for j in range(1, n_periods + 1):
        t_end   = min(j * PERIOD_LEN, T)
        t_start = (j - 1) * PERIOD_LEN
        t_dur   = t_end - t_start
        ev_j    = 1 if (j == n_periods and event == 1) else 0
        r = row.to_dict()
        r['period'] = j
        r['t_dur']  = max(t_dur, 0.01)
        r['ev_j']   = ev_j
        long_rows.append(r)

df_long = pd.DataFrame(long_rows)
print(f'Wiersze w formacie dlugim: {len(df_long)}  (oryginalne: {len(df)})')
print(f'Liczba unikalnych okresow: {df_long[\"period\"].nunique()}')

# Zmienne do modelu (te same co model zredukowany)
long_cat  = ['anaemia', 'high_blood_pressure']
long_num  = ['age', 'creatinine_phosphokinase', 'ejection_fraction', 'serum_creatinine']

dummies_long = pd.get_dummies(df_long[long_cat], drop_first=True)
period_dummies = pd.get_dummies(df_long['period'], prefix='period').astype(int)
# Usun pierwsza kolumne (referencje) aby uniknac singularnosci
period_dummies = period_dummies.iloc[:, 1:]

model_long = pd.concat(
    [dummies_long, df_long[long_num], period_dummies,
     df_long[['t_dur', 'ev_j']]], axis=1
)

aft_long = WeibullAFTFitter()
aft_long.fit(model_long, duration_col='t_dur', event_col='ev_j')
print('\\n=== Model piecewise AFT (format dlugi) ===')
aft_long.print_summary()

# --- Wykres efektow okresu ---
period_params = [
    (n, v)
    for n, v in aft_long.params_['lambda_'].items()
    if str(n).startswith('period_')
]

if period_params:
    names, vals = zip(*sorted(period_params, key=lambda x: int(x[0].split('_')[1])))
    vals_arr = np.array(vals)

    # Auto-skalowanie osi Y: ogranicz artefakty numeryczne
    median_v = np.median(vals_arr)
    std_v    = np.std(vals_arr)
    YLIM_MAX = min(median_v + 4 * std_v, 4.0)
    YLIM_MIN = median_v - 3 * std_v

    # Etykiety X = zakres dni
    def period_label(name):
        idx = int(name.split('_')[1])
        return f'{(idx-1)*PERIOD_LEN+1}-{idx*PERIOD_LEN}d'
    x_labels = [period_label(n) for n in names]

    fig, ax = plt.subplots(figsize=(12, 5))
    bar_vals = [min(v, YLIM_MAX * 0.95) if v > YLIM_MAX else v for v in vals_arr]
    bar_colors = ['#e74c3c' if abs(v) > 5 else '#4C72B0' for v in vals_arr]
    ax.bar(x_labels, bar_vals, color=bar_colors)
    ax.set_ylim(YLIM_MIN, YLIM_MAX)
    ax.axhline(0, color='black', linewidth=1)
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8)
    ax.set_title('Efekty okresu (j) \\u2013 model piecewise AFT (odpowiednik CLASS j w SAS)')
    ax.set_ylabel('Wspolczynnik lambda_ (log-skala czasu)')
    ax.set_xlabel('Okres obserwacji')

    # Adnotacja ARTEFAKT dla ostatniego okresu (period_10+)
    for idx_bar, (n, v) in enumerate(zip(names, vals_arr)):
        if abs(v) > 5:
            ax.annotate(
                'ARTEFAKT\\n(brak zdarzen)',
                xy=(idx_bar, min(v, YLIM_MAX * 0.95)),
                xytext=(idx_bar, YLIM_MAX * 0.75),
                fontsize=7, color='red', ha='center',
                arrowprops=dict(arrowstyle='->', color='red', lw=1.2)
            )

    # Ramka informacyjna
    ax.text(0.02, 0.97,
        'Wspolczynniki > 5 to artefakty numeryczne MLE:\\n'
        'w tym okresie nie ma zdarzen (zgonow), wiec\\n'
        'MLE diverguje do +inf. Os Y przycięta automatycznie.',
        transform=ax.transAxes, fontsize=8, va='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='gray', alpha=0.8)
    )

    plt.tight_layout()
    plt.savefig('hf_aft_period_effects.png', dpi=150)
    plt.show()

    print('\\nSurowe wartosci wspolczynnikow periodu:')
    for n, v in zip(names, vals_arr):
        flag = ' <-- ARTEFAKT (brak zdarzen, MLE niestabilne)' if abs(v) > 5 else ''
        print(f'  {n}: {v:.4f}{flag}')
"""]

with open(NB, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Patch applied. Verifying...")

# Quick verification
with open(NB, 'r', encoding='utf-8') as f:
    nb2 = json.load(f)

c11 = ''.join(nb2['cells'][11]['source'])
c13 = ''.join(nb2['cells'][13]['source'])
c22 = ''.join(nb2['cells'][22]['source'])
c25 = ''.join(nb2['cells'][25]['source'])

ok = {
    'cell11_cpk':        'creatinine_phosphokinase' in c11,
    'cell11_N_BOOT':     'N_BOOT' in c11,
    'cell11_fill_btw':   'fill_between' in c11,
    'cell11_weibull':    'model Weibull AFT' in c11,
    'cell13_pearsonr':   'pearsonr' in c13,
    'cell13_R2_print':   'R\\u00b2' in c13,
    'cell13_slope_exp':  'parametr ksztaltu' in c13,
    'cell22_weibull':    'WeibullAFTFitter' in c22,
    'cell22_no_lognorm': 'LogNormal' not in c22,
    'cell25_artefakt':   'ARTEFAKT' in c25,
    'cell25_ylim':       'YLIM_MAX' in c25,
    'cell25_x_labels':   'period_label' in c25,
}

for k, v in ok.items():
    print(f'  {"OK" if v else "FAIL"} {k}')

all_ok = all(ok.values())
print()
print("ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED")
