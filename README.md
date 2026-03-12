# 🏦 Gamified Simulation for Liquidity Risk Management During Market Stress

**A Beginner Data Science Portfolio Project**

---

## 📌 What Is This Project About?

This project simulates **liquidity risk** — the risk that a bank runs out of cash during a financial crisis.

Using simple Python code, we:
- 🎮 Simulate 4 different stress scenarios like a game
- 📊 Calculate basic liquidity metrics (LCR, funding gap)
- 📈 Generate charts showing how cash drains during crises
- 💡 Make it beginner-friendly with lots of comments

---

## 💡 Key Concepts Explained Simply

| Concept | Simple Explanation |
|---|---|
| **Liquidity Risk** | Not having enough cash when you need it |
| **LCR (Liquidity Coverage Ratio)** | Do you have 30 days of cash reserves? Must be ≥ 100% |
| **Bank Run** | Everyone withdraws money at once |
| **Margin Call** | Lender demands extra collateral during market drops |
| **Fire Sale** | Selling assets quickly at a big discount |
| **Funding Crisis** | Short-term lenders stop lending to you |

---

## 📁 Project Structure

```
liquidity_risk_project/
│
├── data/
│   └── simulation_results.csv    ← Generated simulation data
│
├── plots/
│   ├── cash_levels.png           ← Cash comparison chart
│   ├── lcr_over_time.png         ← LCR chart
│   ├── scenario_comparison.png   ← 2x2 scenario grid
│   ├── cash_flow_projection.png  ← Baseline cash flow
│   ├── stress_test_summary.png   ← Final score bar chart
│   └── heatmap_lcr.png           ← LCR heatmap
│
├── simulation.py                 ← Main Python code
├── notebook.ipynb                ← Jupyter Notebook walkthrough
└── README.md                     ← This file!
```

---

## 🚀 How to Run This Project

### Option 1: Google Colab (Easiest — No Installation Needed!)

1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Create a new notebook
3. Upload `simulation.py` to Colab (Files panel on the left)
4. In a new cell, run:

```python
# Install libraries (already on Colab, but just in case)
!pip install pandas numpy matplotlib seaborn

# Run the simulation
exec(open('simulation.py').read())
scenarios, data = run_all_scenarios()
```

### Option 2: Jupyter Notebook (Local)

1. Make sure you have Python installed
2. Install dependencies:
```bash
pip install pandas numpy matplotlib seaborn jupyter
```
3. Open the notebook:
```bash
jupyter notebook notebook.ipynb
```

### Option 3: Run Python Script Directly

```bash
cd liquidity_risk_project
python simulation.py
```

---

## 🎮 Adjust the Difficulty!

You can change the parameters to simulate harder or easier crises:

```python
# Easy Mode (mild stress)
scenarios, data = run_all_scenarios(
    withdrawal_rate=0.05,       # Only 5% daily withdrawals
    volatility=0.02,            # Low market volatility
    discount_rate=0.15,         # 15% fire sale discount
    funding_reduction_rate=0.03
)

# Hard Mode (severe crisis)
scenarios, data = run_all_scenarios(
    withdrawal_rate=0.25,       # 25% daily withdrawals
    volatility=0.15,            # High volatility
    discount_rate=0.50,         # 50% fire sale discount
    funding_reduction_rate=0.20
)
```

---

## 📊 What Charts Are Generated?

1. **Cash Levels Chart** — How cash drops across all 4 scenarios
2. **LCR Over Time** — Whether the bank stays above the 100% safety line
3. **Scenario Comparison Grid** — Side-by-side 2x2 comparison
4. **Cash Flow Projection** — Baseline 30-day forecast
5. **Stress Test Summary** — Final score bar chart
6. **LCR Heatmap** — Color-coded risk overview

---

## 🛠️ Libraries Used

| Library | Purpose |
|---|---|
| `pandas` | Data tables and CSV export |
| `numpy` | Math calculations and random numbers |
| `matplotlib` | Basic charts and plots |
| `seaborn` | Heatmaps and styled visualizations |

---

## 📚 What I Learned

- What liquidity risk means in real banking
- How to simulate financial scenarios with Python
- How to calculate basic metrics like LCR
- How to create visualizations to tell a data story
- How market stress events chain together (e.g., fire sale → funding crisis)

---

## 👤 Author

**Beginner Data Science Student**  
Portfolio Project | Learning Finance + Python + Data Visualization

---

*This project is for educational purposes only. All numbers are fictional.*
