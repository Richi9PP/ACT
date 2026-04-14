# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Survival analysis project (ACT) examining censored time-to-event data across two clinical datasets:
- **aids_data.csv** — ACTG175 HIV/AIDS clinical trial (2,139 observations)
- **heart_failure_clinical_records_dataset.csv** — Heart failure outcomes (299 observations)

## Environment Setup

```bash
# Activate the virtual environment (Windows)
.venv/Scripts/activate

# Install core dependencies if missing
pip install lifelines pandas matplotlib numpy jupyter
```

## Running the Analysis

```bash
# Launch a specific notebook
jupyter notebook analiza_parametryczna.ipynb
jupyter notebook model_semiparametryczny.ipynb
jupyter notebook modele_nieparametryczne.ipynb

# Run SAS analysis (requires SAS installation)
sas ACT_projekt_nieparam.sas
```

## Architecture

This is a research project — analysis lives in Jupyter notebooks, not application code. Data flows: CSV → pandas DataFrame → lifelines model → plots/summary tables.

| Notebook | Analysis type | Key methods |
|---|---|---|
| `analiza_parametryczna.ipynb` | Parametric AFT models | Weibull, Log-Normal, Log-Logistic; AIC/concordance comparison |
| `model_semiparametryczny.ipynb` | Semiparametric | Cox PH, Cox time-varying covariates, PH assumption tests |
| `modele_nieparametryczne.ipynb` | Nonparametric | Kaplan-Meier, life tables, stratification |
| `ACT_projekt_nieparam.sas` | SAS equivalent | `PROC LIFETEST` for life tables, survival/hazard plots |

All analyses handle **right-censored** data. Event indicators and duration columns differ by dataset — check the data-loading cells at the top of each notebook before modifying model calls.
