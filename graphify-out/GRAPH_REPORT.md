# Graph Report - C:/Users/patry/Desktop/Programs/ACT  (2026-04-15)

## Corpus Check
- Corpus is ~13,847 words - fits in a single context window. You may not need a graph.

## Summary
- 205 nodes · 255 edges · 20 communities detected
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 35 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Semiparametric Cox Models|Semiparametric Cox Models]]
- [[_COMMUNITY_Nonparametric Survival Methods|Nonparametric Survival Methods]]
- [[_COMMUNITY_ACT Project Overview|ACT Project Overview]]
- [[_COMMUNITY_Survival Analysis Fundamentals|Survival Analysis Fundamentals]]
- [[_COMMUNITY_Parametric Survival Models|Parametric Survival Models]]
- [[_COMMUNITY_Life Tables & Cohorts|Life Tables & Cohorts]]
- [[_COMMUNITY_AFT Hazard Profiles|AFT Hazard Profiles]]
- [[_COMMUNITY_AFT Survival Profiles|AFT Survival Profiles]]
- [[_COMMUNITY_Censoring Mechanisms|Censoring Mechanisms]]
- [[_COMMUNITY_Competing Risks & Extensions|Competing Risks & Extensions]]
- [[_COMMUNITY_AFT Model Comparison (AIC)|AFT Model Comparison (AIC)]]
- [[_COMMUNITY_Heart Failure Censoring Data|Heart Failure Censoring Data]]
- [[_COMMUNITY_Notebook Generation Code|Notebook Generation Code]]
- [[_COMMUNITY_Partial Likelihood Estimation|Partial Likelihood Estimation]]
- [[_COMMUNITY_Core Survival Functions|Core Survival Functions]]
- [[_COMMUNITY_Event & Episode Concepts|Event & Episode Concepts]]
- [[_COMMUNITY_Variable Covariates|Variable Covariates]]
- [[_COMMUNITY_Secondary Covariates|Secondary Covariates]]
- [[_COMMUNITY_Cross-Sectional Study Design|Cross-Sectional Study Design]]
- [[_COMMUNITY_Panel Study Design|Panel Study Design]]

## God Nodes (most connected - your core abstractions)
1. `Cox Proportional Hazards Model` - 15 edges
2. `Survival Analysis (Analiza czasu trwania)` - 11 edges
3. `Nonparametric Models (Modele nieparametryczne)` - 10 edges
4. `HF AFT Survival Profiles Plot` - 9 edges
5. `Life Tables (Tablice trwania życia)` - 9 edges
6. `PROC LIFETEST (SAS Procedure)` - 8 edges
7. `Time-Varying Covariates` - 8 edges
8. `analiza_parametryczna.ipynb (Parametric AFT Models)` - 7 edges
9. `Censoring (Obcięcie)` - 7 edges
10. `Partial Likelihood Method (Maximum Partial Likelihood)` - 7 edges

## Surprising Connections (you probably didn't know these)
- `TODO: Add Probability Plot for Log Survival Function` --references--> `analiza_parametryczna.ipynb (Parametric AFT Models)`  [INFERRED]
  notatak.txt → CLAUDE.md
- `Rationale: SAS Code Is Fuller/More Complete Reference` --rationale_for--> `ACT_projekt_nieparam.sas (SAS PROC LIFETEST)`  [INFERRED]
  notatak.txt → CLAUDE.md
- `TODO: Check Proportionality in Semiparametric Model` --references--> `model_semiparametryczny.ipynb (Cox PH Semiparametric)`  [EXTRACTED]
  notatak.txt → CLAUDE.md
- `TODO: Port SAS Code to Python` --references--> `ACT_projekt_nieparam.sas (SAS PROC LIFETEST)`  [EXTRACTED]
  notatak.txt → CLAUDE.md
- `TODO: Check Proportionality in Semiparametric Model` --references--> `Cox Proportional Hazards Model`  [INFERRED]
  notatak.txt → CLAUDE.md

## Communities

### Community 0 - "Semiparametric Cox Models"
Cohesion: 0.07
Nodes (36): AIC/BIC Information Criteria for Survival Models, Alcoholic Cirrhosis Dataset (example dataset), Baseline Hazard Function, Baseline Survival Function Estimation, Blood Data (example dataset), Counting Process (data coding approach), Cox Proportional Hazards Model, Exponential Model (special case of PH) (+28 more)

### Community 1 - "Nonparametric Survival Methods"
Cohesion: 0.1
Nodes (30): Accelerated Failure Time Model (AFT Model), Actuarial Method / Life Table Method (Metoda tradycyjna/aktuarialna), Censoring / Censored Observations (Obserwacje obcięte), Confidence Intervals for S(t) – CL and CB (EP), Cumulative Hazard Function H(t), Density Function (Funkcja gęstości), Exponential Model (constant hazard, suggested by LS plot linearity), Fleming-Harrington Test (generalization with parameters p, q) (+22 more)

### Community 2 - "ACT Project Overview"
Cohesion: 0.16
Nodes (19): ACT Survival Analysis Project, aids_data.csv (ACTG175 HIV/AIDS Trial), analiza_parametryczna.ipynb (Parametric AFT Models), Cox Proportional Hazards Model, heart_failure_clinical_records_dataset.csv, Kaplan-Meier Estimator, lifelines (Python Survival Analysis Library), Log-Logistic AFT Model (+11 more)

### Community 3 - "Survival Analysis Fundamentals"
Cohesion: 0.12
Nodes (17): Causality Mechanism (Mechanizm przyczynowości), Competing Risks Model, Fixed Covariates (Cechy stałe), Duration Analysis / Transition Analysis (economics domain), Event History Analysis, Longitudinal Study (Badanie wzdłużne), Multi-Episode Model, Multi-State Model (including competing risks) (+9 more)

### Community 4 - "Parametric Survival Models"
Cohesion: 0.14
Nodes (14): Cox Proportional Hazards Regression, Gompertz Model, Kaplan-Meier Estimator, Life Tables (Tablice trwania życia), Log-Logistic Model, Log-Normal Model, Nonparametric Models (Modele nieparametryczne), Parametric Models (Modele parametryczne) (+6 more)

### Community 5 - "Life Tables & Cohorts"
Cohesion: 0.18
Nodes (11): Abridged Life Tables (Tablice skrócone – 5-letnie przedziały), Birth Cohort (Kohorta urodzeniowa), Cohort (Kohorta) – group defined by a shared event, Cohort Life Tables (Tablice kohortowe), Complete Life Tables (Tablice pełne – roczne przedziały), Cross-Sectional Life Tables (Tablice przekrojowe), John Graunt (1662), Life Tables (Tablice trwania życia) (+3 more)

### Community 6 - "AFT Hazard Profiles"
Cohesion: 0.36
Nodes (10): HF AFT Hazard Profiles Figure, Hazard Function h(t), Heart Failure Clinical Records Dataset, Log-Normal AFT Model, Patient A – Low Risk Profile, Patient B – Medium Risk Profile, Patient C – High Risk Profile, Patient D – High Risk Profile (+2 more)

### Community 7 - "AFT Survival Profiles"
Cohesion: 0.36
Nodes (10): Heart Failure Clinical Records Dataset, HF AFT Survival Profiles Plot, Log-Normal AFT Model, Patient A – Low Risk Profile, Patient B – Medium Risk Profile, Patient C – High Risk Profile, Patient D – High Risk Profile, Risk Stratification (Low / Medium / High) (+2 more)

### Community 8 - "Censoring Mechanisms"
Cohesion: 0.2
Nodes (10): Censoring (Obcięcie), Left Censoring (Obcięcie lewostronne), Myelomatosis Data (example dataset), Noninformative Censoring (key assumption of survival analysis), Random Censoring (uncontrolled censoring), Rationale: Noninformative censoring is required so that censored individuals represent all survivors at that time point, Cox & Oakes (1984) - Noninformative Censoring reference, Right Censoring (Obcięcie prawostronne) (+2 more)

### Community 9 - "Competing Risks & Extensions"
Cohesion: 0.22
Nodes (9): Aneta Ptak-Chmielewska, Competing Risks Model (Model ryzyka konkurencyjnego), Multi-Episode Model (Model wielu epizodów), Myelomatosis Data (Example Dataset), Analiza czasu trwania – modele nieparametryczne (Presentation), Recidivism Data (Example Dataset – recid), Single Episode Model (Model pojedynczych epizodów), Survival Analysis (Analiza czasu trwania / przeżycia) (+1 more)

### Community 10 - "AFT Model Comparison (AIC)"
Cohesion: 0.86
Nodes (7): Parametric AFT Survival Analysis, AIC Model Selection Criterion, HF AFT Model AIC Comparison Chart, Heart Failure Clinical Records Dataset, Log-Logistic AFT Model (Heart Failure), Log-Normal AFT Model (Heart Failure), Weibull AFT Model (Heart Failure)

### Community 11 - "Heart Failure Censoring Data"
Cohesion: 0.52
Nodes (7): Right Censoring (Survival Analysis Concept), Censored Observations (67.9%), Heart Failure Clinical Records Dataset, Death Events / Zgon (32.1%), Event vs Censoring Proportion Pie Chart, HF Censoring Analysis Chart, Observation Time Distribution by Status (Histogram)

### Community 12 - "Notebook Generation Code"
Cohesion: 0.33
Nodes (1): Generator trzech notebooków Jupyter dla zbioru Heart Failure.

### Community 13 - "Partial Likelihood Estimation"
Cohesion: 0.47
Nodes (6): Breslow Approximation for Tied Events, Discrete Time Method (TIES=DISCRETE), Efron Approximation for Tied Events, Exact Method for Tied Events (TIES=EXACT), Proportional Odds Model (Discrete Time), Tied Data Handling

### Community 14 - "Core Survival Functions"
Cohesion: 0.4
Nodes (5): Cumulative Distribution Function (Dystrybuanta), Cumulative Hazard Function H(t), Hazard Function (Funkcja hazardu), Probability Density Function (Funkcja gęstości), Survival Function (Funkcja przeżycia)

### Community 15 - "Event & Episode Concepts"
Cohesion: 0.5
Nodes (4): Career (Kariera) - sequence of events, Episode (Epizod), Event (Zdarzenie) - state transition, Primary Covariates (Cechy pierwotne) - state identification

### Community 16 - "Variable Covariates"
Cohesion: 1.0
Nodes (1): Time-Varying Covariates (Cechy zmienne)

### Community 17 - "Secondary Covariates"
Cohesion: 1.0
Nodes (1): Secondary Covariates (Cechy wtórne) - unit differentiation

### Community 18 - "Cross-Sectional Study Design"
Cohesion: 1.0
Nodes (1): Cross-Sectional Study (Badanie przekrojowe)

### Community 19 - "Panel Study Design"
Cohesion: 1.0
Nodes (1): Panel Study (Badanie panelowe)

## Knowledge Gaps
- **81 isolated node(s):** `Generator trzech notebooków Jupyter dla zbioru Heart Failure.`, `Heart Failure Clinical Records Dataset`, `Heart Failure Clinical Records Dataset`, `Follow-up Time (Days, 0–280)`, `Weibull AFT Model` (+76 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Variable Covariates`** (1 nodes): `Time-Varying Covariates (Cechy zmienne)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Secondary Covariates`** (1 nodes): `Secondary Covariates (Cechy wtórne) - unit differentiation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Cross-Sectional Study Design`** (1 nodes): `Cross-Sectional Study (Badanie przekrojowe)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Panel Study Design`** (1 nodes): `Panel Study (Badanie panelowe)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Nonparametric Models (Modele nieparametryczne)` connect `Nonparametric Survival Methods` to `Competing Risks & Extensions`, `Life Tables & Cohorts`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `Life Tables (Tablice trwania życia)` connect `Life Tables & Cohorts` to `Nonparametric Survival Methods`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **What connects `Generator trzech notebooków Jupyter dla zbioru Heart Failure.`, `Heart Failure Clinical Records Dataset`, `Heart Failure Clinical Records Dataset` to the rest of the system?**
  _81 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Semiparametric Cox Models` be split into smaller, more focused modules?**
  _Cohesion score 0.07 - nodes in this community are weakly interconnected._
- **Should `Nonparametric Survival Methods` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._
- **Should `Survival Analysis Fundamentals` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._
- **Should `Parametric Survival Models` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._