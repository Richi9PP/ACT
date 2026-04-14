"""Generator trzech notebooków Jupyter dla zbioru Heart Failure."""
import json

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def code(src):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": src,
    }


def md(src):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": src,
    }


def notebook(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.13.0"},
        },
        "cells": cells,
    }


def save(nb, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"  Saved: {path}")


# ===========================================================================
# NOTEBOOK 1 – MODELE PARAMETRYCZNE (Heart Failure)
# ===========================================================================

P = []

P.append(md(
    "# Modele parametryczne – zbiór danych Heart Failure\n\n"
    "Analiza czasu przeżycia (czas do zgonu) metodami parametrycznymi AFT "
    "(Accelerated Failure Time) dla pacjentów z niewydolnością serca.\n\n"
    "- **Zmienna czasu**: `time` (dni od pierwszej wizyty)\n"
    "- **Zdarzenie**: `DEATH_EVENT = 1` (zgon), `0` = cenzurowanie prawostronne\n"
    "- **N = 299** obserwacji; 96 zgonów (32,1 %)"
))

P.append(code(
    "# Instalacja (odkomentuj jeśli potrzeba)\n"
    "#!pip install lifelines pandas matplotlib numpy seaborn openpyxl\n\n"
    "import pandas as pd\n"
    "import numpy as np\n"
    "import matplotlib.pyplot as plt\n"
    "import warnings\n"
    "warnings.filterwarnings('ignore')\n"
    "from lifelines import WeibullAFTFitter, LogNormalAFTFitter, LogLogisticAFTFitter\n\n"
    "df = pd.read_csv('heart_failure_clinical_records_dataset.csv')\n\n"
    "print('Ksztalt danych:', df.shape)\n"
    "print('Kolumny:', df.columns.tolist())\n"
    "print()\n"
    "print('Podstawowe statystyki:')\n"
    "display(df.describe().round(2))\n"
    "print()\n"
    "print(f\"Zdarzenia (zgony): {df['DEATH_EVENT'].sum()} \"\n"
    "      f\"({df['DEATH_EVENT'].mean()*100:.1f}%)\")\n"
    "print(f\"Cenzurowane:       {(df['DEATH_EVENT']==0).sum()} \"\n"
    "      f\"({(df['DEATH_EVENT']==0).mean()*100:.1f}%)\")\n"
))

P.append(md(
    "## KOD 1 – Model Weibulla AFT\n\n"
    "Model Weibulla AFT zakłada, że $\\log(T) = \\mu + \\mathbf{x}^\\top\\boldsymbol{\\beta} + \\sigma\\varepsilon$, "
    "gdzie $\\varepsilon$ pochodzi z rozkładu Gumbela. Parametr $\\rho$ (rho) "
    "opisuje kształt funkcji hazardu:\n"
    "- $\\rho < 1$ – hazard malejący\n"
    "- $\\rho = 1$ – hazard stały (rozkład wykładniczy)\n"
    "- $\\rho > 1$ – hazard rosnący"
))

P.append(code(
    "# Wszystkie zmienne objaśniające\n"
    "variables = [\n"
    "    'age', 'anaemia', 'creatinine_phosphokinase', 'diabetes',\n"
    "    'ejection_fraction', 'high_blood_pressure', 'platelets',\n"
    "    'serum_creatinine', 'serum_sodium', 'sex', 'smoking'\n"
    "]\n\n"
    "aft_weibull = WeibullAFTFitter()\n"
    "aft_weibull.fit(\n"
    "    df[variables + ['time', 'DEATH_EVENT']],\n"
    "    duration_col='time', event_col='DEATH_EVENT'\n"
    ")\n"
    "aft_weibull.print_summary()\n"
))

P.append(md(
    "## KOD 2 – Porównanie modeli AFT: Weibull vs Log-Normalny vs Log-Logistyczny\n\n"
    "Porównujemy trzy rozkłady czasu przeżycia według:\n"
    "- **AIC** (Akaike Information Criterion) – niższe = lepsze dopasowanie\n"
    "- **C** (concordance index) – wyższe = lepsza dyskryminacja\n"
    "- **Log-Likelihood** – miara dopasowania modelu"
))

P.append(code(
    "models = {\n"
    "    'Weibull AFT':      WeibullAFTFitter(),\n"
    "    'Log-Logistic AFT': LogLogisticAFTFitter(),\n"
    "    'Log-Normal AFT':   LogNormalAFTFitter()\n"
    "}\n\n"
    "data = df[variables + ['time', 'DEATH_EVENT']]\n"
    "results = []\n\n"
    "for name, model in models.items():\n"
    "    model.fit(data, duration_col='time', event_col='DEATH_EVENT')\n"
    "    results.append({\n"
    "        'Model': name,\n"
    "        'AIC':           round(model.AIC_, 2),\n"
    "        'Concordance':   round(model.concordance_index_, 4),\n"
    "        'Log-Likelihood': round(model.log_likelihood_, 2)\n"
    "    })\n\n"
    "results_df = pd.DataFrame(results).sort_values('AIC')\n"
    "print('Porownanie modeli AFT (sortowane wg AIC):')\n"
    "display(results_df)\n\n"
    "plt.figure(figsize=(8, 5))\n"
    "colors = ['#4C72B0', '#DD8452', '#55A868']\n"
    "bars = plt.bar(results_df['Model'], results_df['AIC'], color=colors)\n"
    "plt.title('Porownanie modeli AFT – kryterium AIC')\n"
    "plt.ylabel('AIC')\n"
    "plt.xlabel('Model')\n"
    "y_min = min(results_df['AIC']) * 0.995\n"
    "y_max = max(results_df['AIC']) * 1.005\n"
    "plt.ylim(y_min, y_max)\n"
    "for bar, val in zip(bars, results_df['AIC']):\n"
    "    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (y_max-y_min)*0.001,\n"
    "             f'{val:.1f}', ha='center', va='bottom', fontsize=10)\n"
    "plt.grid(axis='y')\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_aft_aic_comparison.png', dpi=150)\n"
    "plt.show()\n"
))

P.append(md(
    "## KOD 3 – Szczegółowa analiza najlepszego modelu\n\n"
    "Na podstawie AIC wybieramy model Log-Normalny AFT. "
    "Następnie:\n"
    "1. Tworzymy zmienne dummy dla zmiennych binarnych\n"
    "2. Eliminujemy nieistotne statystycznie predyktory (p > 0,05)\n"
    "3. Prezentujemy funkcję przeżycia i hazardu dla różnych profili pacjentów"
))

P.append(code(
    "# Budowanie danych modelowych\n"
    "cat_vars = ['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking']\n"
    "num_vars = ['age', 'creatinine_phosphokinase', 'ejection_fraction',\n"
    "            'platelets', 'serum_creatinine', 'serum_sodium']\n\n"
    "dummies = pd.get_dummies(df[cat_vars], drop_first=True)\n"
    "model_data = pd.concat([dummies, df[num_vars + ['time', 'DEATH_EVENT']]], axis=1)\n\n"
    "# Model pełny\n"
    "aft_lognorm = LogNormalAFTFitter()\n"
    "aft_lognorm.fit(model_data, duration_col='time', event_col='DEATH_EVENT')\n"
    "print('=== Model pelny – Log-Normalny AFT ===')\n"
    "aft_lognorm.print_summary()\n"
))

P.append(code(
    "# Model zredukowany – tylko zmienne istotne statystycznie (p < 0.05)\n"
    "# Na podstawie wynikow modelu pelnego\n"
    "final_num = ['age', 'ejection_fraction', 'serum_creatinine', 'serum_sodium']\n"
    "final_cat = ['anaemia', 'high_blood_pressure']\n\n"
    "dummies_final = pd.get_dummies(df[final_cat], drop_first=True)\n"
    "model_final = pd.concat(\n"
    "    [dummies_final, df[final_num + ['time', 'DEATH_EVENT']]], axis=1\n"
    ")\n\n"
    "aft_final = LogNormalAFTFitter()\n"
    "aft_final.fit(model_final, duration_col='time', event_col='DEATH_EVENT')\n"
    "print('=== Model zredukowany – Log-Normalny AFT ===')\n"
    "aft_final.print_summary()\n\n"
    "aft_final.summary.to_excel('hf_aft_final_summary.xlsx')\n"
    "print('Wyniki zapisane do hf_aft_final_summary.xlsx')\n"
))

P.append(code(
    "# Profile pacjentow do wizualizacji\n"
    "profiles = pd.DataFrame({\n"
    "    'anaemia':              [0,    1,    0,    1],\n"
    "    'high_blood_pressure':  [0,    0,    1,    1],\n"
    "    'age':                  [55,   65,   75,   55],\n"
    "    'ejection_fraction':    [45,   30,   20,   25],\n"
    "    'serum_creatinine':     [1.0,  1.5,  2.0,  1.2],\n"
    "    'serum_sodium':         [138,  136,  134,  135]\n"
    "})\n"
    "labels = [\n"
    "    'Pacjent A – niskie ryzyko',\n"
    "    'Pacjent B – srednie ryzyko',\n"
    "    'Pacjent C – wysokie ryzyko',\n"
    "    'Pacjent D – wysokie ryzyko'\n"
    "]\n\n"
    "# Funkcja przezyycia\n"
    "plt.figure(figsize=(10, 6))\n"
    "colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']\n"
    "for i, (_, row) in enumerate(profiles.iterrows()):\n"
    "    sf = aft_final.predict_survival_function(row.to_frame().T)\n"
    "    plt.plot(sf.index, sf.values.flatten(),\n"
    "             label=labels[i], color=colors[i], linewidth=2)\n"
    "plt.title('Funkcja przezycia – model Log-Normalny AFT')\n"
    "plt.xlabel('Czas (dni)')\n"
    "plt.ylabel('Prawdopodobienstwo przezycia S(t)')\n"
    "plt.legend()\n"
    "plt.grid(True)\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_aft_survival_profiles.png', dpi=150)\n"
    "plt.show()\n\n"
    "# Funkcja hazardu\n"
    "t_values = np.linspace(1, df['time'].max(), 500)\n\n"
    "def compute_hazard(model, profile, t_vals):\n"
    "    sf = model.predict_survival_function(profile, times=t_vals)\n"
    "    S = np.clip(sf.values.flatten(), 1e-10, 1.0)\n"
    "    return -np.gradient(np.log(S), t_vals)\n\n"
    "plt.figure(figsize=(10, 6))\n"
    "for i, (_, row) in enumerate(profiles.iterrows()):\n"
    "    h = compute_hazard(aft_final, row.to_frame().T, t_values)\n"
    "    plt.plot(t_values, h, label=labels[i], color=colors[i], linewidth=2)\n"
    "plt.title('Funkcja hazardu – model Log-Normalny AFT')\n"
    "plt.xlabel('Czas (dni)')\n"
    "plt.ylabel('Hazard h(t)')\n"
    "plt.legend()\n"
    "plt.grid(True)\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_aft_hazard_profiles.png', dpi=150)\n"
    "plt.show()\n"
))

P.append(md(
    "## KOD 4 – Cenzurowanie prawostronne\n\n"
    "W zbiorze Heart Failure występuje **cenzurowanie prawostronne**: "
    "obserwacja kończy się, gdy pacjent przeżywa do końca okresu badania (lub wypada z badania) "
    "bez zarejestrowania zgonu. Wiemy jedynie, że przeżył *co najmniej* `time` dni.\n\n"
    "**Cenzurowanie lewostronne** nie zachodzi – punkt startu obserwacji jest dokładnie znany dla każdego pacjenta. "
    "**Cenzurowanie interwałowe** również nie jest potrzebne – czas `time` jest wyrażony w dniach."
))

P.append(code(
    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n\n"
    "for status, label, color in [(0, 'Cenzurowane', '#4C72B0'),\n"
    "                              (1, 'Zdarzenie (zgon)', '#DD8452')]:\n"
    "    mask = df['DEATH_EVENT'] == status\n"
    "    axes[0].hist(df['time'][mask], bins=30, alpha=0.6,\n"
    "                 label=label, color=color)\n"
    "axes[0].set_title('Rozklad czasu obserwacji wg statusu')\n"
    "axes[0].set_xlabel('Czas (dni)')\n"
    "axes[0].set_ylabel('Liczba pacjentow')\n"
    "axes[0].legend()\n"
    "axes[0].grid(True)\n\n"
    "counts = df['DEATH_EVENT'].value_counts()\n"
    "axes[1].pie(counts, labels=['Cenzurowane (0)', 'Zgon (1)'],\n"
    "            autopct='%1.1f%%', colors=['#4C72B0', '#DD8452'],\n"
    "            startangle=90)\n"
    "axes[1].set_title('Proporcja zdarzen i cenzorowan')\n\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_censoring.png', dpi=150)\n"
    "plt.show()\n\n"
    "print(f'Laczna liczba obserwacji: {len(df)}')\n"
    "print(f\"Cenzurowane (DEATH_EVENT=0): {(df['DEATH_EVENT']==0).sum()} \"\n"
    "      f\"({(df['DEATH_EVENT']==0).mean()*100:.1f}%)\")\n"
    "print(f\"Zdarzenia (DEATH_EVENT=1):   {df['DEATH_EVENT'].sum()} \"\n"
    "      f\"({df['DEATH_EVENT'].mean()*100:.1f}%)\")\n"
))

P.append(md("## KOD 5 – Cenzurowanie interwałowe\n\n"
    "W zbiorze Heart Failure **cenzurowanie interwałowe nie jest wymagane**. "
    "Czas do zgonu jest rejestrowany z dokładnością do jednego dnia, "
    "dlatego nie ma potrzeby modelowania przedziału, w którym zdarzenie mogło nastąpić. "
    "Zmienna `time` reprezentuje precyzyjny czas obserwacji."))

P.append(md("## KOD 6 – Mediana przeżycia z bootstrapem\n\n"
    "Estymujemy medianę czasu przeżycia każdego pacjenta wraz z odchyleniem standardowym "
    "przy użyciu metody bootstrap (100 iteracji)."))

P.append(code(
    "n_iterations = 100\n"
    "all_medians = []\n\n"
    "np.random.seed(42)\n"
    "for i in range(n_iterations):\n"
    "    sample = model_final.sample(frac=1, replace=True).reset_index(drop=True)\n"
    "    aft_bs = LogNormalAFTFitter()\n"
    "    aft_bs.fit(sample, duration_col='time', event_col='DEATH_EVENT')\n"
    "    all_medians.append(aft_bs.predict_median(model_final))\n\n"
    "bootstrap_df = pd.concat(all_medians, axis=1)\n"
    "mediany = aft_final.predict_median(model_final)\n"
    "stds = bootstrap_df.std(axis=1)\n\n"
    "wyniki = pd.DataFrame({\n"
    "    'Mediana przezycia (dni)': mediany.round(1),\n"
    "    'Odch. std. (bootstrap)':  stds.round(1)\n"
    "})\n\n"
    "print('Mediana przezycia z bootstrapem (pierwsze 20 pacjentow):')\n"
    "display(wyniki.head(20))\n"
    "print(f'Srednia mediana przezycia: {mediany.mean():.1f} dni')\n"
    "print(f'Sred. odch. std. (bootstrap): {stds.mean():.1f} dni')\n\n"
    "plt.figure(figsize=(10, 5))\n"
    "plt.hist(mediany, bins=40, color='#4C72B0', edgecolor='white', alpha=0.8)\n"
    "plt.axvline(mediany.mean(), color='red', linestyle='--', linewidth=2,\n"
    "            label=f'Srednia mediana = {mediany.mean():.0f} dni')\n"
    "plt.title('Rozklad estymowanej mediany przezycia – model Log-Normalny AFT')\n"
    "plt.xlabel('Mediana przezycia (dni)')\n"
    "plt.ylabel('Liczba pacjentow')\n"
    "plt.legend()\n"
    "plt.grid(True)\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_aft_median_distribution.png', dpi=150)\n"
    "plt.show()\n"
))

P.append(code(
    "# Macierz kowariancji (COVB)\n"
    "cov_df = pd.DataFrame(aft_final.variance_matrix_)\n"
    "cov_df.to_excel('hf_aft_covariance_matrix.xlsx')\n"
    "print('Macierz kowariancji (COVB):')\n"
    "display(cov_df)\n"
    "print('Macierz kowariancji zapisana do hf_aft_covariance_matrix.xlsx')\n"
))

save(notebook(P), "C:/Users/patry/Desktop/Programs/ACT/hf_analiza_parametryczna.ipynb")

# ===========================================================================
# NOTEBOOK 2 – MODEL SEMIPARAMETRYCZNY (Heart Failure)
# ===========================================================================

S = []

S.append(md(
    "# Model semiparametryczny – zbiór danych Heart Failure\n\n"
    "Model Coxa proporcjonalnych hazardów (CoxPH) oraz model Coxa ze zmiennymi "
    "zależnymi od czasu dla pacjentów z niewydolnością serca.\n\n"
    "- **Zmienna czasu**: `time` (dni)\n"
    "- **Zdarzenie**: `DEATH_EVENT = 1` (zgon)\n"
    "- **N = 299** obserwacji; 96 zgonów (32,1 %)"
))

S.append(code(
    "#!pip install lifelines pandas matplotlib numpy\n\n"
    "import pandas as pd\n"
    "import numpy as np\n"
    "import matplotlib.pyplot as plt\n"
    "import warnings\n"
    "warnings.filterwarnings('ignore')\n"
    "from lifelines import CoxPHFitter, CoxTimeVaryingFitter\n"
    "from lifelines.utils import to_episodic_format\n\n"
    "df = pd.read_csv('heart_failure_clinical_records_dataset.csv')\n\n"
    "print('Ksztalt danych:', df.shape)\n"
    "print()\n"
    "selected_cols = ['time', 'DEATH_EVENT', 'age', 'anaemia', 'creatinine_phosphokinase',\n"
    "                 'diabetes', 'ejection_fraction', 'high_blood_pressure',\n"
    "                 'platelets', 'serum_creatinine', 'serum_sodium', 'sex', 'smoking']\n"
    "missing = df[selected_cols].isnull().sum()\n"
    "print('Braki danych:')\n"
    "display(missing[missing > 0] if missing.any() else pd.Series({'Brak brakow danych': 0}))\n"
    "print()\n"
    "display(df[selected_cols].describe().round(3))\n"
))

S.append(md(
    "## KOD 1 – Model Coxa proporcjonalnych hazardów (pełny)\n\n"
    "Model Coxa ma postać:\n"
    "$$h(t|\\mathbf{x}) = h_0(t) \\cdot \\exp(\\boldsymbol{\\beta}^\\top \\mathbf{x})$$\n\n"
    "gdzie $h_0(t)$ to niespecyfikowany hazard bazowy. "
    "Parametry $\\exp(\\beta_j)$ interpretujemy jako **współczynniki ryzyka** (hazard ratio, HR): "
    "HR > 1 oznacza zwiększone ryzyko zgonu, HR < 1 – zmniejszone."
))

S.append(code(
    "variables = [\n"
    "    'age', 'anaemia', 'creatinine_phosphokinase', 'diabetes',\n"
    "    'ejection_fraction', 'high_blood_pressure', 'platelets',\n"
    "    'serum_creatinine', 'serum_sodium', 'sex', 'smoking'\n"
    "]\n\n"
    "cph = CoxPHFitter()\n"
    "cph.fit(\n"
    "    df[variables + ['time', 'DEATH_EVENT']],\n"
    "    duration_col='time', event_col='DEATH_EVENT'\n"
    ")\n"
    "cph.print_summary(model='pelen model Cox', decimals=3)\n"
))

S.append(code(
    "# Forest plot wspolczynnikow\n"
    "fig, ax = plt.subplots(figsize=(8, 6))\n"
    "cph.plot(ax=ax)\n"
    "ax.set_title('Wspolczynniki modelu Coxa (95% CI)')\n"
    "ax.axvline(0, color='red', linestyle='--', linewidth=1)\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_cox_coefficients.png', dpi=150)\n"
    "plt.show()\n"
))

S.append(md(
    "## KOD 2 – Weryfikacja założenia proporcjonalnych hazardów\n\n"
    "Kluczowe założenie modelu Coxa to **proporcjonalność hazardów**: "
    "efekt każdego predyktora nie zmienia się w czasie. "
    "Test Schoenfelda: $H_0$: hazardy są proporcjonalne (p > 0,05 = brak dowodów na naruszenie)."
))

S.append(code(
    "# Test proporcjonalnosci hazardow\n"
    "print('Weryfikacja zalozenia proporcjonalnych hazardow:')\n"
    "cph.check_assumptions(\n"
    "    df[variables + ['time', 'DEATH_EVENT']],\n"
    "    p_value_threshold=0.05,\n"
    "    show_plots=True\n"
    ")\n"
))

S.append(md(
    "## KOD 3 – Model Coxa zredukowany (zmienne istotne statystycznie)\n\n"
    "Usuwamy zmienne nieistotne (p > 0,05) i sprawdzamy założenie na modelu zredukowanym. "
    "W literaturze klinicznej kluczowymi predyktorami w Heart Failure są: "
    "`ejection_fraction`, `serum_creatinine`, `age`, `serum_sodium`."
))

S.append(code(
    "sig_vars = ['age', 'ejection_fraction', 'serum_creatinine', 'serum_sodium',\n"
    "            'anaemia', 'high_blood_pressure']\n\n"
    "cph_red = CoxPHFitter()\n"
    "cph_red.fit(\n"
    "    df[sig_vars + ['time', 'DEATH_EVENT']],\n"
    "    duration_col='time', event_col='DEATH_EVENT'\n"
    ")\n"
    "cph_red.print_summary(model='model zredukowany', decimals=3)\n"
))

S.append(code(
    "# Sprawdzenie zalozen na modelu zredukowanym\n"
    "print('Weryfikacja zalozenia proporcjonalnych hazardow (model zredukowany):')\n"
    "_ = cph_red.check_assumptions(\n"
    "    df[sig_vars + ['time', 'DEATH_EVENT']],\n"
    "    p_value_threshold=0.05,\n"
    "    show_plots=True\n"
    ")\n"
))

S.append(md(
    "## KOD 4 – Stratyfikacja zmiennej naruszającej proporcjonalność\n\n"
    "Jeśli zmienna narusza założenie proporcjonalności hazardów, "
    "stosujemy stratyfikację: osobny hazard bazowy $h_{0k}(t)$ dla każdej warstwy $k$, "
    "ale wspólne parametry $\\boldsymbol{\\beta}$."
))

S.append(code(
    "# Binaryzacja serum_creatinine na kwartyle (jesli naruszenie zalozenia)\n"
    "df_strata = df[sig_vars + ['time', 'DEATH_EVENT']].copy()\n"
    "df_strata['sc_strata'] = pd.qcut(df_strata['serum_creatinine'], q=3,\n"
    "                                  labels=['niski', 'sredni', 'wysoki'])\n\n"
    "cph_strat = CoxPHFitter()\n"
    "cph_strat.fit(\n"
    "    df_strata,\n"
    "    duration_col='time', event_col='DEATH_EVENT',\n"
    "    strata=['sc_strata']\n"
    ")\n"
    "cph_strat.print_summary(model='stratyfikowany serum_creatinine', decimals=3)\n\n"
    "print()\n"
    "_ = cph_strat.check_assumptions(df_strata, p_value_threshold=0.05)\n"
))

S.append(code(
    "# Porownanie AIC modeli Cox\n"
    "comparison = pd.DataFrame({\n"
    "    'Model': ['Pelny Cox', 'Zredukowany Cox', 'Stratyfikowany Cox'],\n"
    "    'Partial AIC': [\n"
    "        round(cph.AIC_, 2),\n"
    "        round(cph_red.AIC_, 2),\n"
    "        round(cph_strat.AIC_, 2)\n"
    "    ],\n"
    "    'Concordance': [\n"
    "        round(cph.concordance_index_, 4),\n"
    "        round(cph_red.concordance_index_, 4),\n"
    "        round(cph_strat.concordance_index_, 4)\n"
    "    ]\n"
    "})\n"
    "print('Porownanie modeli Coxa:')\n"
    "display(comparison)\n"
))

S.append(md(
    "## KOD 5 – Model Coxa ze zmiennymi zależnymi od czasu\n\n"
    "Jeśli zmienna narusza proporcjonalność, możemy wprowadzić **interakcję z czasem** "
    "(`zmienna × czas`), co modeluje zmianę efektu w czasie. "
    "Dane są przekształcane do formatu episodycznego (start/stop)."
))

S.append(code(
    "# Przeksztalcenie do formatu episodycznego\n"
    "df_time = df[sig_vars + ['time', 'DEATH_EVENT']].copy().reset_index()\n"
    "df_time = df_time.rename(columns={'index': 'id'})\n\n"
    "df_long = to_episodic_format(\n"
    "    df_time,\n"
    "    duration_col='time',\n"
    "    event_col='DEATH_EVENT',\n"
    "    time_gaps=30.0  # okna 30-dniowe\n"
    ")\n\n"
    "print(f'Liczba epizodow: {len(df_long)}')\n"
    "display(df_long.head(20))\n"
))

S.append(code(
    "# Dodanie interakcji czas x serum_creatinine\n"
    "df_long['time_x_sc'] = df_long['serum_creatinine'] * df_long['stop']\n\n"
    "ctv = CoxTimeVaryingFitter()\n"
    "ctv.fit(\n"
    "    df_long,\n"
    "    id_col='id',\n"
    "    event_col='DEATH_EVENT',\n"
    "    start_col='start',\n"
    "    stop_col='stop'\n"
    ")\n"
    "ctv.print_summary(5, model='Cox z interakcja czas x serum_creatinine')\n"
))

S.append(code(
    "# Wykres krzywej przezyycia wg modelu Coxa dla mediany danych\n"
    "median_patient = df[sig_vars].median().to_frame().T\n\n"
    "fig, axes = plt.subplots(1, 2, figsize=(14, 6))\n\n"
    "cph_red.predict_survival_function(median_patient).plot(ax=axes[0])\n"
    "axes[0].set_title('Funkcja przezycia Coxa – medianowy pacjent')\n"
    "axes[0].set_xlabel('Czas (dni)')\n"
    "axes[0].set_ylabel('S(t)')\n"
    "axes[0].grid(True)\n\n"
    "cph_red.predict_cumulative_hazard(median_patient).plot(ax=axes[1], color='red')\n"
    "axes[1].set_title('Skumulowany hazard Coxa – medianowy pacjent')\n"
    "axes[1].set_xlabel('Czas (dni)')\n"
    "axes[1].set_ylabel('H(t)')\n"
    "axes[1].grid(True)\n\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_cox_survival_hazard.png', dpi=150)\n"
    "plt.show()\n"
))

S.append(code(
    "# Porownanie przezyycia dla roznych wartosci ejection_fraction\n"
    "ef_values = [20, 30, 38, 50, 65]  # percentyle + wartosci kliniczne\n"
    "base_patient = df[sig_vars].median().to_frame().T.copy()\n\n"
    "plt.figure(figsize=(10, 6))\n"
    "for ef in ef_values:\n"
    "    p = base_patient.copy()\n"
    "    p['ejection_fraction'] = ef\n"
    "    sf = cph_red.predict_survival_function(p)\n"
    "    plt.plot(sf.index, sf.values.flatten(), linewidth=2,\n"
    "             label=f'EF = {ef}%')\n\n"
    "plt.title('Funkcja przezycia Coxa wg frakcji wyrzutowej (EF)\\n'\n"
    "          '(pozostale zmienne = mediana)')\n"
    "plt.xlabel('Czas (dni)')\n"
    "plt.ylabel('Prawdopodobienstwo przezycia S(t)')\n"
    "plt.legend()\n"
    "plt.grid(True)\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_cox_ef_comparison.png', dpi=150)\n"
    "plt.show()\n"
))

save(notebook(S), "C:/Users/patry/Desktop/Programs/ACT/hf_model_semiparametryczny.ipynb")

# ===========================================================================
# NOTEBOOK 3 – MODELE NIEPARAMETRYCZNE (Heart Failure)
# ===========================================================================

N = []

N.append(md(
    "# Modele nieparametryczne – zbiór danych Heart Failure\n\n"
    "Analiza czasu przeżycia metodami nieparametrycznymi: Kaplan-Meier, "
    "tablice trwania życia oraz wygładzanie kernelowe funkcji hazardu.\n\n"
    "- **Zmienna czasu**: `time` (dni)\n"
    "- **Zdarzenie**: `DEATH_EVENT = 1` (zgon)\n"
    "- **N = 299** obserwacji; 96 zgonów (32,1 %)"
))

N.append(code(
    "#!pip install lifelines pandas matplotlib numpy seaborn openpyxl\n\n"
    "import pandas as pd\n"
    "import numpy as np\n"
    "import matplotlib.pyplot as plt\n"
    "import seaborn as sns\n"
    "from lifelines import KaplanMeierFitter, NelsonAalenFitter\n"
    "from lifelines.plotting import add_at_risk_counts\n"
    "from lifelines.statistics import logrank_test, multivariate_logrank_test\n"
    "import warnings\n"
    "warnings.filterwarnings('ignore')\n\n"
    "plt.style.use('seaborn-v0_8-whitegrid')\n"
    "sns.set(font_scale=1.1)\n"
    "plt.rcParams['figure.figsize'] = (10, 6)\n\n"
    "df = pd.read_csv('heart_failure_clinical_records_dataset.csv')\n"
    "print('Ksztalt danych:', df.shape)\n"
    "display(df[['time', 'DEATH_EVENT']].describe().round(2))\n"
    "event_rate = df['DEATH_EVENT'].mean()\n"
    "print(f'Czestotliwosc zdarzen: {event_rate:.3f} '\n"
    "      f\"({df['DEATH_EVENT'].sum()} z {len(df)})\")\n"
))

N.append(md("## KOD 1.1 – Podstawowe statystyki i korelacje z czasem przeżycia"))

N.append(code(
    "selected_cols = ['age', 'anaemia', 'creatinine_phosphokinase', 'diabetes',\n"
    "                 'ejection_fraction', 'high_blood_pressure', 'platelets',\n"
    "                 'serum_creatinine', 'serum_sodium', 'sex', 'smoking', 'time']\n\n"
    "correlations = df[selected_cols].corr()['time'].sort_values(ascending=False).drop('time')\n"
    "corr_df = correlations.reset_index()\n"
    "corr_df.columns = ['Zmienna', 'Korelacja z czasem przezycia']\n\n"
    "print('Korelacje zmiennych z czasem przezycia:')\n"
    "display(corr_df.style\n"
    "        .background_gradient(cmap='coolwarm',\n"
    "                             subset=['Korelacja z czasem przezycia'])\n"
    "        .format({'Korelacja z czasem przezycia': '{:.4f}'}))\n\n"
    "plt.figure(figsize=(8, 6))\n"
    "sns.barplot(data=corr_df, y='Zmienna',\n"
    "            x='Korelacja z czasem przezycia',\n"
    "            palette='coolwarm_r', orient='h')\n"
    "plt.title('Korelacje zmiennych z czasem przezycia (Heart Failure)')\n"
    "plt.axvline(0, color='black', linewidth=0.8)\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_correlations_with_time.png', dpi=150)\n"
    "plt.show()\n"
))

N.append(md(
    "## KOD 1.2 – Krzywa Kaplana-Meiera z przedziałami ufności i tabelą osób narażonych\n\n"
    "Estymator K-M: $\\hat{S}(t) = \\prod_{t_i \\leq t} \\left(1 - \\frac{d_i}{n_i}\\right)$, "
    "gdzie $d_i$ – liczba zdarzeń, $n_i$ – liczba narażonych w chwili $t_i$."
))

N.append(code(
    "plt.figure(figsize=(12, 8))\n"
    "ax = plt.subplot(111)\n\n"
    "kmf = KaplanMeierFitter()\n"
    "kmf.fit(df['time'], df['DEATH_EVENT'], label='Estymator K-M', alpha=0.05)\n"
    "kmf.plot(ax=ax, ci_show=True, ci_alpha=0.3)\n"
    "add_at_risk_counts(kmf, ax=ax)\n\n"
    "plt.title('Krzywa przezycia Kaplana-Meiera z 95% przedzialem ufnosci\\n'\n"
    "          'Heart Failure (N=299, zdarzenia=96)')\n"
    "plt.xlabel('Czas (dni)')\n"
    "plt.ylabel('Prawdopodobienstwo przezycia')\n"
    "plt.grid(True)\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_km_overall.png', dpi=150)\n"
    "plt.show()\n\n"
    "print(f'Mediana czasu przezycia (K-M): {kmf.median_survival_time_:.1f} dni')\n"
))

N.append(md("## KOD 1.3 – Tabela przeżycia Kaplana-Meiera"))

N.append(code(
    "kmf_table = pd.DataFrame(kmf.survival_function_)\n"
    "kmf_table.columns = ['Przezycie']\n"
    "kmf_table['Dolny PU 95%'] = kmf.confidence_interval_.iloc[:, 0]\n"
    "kmf_table['Gorny PU 95%'] = kmf.confidence_interval_.iloc[:, 1]\n"
    "log_s = -np.log(np.clip(kmf.survival_function_.values.flatten(), 1e-10, 1))\n"
    "kmf_table['Skum. hazard H(t)'] = log_s\n"
    "kmf_table.loc[kmf_table.index[0], 'Skum. hazard H(t)'] = 0\n"
    "kmf_table['Zdarzenia'] = kmf.event_table['observed']\n"
    "kmf_table['Cenzurowane'] = kmf.event_table['censored']\n"
    "kmf_table['Narazeni na ryzyko'] = kmf.event_table['at_risk']\n\n"
    "print('Tabela przezycia K-M (pierwsze 15 wierszy):')\n"
    "display(kmf_table.head(15))\n"
    "print('\\nTabela przezycia K-M (ostatnie 10 wierszy):')\n"
    "display(kmf_table.tail(10))\n\n"
    "kmf_table.to_excel('hf_km_table.xlsx')\n"
    "print('Tabela zapisana do hf_km_table.xlsx')\n"
))

N.append(md(
    "## KOD 1.4 – Porównanie krzywych K-M wg zmiennych binarnych\n\n"
    "Porównujemy krzywe przeżycia dla wszystkich zmiennych binarnych: "
    "`sex`, `anaemia`, `diabetes`, `high_blood_pressure`, `smoking`. "
    "Weryfikacja testu log-rank: $H_0$: krzywe przeżycia są identyczne."
))

N.append(code(
    "binary_vars = {\n"
    "    'sex':                 {0: 'Kobieta', 1: 'Mezczyzna'},\n"
    "    'anaemia':             {0: 'Brak anemii', 1: 'Anemia'},\n"
    "    'diabetes':            {0: 'Brak cukrzycy', 1: 'Cukrzyca'},\n"
    "    'high_blood_pressure': {0: 'Brak NT', 1: 'Nadcisnienie'},\n"
    "    'smoking':             {0: 'Niepalacy', 1: 'Palacy'}\n"
    "}\n\n"
    "fig, axes = plt.subplots(2, 3, figsize=(18, 11))\n"
    "axes = axes.flatten()\n\n"
    "for idx, (var, labels_map) in enumerate(binary_vars.items()):\n"
    "    ax = axes[idx]\n"
    "    for val in sorted(df[var].unique()):\n"
    "        mask = df[var] == val\n"
    "        kmf_g = KaplanMeierFitter()\n"
    "        kmf_g.fit(df['time'][mask], df['DEATH_EVENT'][mask],\n"
    "                  label=labels_map.get(val, str(val)))\n"
    "        kmf_g.plot(ax=ax, ci_show=True)\n"
    "    lr = multivariate_logrank_test(df['time'], df[var], df['DEATH_EVENT'])\n"
    "    ax.set_title(f'{var}\\nlog-rank p = {lr.p_value:.4f}')\n"
    "    ax.set_xlabel('Czas (dni)')\n"
    "    ax.set_ylabel('S(t)')\n"
    "    ax.grid(True)\n\n"
    "axes[-1].set_visible(False)\n"
    "plt.suptitle('Porownanie krzywych K-M wg zmiennych binarnych (Heart Failure)',\n"
    "             fontsize=14, y=1.01)\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_km_binary_comparison.png', dpi=150, bbox_inches='tight')\n"
    "plt.show()\n"
))

N.append(code(
    "# Szczegolowe wyniki testow log-rank\n"
    "print('=== Testy log-rank i Wilcoxona dla zmiennych binarnych ===')\n"
    "for var, labels_map in binary_vars.items():\n"
    "    lr = multivariate_logrank_test(df['time'], df[var], df['DEATH_EVENT'])\n"
    "    wx = multivariate_logrank_test(df['time'], df[var], df['DEATH_EVENT'],\n"
    "                                   weightings='wilcoxon')\n"
    "    print(f'\\n{var}:')\n"
    "    print(f'  Log-rank:  p = {lr.p_value:.4f} '\n"
    "          f'({\"istotny\" if lr.p_value < 0.05 else \"nieistotny\"})')\n"
    "    print(f'  Wilcoxon:  p = {wx.p_value:.4f} '\n"
    "          f'({\"istotny\" if wx.p_value < 0.05 else \"nieistotny\"})')\n"
))

N.append(md(
    "## KOD 1.5 – Porównanie K-M wg kategoryzowanej frakcji wyrzutowej\n\n"
    "Frakcja wyrzutowa (EF) jest kluczowym klinicznym predyktorem. "
    "Kategoryzujemy ją na kwartyle i porównujemy krzywe przeżycia."
))

N.append(code(
    "df['ef_cat'] = pd.qcut(df['ejection_fraction'], q=4,\n"
    "                        labels=['Q1 (niska EF)', 'Q2', 'Q3', 'Q4 (wysoka EF)'])\n\n"
    "plt.figure(figsize=(12, 8))\n"
    "ax = plt.subplot(111)\n"
    "colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']\n\n"
    "kmf_list = []\n"
    "for i, cat in enumerate(df['ef_cat'].cat.categories):\n"
    "    mask = df['ef_cat'] == cat\n"
    "    kmf_ef = KaplanMeierFitter()\n"
    "    kmf_ef.fit(df['time'][mask], df['DEATH_EVENT'][mask], label=str(cat))\n"
    "    kmf_ef.plot(ax=ax, ci_show=True, color=colors[i])\n"
    "    kmf_list.append(kmf_ef)\n\n"
    "lr_ef = multivariate_logrank_test(df['time'], df['ef_cat'], df['DEATH_EVENT'])\n\n"
    "add_at_risk_counts(*kmf_list, ax=ax)\n"
    "plt.title(f'Krzywa K-M wg frakcji wyrzutowej (kwartyle)\\n'\n"
    "          f'log-rank p = {lr_ef.p_value:.4f}')\n"
    "plt.xlabel('Czas (dni)')\n"
    "plt.ylabel('Prawdopodobienstwo przezycia')\n"
    "plt.grid(True)\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_km_ef_quartiles.png', dpi=150)\n"
    "plt.show()\n"
))

N.append(md(
    "## KOD 2 – Tablica trwania życia (Life Table)\n\n"
    "Tablice trwania życia są starszą metodą nieparametryczną, "
    "grupującą obserwacje w przedziały czasu i obliczającą "
    "funkcję przeżycia oraz hazard dla każdego przedziału."
))

N.append(code(
    "def create_life_table(durations, events, intervals=None):\n"
    "    if intervals is None:\n"
    "        max_dur = max(durations)\n"
    "        intervals = np.linspace(0, max_dur, 11)[1:]\n\n"
    "    lt = pd.DataFrame({\n"
    "        'Poczatek': [0] + list(np.ceil(intervals)[:-1]),\n"
    "        'Koniec':    list(np.floor(intervals)),\n"
    "        'Srodek (t_jm)':  np.zeros(len(intervals)),\n"
    "        'Szerokosc (b_j)': np.zeros(len(intervals)),\n"
    "        'Narazeni (n_j)': np.zeros(len(intervals)),\n"
    "        'Zdarzenia (d_j)': np.zeros(len(intervals)),\n"
    "        'Cenzurowane (m_j)': np.zeros(len(intervals)),\n"
    "        'Hazard (h_j)':   np.zeros(len(intervals)),\n"
    "        'P(zdarzenia) q_j': np.zeros(len(intervals)),\n"
    "        'P(przezycia) p_j': np.zeros(len(intervals)),\n"
    "        'Przezycie S(t)':   np.zeros(len(intervals)),\n"
    "    })\n\n"
    "    for i, (start, end) in enumerate(zip(lt['Poczatek'], lt['Koniec'])):\n"
    "        in_interval = [(d > start) & (d <= end) for d in durations]\n"
    "        at_risk     = sum([d > start for d in durations])\n"
    "        events_i    = sum([e and (start < d <= end)\n"
    "                           for d, e in zip(durations, events)])\n"
    "        censored_i  = sum([(not e) and (start < d <= end)\n"
    "                           for d, e in zip(durations, events)])\n"
    "        width       = end - start\n"
    "        mid         = (start + end) / 2\n"
    "        eff_at_risk = at_risk - censored_i / 2\n"
    "        eff_at_risk = max(eff_at_risk, 0.001)\n\n"
    "        lt.at[i, 'Srodek (t_jm)']   = mid\n"
    "        lt.at[i, 'Szerokosc (b_j)'] = width\n"
    "        lt.at[i, 'Narazeni (n_j)']  = at_risk\n"
    "        lt.at[i, 'Zdarzenia (d_j)'] = events_i\n"
    "        lt.at[i, 'Cenzurowane (m_j)'] = censored_i\n"
    "        lt.at[i, 'P(zdarzenia) q_j'] = events_i / eff_at_risk\n"
    "        lt.at[i, 'P(przezycia) p_j'] = 1 - events_i / eff_at_risk\n"
    "        lt.at[i, 'Hazard (h_j)']    = events_i / (eff_at_risk * width)\n\n"
    "    S = 1.0\n"
    "    for i in range(len(lt)):\n"
    "        S *= lt.at[i, 'P(przezycia) p_j']\n"
    "        lt.at[i, 'Przezycie S(t)'] = S\n\n"
    "    return lt\n\n"
    "# Generowanie tablic zycia\n"
    "custom_intervals = [30, 60, 90, 120, 150, 180, 210, 240, 270, 285]\n"
    "lt = create_life_table(df['time'].tolist(), df['DEATH_EVENT'].tolist(),\n"
    "                        intervals=custom_intervals)\n\n"
    "print('Tablica trwania zycia (Heart Failure):')\n"
    "display(lt.round(4))\n"
    "lt.to_excel('hf_life_table.xlsx', index=False)\n"
    "print('Tablica zapisana do hf_life_table.xlsx')\n"
))

N.append(code(
    "# Wykres funkcji przezycia i hazardu z tablicy zycia\n"
    "fig, axes = plt.subplots(1, 2, figsize=(16, 6))\n\n"
    "axes[0].plot(lt['Koniec'], lt['Przezycie S(t)'], '-o',\n"
    "             color='#1f77b4', linewidth=2, markersize=6)\n"
    "axes[0].set_title('Funkcja przezycia z tablicy zycia (Heart Failure)')\n"
    "axes[0].set_xlabel('Czas (dni)')\n"
    "axes[0].set_ylabel('Prawdopodobienstwo przezycia S(t)')\n"
    "axes[0].set_ylim(0, 1)\n"
    "axes[0].grid(True)\n\n"
    "axes[1].plot(lt['Koniec'], lt['Hazard (h_j)'], '-o',\n"
    "             color='#d62728', linewidth=2, markersize=6)\n"
    "axes[1].set_title('Funkcja hazardu z tablicy zycia (Heart Failure)')\n"
    "axes[1].set_xlabel('Czas (dni)')\n"
    "axes[1].set_ylabel('Hazard h(t)')\n"
    "axes[1].grid(True)\n\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_life_table_plots.png', dpi=150)\n"
    "plt.show()\n"
))

N.append(md(
    "## KOD 3 – Logarytm funkcji przeżycia i diagnostyka rozkładu\n\n"
    "Wykresy $-\\log(\\hat{S}(t))$ oraz $\\log(-\\log(\\hat{S}(t)))$ vs $\\log(t)$ "
    "służą diagnostyce zgodności z rozkładami parametrycznymi:\n"
    "- Liniowość $-\\log(S(t))$ vs $t$ → rozkład wykładniczy\n"
    "- Liniowość $\\log(-\\log(S(t)))$ vs $\\log(t)$ → rozkład Weibulla\n"
    "- Proporcjonalność hazardów: równoległe krzywe $\\log(-\\log(S(t)))$ dla grup"
))

N.append(code(
    "fig, axes = plt.subplots(1, 2, figsize=(14, 6))\n\n"
    "# -log(S(t))\n"
    "log_s = -np.log(np.clip(kmf.survival_function_.values.flatten(), 1e-10, 1))\n"
    "axes[0].plot(kmf.survival_function_.index, log_s, 'o-', color='#1f77b4')\n"
    "axes[0].set_title('-log(S(t)) – diagnostyka rozkl. wyklad.')\n"
    "axes[0].set_xlabel('Czas (dni)')\n"
    "axes[0].set_ylabel('-log(S(t))')\n"
    "axes[0].grid(True)\n\n"
    "# log(-log(S(t))) vs log(t)\n"
    "t_idx = kmf.survival_function_.index\n"
    "valid = (log_s > 0) & (t_idx > 0)\n"
    "loglog_s = np.log(log_s[valid])\n"
    "log_t = np.log(t_idx[valid])\n"
    "axes[1].plot(log_t, loglog_s, 'o-', color='#ff7f0e')\n"
    "axes[1].set_title('log(-log(S(t))) vs log(t) – diagnostyka Weibulla')\n"
    "axes[1].set_xlabel('log(Czas)')\n"
    "axes[1].set_ylabel('log(-log(S(t)))')\n"
    "axes[1].grid(True)\n\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_log_survival_diagnostic.png', dpi=150)\n"
    "plt.show()\n\n"
    "# Diagnostyka proporcjonalnosci hazardow (log-log dla grup)\n"
    "plt.figure(figsize=(10, 6))\n"
    "for val, label in {0: 'Kobieta', 1: 'Mezczyzna'}.items():\n"
    "    mask = df['sex'] == val\n"
    "    kmf_g = KaplanMeierFitter()\n"
    "    kmf_g.fit(df['time'][mask], df['DEATH_EVENT'][mask], label=label)\n"
    "    S_g = np.clip(kmf_g.survival_function_.values.flatten(), 1e-10, 1)\n"
    "    t_g = kmf_g.survival_function_.index\n"
    "    loglog_g = np.log(-np.log(S_g))\n"
    "    plt.plot(np.log(t_g), loglog_g, label=label)\n"
    "plt.title('log(-log(S(t))) wg plci – diagnostyka proporcjonalnosci hazardow')\n"
    "plt.xlabel('log(Czas)')\n"
    "plt.ylabel('log(-log(S(t)))')\n"
    "plt.legend()\n"
    "plt.grid(True)\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_loglog_sex.png', dpi=150)\n"
    "plt.show()\n"
))

N.append(md(
    "## KOD 4 – Estymator Nelsona-Aalena i wygładzanie kernelowe hazardu\n\n"
    "Estymator Nelsona-Aalena: $\\hat{H}(t) = \\sum_{t_i \\leq t} \\frac{d_i}{n_i}$. "
    "Funkcja hazardu chwilowego jest obliczana przez wygładzanie kernelowe z różnymi pasmami."
))

N.append(code(
    "naf = NelsonAalenFitter()\n"
    "naf.fit(df['time'], df['DEATH_EVENT'])\n\n"
    "fig, axes = plt.subplots(2, 2, figsize=(14, 10))\n"
    "for i, bw in enumerate([20, 50, 100, 200]):\n"
    "    ax = axes[i // 2][i % 2]\n"
    "    hazard_smooth = naf.smoothed_hazard_(bandwidth=bw)\n"
    "    ax.plot(hazard_smooth, 'r-', linewidth=1.5)\n"
    "    ax.set_title(f'Wygladzony hazard (bandwidth={bw})')\n"
    "    ax.set_xlabel('Czas (dni)')\n"
    "    ax.set_ylabel('Hazard h(t)')\n"
    "    ax.grid(True)\n\n"
    "plt.suptitle('Wygladzanie kernelowe funkcji hazardu – Heart Failure', fontsize=13)\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_hazard_bandwidth.png', dpi=150)\n"
    "plt.show()\n"
))

N.append(code(
    "# Porownanie wygladzonego hazardu miedzy grupami ef_cat\n"
    "plt.figure(figsize=(12, 7))\n"
    "colors_ef = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']\n"
    "cats = df['ef_cat'].cat.categories\n\n"
    "for i, cat in enumerate(cats):\n"
    "    mask = df['ef_cat'] == cat\n"
    "    if mask.sum() < 10:\n"
    "        continue\n"
    "    naf_g = NelsonAalenFitter()\n"
    "    naf_g.fit(df['time'][mask], df['DEATH_EVENT'][mask])\n"
    "    hz = naf_g.smoothed_hazard_(bandwidth=50)\n"
    "    plt.plot(hz, color=colors_ef[i], linewidth=2, label=str(cat))\n\n"
    "plt.title('Wygladzony hazard wg frakcji wyrzutowej (EF)\\nbandwidth=50')\n"
    "plt.xlabel('Czas (dni)')\n"
    "plt.ylabel('Hazard h(t)')\n"
    "plt.legend()\n"
    "plt.grid(True)\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_hazard_ef_groups.png', dpi=150)\n"
    "plt.show()\n"
))

N.append(code(
    "# Porownanie hazardu dla zmiennych binarnych na jednym wykresie\n"
    "fig, axes = plt.subplots(2, 3, figsize=(18, 11))\n"
    "axes = axes.flatten()\n\n"
    "for idx, (var, labels_map) in enumerate(binary_vars.items()):\n"
    "    ax = axes[idx]\n"
    "    for val in sorted(df[var].unique()):\n"
    "        mask = df[var] == val\n"
    "        if mask.sum() < 5:\n"
    "            continue\n"
    "        naf_g = NelsonAalenFitter()\n"
    "        naf_g.fit(df['time'][mask], df['DEATH_EVENT'][mask])\n"
    "        hz = naf_g.smoothed_hazard_(bandwidth=50)\n"
    "        ax.plot(hz, linewidth=2,\n"
    "                label=labels_map.get(val, str(val)))\n"
    "    ax.set_title(f'Hazard wg {var}')\n"
    "    ax.set_xlabel('Czas (dni)')\n"
    "    ax.set_ylabel('Hazard h(t)')\n"
    "    ax.legend()\n"
    "    ax.grid(True)\n\n"
    "axes[-1].set_visible(False)\n"
    "plt.suptitle('Wygladzony hazard wg zmiennych binarnych', fontsize=13)\n"
    "plt.tight_layout()\n"
    "plt.savefig('hf_hazard_binary_groups.png', dpi=150)\n"
    "plt.show()\n"
))

save(notebook(N), "C:/Users/patry/Desktop/Programs/ACT/hf_modele_nieparametryczne.ipynb")

print("\nWszystkie 3 notebooki zostaly wygenerowane pomyslnie.")
