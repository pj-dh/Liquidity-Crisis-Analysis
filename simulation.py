"""
=============================================================
  GAMIFIED SIMULATION FOR LIQUIDITY RISK MANAGEMENT
  DURING MARKET STRESS
=============================================================
  Author  : Beginner Data Science Student
  Purpose : Simulate liquidity risk scenarios to understand
            how banks and financial institutions manage cash
            during stressful market conditions.
  Level   : Beginner
=============================================================

WHAT IS LIQUIDITY RISK?
------------------------
Liquidity risk is the danger that a bank or company cannot
meet its short-term financial obligations because it doesn't
have enough cash or assets it can quickly convert to cash.

Think of it like this: imagine you have money in a savings
account, but all your money is tied up in a house. If you
suddenly need cash for an emergency, you can't quickly sell
your house. That's liquidity risk!
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# Set a nice style for all charts
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("husl")

# ─────────────────────────────────────────────────────────
# SECTION 1 — INITIAL BANK SETUP (Our "Game" Starting Point)
# ─────────────────────────────────────────────────────────

def setup_bank(
    initial_cash=500,        # Cash on hand (in millions $)
    total_deposits=2000,     # Total customer deposits
    liquid_assets=800,       # Assets easily converted to cash
    short_term_funding=600,  # Money borrowed short-term
    daily_inflow=50,         # Normal daily cash coming in
    daily_outflow=45         # Normal daily cash going out
):
    """
    Creates a simple bank balance sheet as a dictionary.
    Think of this as the starting screen of our game —
    these are the bank's initial stats!

    Parameters:
        initial_cash        : Starting cash reserves
        total_deposits      : How much customers have deposited
        liquid_assets       : Assets that can be sold quickly
        short_term_funding  : Short-term loans the bank took
        daily_inflow        : Daily cash received (loans repaid, fees)
        daily_outflow       : Daily cash paid (operations, interest)

    Returns:
        A dictionary representing the bank's financial state
    """
    bank = {
        "cash": initial_cash,
        "liquid_assets": liquid_assets,
        "total_deposits": total_deposits,
        "short_term_funding": short_term_funding,
        "daily_inflow": daily_inflow,
        "daily_outflow": daily_outflow,
        "net_stable_funding": liquid_assets * 0.85,  # Stable funding available
    }
    print("=" * 55)
    print("  🏦  BANK SETUP COMPLETE — STARTING STATS")
    print("=" * 55)
    for key, value in bank.items():
        print(f"  {key:<25}: ${value:>8,.1f}M")
    print("=" * 55)
    return bank


# ─────────────────────────────────────────────────────────
# SECTION 2 — LIQUIDITY METRICS (The Score Board)
# ─────────────────────────────────────────────────────────

def calculate_lcr(hqla, net_cash_outflows_30d):
    """
    Calculates the Liquidity Coverage Ratio (LCR).

    WHAT IS LCR?
    LCR tells us if a bank has enough 'high quality liquid assets'
    (HQLA) to survive 30 days of cash outflows during a crisis.

    Formula:  LCR = HQLA / Net Cash Outflows (30 days) × 100

    A healthy LCR should be >= 100%.
    Below 100% = DANGER ZONE (the bank may run out of cash!)

    Parameters:
        hqla                 : High Quality Liquid Assets (cash + bonds)
        net_cash_outflows_30d: Expected cash going out in 30 days

    Returns:
        LCR as a percentage
    """
    if net_cash_outflows_30d == 0:
        return float("inf")
    lcr = (hqla / net_cash_outflows_30d) * 100
    return round(lcr, 2)


def calculate_funding_gap(cash_inflows, cash_outflows):
    """
    Calculates the short-term funding gap.

    WHAT IS FUNDING GAP?
    It's the difference between money coming IN and money going OUT.
    Negative gap = the bank needs to find extra funding — risky!

    Formula: Funding Gap = Cash Inflows - Cash Outflows

    Parameters:
        cash_inflows  : Total cash expected to come in
        cash_outflows : Total cash expected to go out

    Returns:
        Funding gap (negative means shortfall)
    """
    return round(cash_inflows - cash_outflows, 2)


def calculate_cash_reserve_ratio(cash, total_deposits):
    """
    Calculates what % of deposits the bank holds as cash.

    WHAT IS CASH RESERVE RATIO?
    Regulators require banks to keep a minimum % of deposits as cash.
    Low ratio = the bank is lending out too much and keeping too little.

    Formula: Cash Reserve Ratio = (Cash / Total Deposits) × 100

    Parameters:
        cash           : Current cash on hand
        total_deposits : Total customer deposits

    Returns:
        Cash reserve ratio as a percentage
    """
    if total_deposits == 0:
        return 0
    return round((cash / total_deposits) * 100, 2)


# ─────────────────────────────────────────────────────────
# SECTION 3 — STRESS SCENARIOS (Game Levels!)
# ─────────────────────────────────────────────────────────

def scenario_bank_run(bank, withdrawal_rate=0.10, days=30):
    """
    ════════════════════════════════════
    🚨 SCENARIO 1: BANK RUN
    ════════════════════════════════════
    WHAT IS A BANK RUN?
    When many customers panic and try to withdraw all their money
    at once (think of the movie 'It's a Wonderful Life'!).
    The bank doesn't have all the cash on hand, so it faces a crisis.

    Parameters:
        bank            : Bank dictionary from setup_bank()
        withdrawal_rate : % of deposits withdrawn each day (e.g., 0.10 = 10%)
        days            : Number of days to simulate

    Returns:
        DataFrame with daily cash levels, LCR, and metrics
    """
    print(f"\n🚨 Running Bank Run Scenario — {withdrawal_rate*100:.0f}% daily withdrawals")

    results = []
    cash = bank["cash"]
    liquid_assets = bank["liquid_assets"]
    deposits = bank["total_deposits"]

    for day in range(1, days + 1):
        # Each day, customers withdraw a % of remaining deposits
        daily_withdrawal = deposits * withdrawal_rate
        deposits = max(0, deposits - daily_withdrawal)

        # Cash goes down as withdrawals happen
        cash = cash - daily_withdrawal + bank["daily_inflow"]
        cash = max(0, cash)  # Cash can't go below 0

        # If cash runs out, sell liquid assets (fire sale at 90% value)
        if cash < 0:
            assets_sold = min(liquid_assets, abs(cash) / 0.90)
            liquid_assets = max(0, liquid_assets - assets_sold)
            cash = max(0, cash + assets_sold * 0.90)

        # Calculate metrics for this day
        hqla = cash + liquid_assets * 0.85
        net_outflows_30d = daily_withdrawal * 30
        lcr = calculate_lcr(hqla, net_outflows_30d)
        crr = calculate_cash_reserve_ratio(cash, deposits if deposits > 0 else 1)

        results.append({
            "Day": day,
            "Cash ($M)": round(cash, 2),
            "Liquid Assets ($M)": round(liquid_assets, 2),
            "Remaining Deposits ($M)": round(deposits, 2),
            "LCR (%)": lcr,
            "Cash Reserve Ratio (%)": crr,
            "Scenario": "Bank Run"
        })

    df = pd.DataFrame(results)
    print(f"  ✅ Day 1 Cash: ${df['Cash ($M)'].iloc[0]:.1f}M  →  Day {days} Cash: ${df['Cash ($M)'].iloc[-1]:.1f}M")
    return df


def scenario_margin_call(bank, volatility=0.05, collateral_req_increase=0.20, days=30):
    """
    ════════════════════════════════════
    📉 SCENARIO 2: MARGIN CALL
    ════════════════════════════════════
    WHAT IS A MARGIN CALL?
    When markets are volatile, lenders demand extra collateral
    (security deposits). If you can't pay, they close your position.
    Like a landlord suddenly demanding a bigger security deposit!

    Parameters:
        bank                     : Bank dictionary
        volatility               : Daily market price swings (0.05 = 5%)
        collateral_req_increase  : Extra collateral demanded each day
        days                     : Days to simulate

    Returns:
        DataFrame with cash levels and collateral requirements
    """
    print(f"\n📉 Running Margin Call Scenario — {volatility*100:.0f}% volatility, "
          f"{collateral_req_increase*100:.0f}% collateral increase")

    results = []
    cash = bank["cash"]
    liquid_assets = bank["liquid_assets"]
    collateral_held = bank["short_term_funding"] * 0.10  # Initial collateral

    np.random.seed(42)  # For reproducibility

    for day in range(1, days + 1):
        # Market moves randomly each day (up or down)
        market_move = np.random.uniform(-volatility, volatility)

        # Higher volatility → lender demands more collateral
        extra_collateral = collateral_held * collateral_req_increase * abs(market_move / volatility)
        collateral_held += extra_collateral

        # Pay collateral from cash
        cash = cash - extra_collateral + bank["daily_inflow"] - bank["daily_outflow"]
        cash = max(0, cash)

        # If cash too low, sell liquid assets
        if cash < extra_collateral:
            sold = min(liquid_assets, extra_collateral * 1.1)
            liquid_assets = max(0, liquid_assets - sold)
            cash += sold * 0.92  # Sell at slight discount

        hqla = cash + liquid_assets * 0.85
        net_outflows_30d = extra_collateral * 30
        lcr = calculate_lcr(hqla, max(net_outflows_30d, 1))
        crr = calculate_cash_reserve_ratio(cash, bank["total_deposits"])

        results.append({
            "Day": day,
            "Cash ($M)": round(cash, 2),
            "Liquid Assets ($M)": round(liquid_assets, 2),
            "Collateral Required ($M)": round(collateral_held, 2),
            "Market Move (%)": round(market_move * 100, 2),
            "LCR (%)": lcr,
            "Cash Reserve Ratio (%)": crr,
            "Scenario": "Margin Call"
        })

    df = pd.DataFrame(results)
    print(f"  ✅ Day 1 Cash: ${df['Cash ($M)'].iloc[0]:.1f}M  →  Day {days} Cash: ${df['Cash ($M)'].iloc[-1]:.1f}M")
    return df


def scenario_fire_sale(bank, discount_rate=0.30, forced_selling_pct=0.05, days=30):
    """
    ════════════════════════════════════
    🔥 SCENARIO 3: ASSET FIRE SALE
    ════════════════════════════════════
    WHAT IS A FIRE SALE?
    When a bank desperately needs cash, it sells assets quickly —
    but at a BIG discount. It's like selling your car in one day;
    you'll get much less than its true value.

    Parameters:
        bank               : Bank dictionary
        discount_rate      : How much below fair value assets sell (0.30 = 30% off)
        forced_selling_pct : % of assets force-sold each day
        days               : Days to simulate

    Returns:
        DataFrame tracking asset values and cash recovered
    """
    print(f"\n🔥 Running Fire Sale Scenario — {discount_rate*100:.0f}% discount, "
          f"{forced_selling_pct*100:.0f}% assets sold daily")

    results = []
    cash = bank["cash"]
    liquid_assets = bank["liquid_assets"]
    fair_value = liquid_assets  # Track what assets are REALLY worth

    for day in range(1, days + 1):
        # Force sell a portion of assets at a discount
        assets_to_sell = liquid_assets * forced_selling_pct
        cash_recovered = assets_to_sell * (1 - discount_rate)  # Sell below fair value

        liquid_assets = max(0, liquid_assets - assets_to_sell)
        cash = cash + cash_recovered + bank["daily_inflow"] - bank["daily_outflow"]
        cash = max(0, cash)

        # Value destroyed = the discount loss
        value_destroyed = assets_to_sell * discount_rate

        hqla = cash + liquid_assets * 0.85
        net_outflows_30d = bank["daily_outflow"] * 30
        lcr = calculate_lcr(hqla, net_outflows_30d)
        crr = calculate_cash_reserve_ratio(cash, bank["total_deposits"])

        results.append({
            "Day": day,
            "Cash ($M)": round(cash, 2),
            "Liquid Assets ($M)": round(liquid_assets, 2),
            "Cash Recovered from Sales ($M)": round(cash_recovered, 2),
            "Value Destroyed ($M)": round(value_destroyed, 2),
            "LCR (%)": lcr,
            "Cash Reserve Ratio (%)": crr,
            "Scenario": "Fire Sale"
        })

    df = pd.DataFrame(results)
    print(f"  ✅ Day 1 Cash: ${df['Cash ($M)'].iloc[0]:.1f}M  →  Day {days} Cash: ${df['Cash ($M)'].iloc[-1]:.1f}M")
    return df


def scenario_funding_crisis(bank, funding_reduction_rate=0.08, days=30):
    """
    ════════════════════════════════════
    💸 SCENARIO 4: FUNDING CRISIS
    ════════════════════════════════════
    WHAT IS A FUNDING CRISIS?
    Banks borrow short-term money (e.g., overnight loans) regularly.
    During a crisis, lenders stop lending — leaving banks with a
    cash shortage. Like your credit card suddenly being cancelled!

    Parameters:
        bank                  : Bank dictionary
        funding_reduction_rate: How fast short-term funding dries up (per day)
        days                  : Days to simulate

    Returns:
        DataFrame showing funding gaps and cash levels
    """
    print(f"\n💸 Running Funding Crisis Scenario — {funding_reduction_rate*100:.0f}% daily funding reduction")

    results = []
    cash = bank["cash"]
    liquid_assets = bank["liquid_assets"]
    available_funding = bank["short_term_funding"]

    for day in range(1, days + 1):
        # Each day, less short-term funding is available
        available_funding = max(0, available_funding * (1 - funding_reduction_rate))

        # Funding gap = what the bank needed vs what it got
        funding_needed = bank["daily_outflow"] * 5  # Weekly funding need
        funding_gap = max(0, funding_needed - available_funding)

        # Fill gap with cash or sell assets
        cash = cash - funding_gap + bank["daily_inflow"]
        if cash < 0:
            assets_sold = min(liquid_assets, abs(cash) / 0.95)
            liquid_assets = max(0, liquid_assets - assets_sold)
            cash = max(0, cash + assets_sold * 0.95)

        hqla = cash + liquid_assets * 0.85
        net_outflows_30d = funding_needed * 6
        lcr = calculate_lcr(hqla, max(net_outflows_30d, 1))
        crr = calculate_cash_reserve_ratio(cash, bank["total_deposits"])

        results.append({
            "Day": day,
            "Cash ($M)": round(cash, 2),
            "Liquid Assets ($M)": round(liquid_assets, 2),
            "Available Funding ($M)": round(available_funding, 2),
            "Funding Gap ($M)": round(funding_gap, 2),
            "LCR (%)": lcr,
            "Cash Reserve Ratio (%)": crr,
            "Scenario": "Funding Crisis"
        })

    df = pd.DataFrame(results)
    print(f"  ✅ Day 1 Cash: ${df['Cash ($M)'].iloc[0]:.1f}M  →  Day {days} Cash: ${df['Cash ($M)'].iloc[-1]:.1f}M")
    return df


# ─────────────────────────────────────────────────────────
# SECTION 4 — VISUALIZATIONS (Our Charts & Dashboards)
# ─────────────────────────────────────────────────────────

COLORS = {
    "Bank Run": "#e74c3c",       # Red — danger
    "Margin Call": "#e67e22",    # Orange — warning
    "Fire Sale": "#9b59b6",      # Purple — severe
    "Funding Crisis": "#2980b9", # Blue — moderate
    "safe": "#27ae60",           # Green — safe zone
    "warning": "#f39c12",        # Yellow — caution
}


def plot_cash_levels(all_scenarios, save_path="plots/cash_levels.png"):
    """
    Plots cash levels over time for all 4 scenarios on one chart.
    This helps compare how fast each crisis drains cash.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    for df in all_scenarios:
        scenario_name = df["Scenario"].iloc[0]
        ax.plot(df["Day"], df["Cash ($M)"],
                label=scenario_name,
                color=COLORS[scenario_name],
                linewidth=2.5,
                marker="o", markersize=3)

    # Add a danger zone shading below $50M
    ax.axhspan(0, 50, alpha=0.1, color="red", label="⚠️ Critical Zone (<$50M)")
    ax.axhline(y=50, color="red", linestyle="--", alpha=0.5, linewidth=1)

    ax.set_title("💰 Cash Levels During Different Stress Scenarios",
                 fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Day", fontsize=12)
    ax.set_ylabel("Cash on Hand ($M)", fontsize=12)
    ax.legend(fontsize=10)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"  📊 Chart saved: {save_path}")


def plot_lcr_over_time(all_scenarios, save_path="plots/lcr_over_time.png"):
    """
    Plots the Liquidity Coverage Ratio (LCR) for all scenarios.
    The red line at 100% shows the regulatory minimum.
    Below 100% = bank may be in trouble!
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    for df in all_scenarios:
        scenario_name = df["Scenario"].iloc[0]
        # Cap LCR display at 500% for readability
        lcr_capped = df["LCR (%)"].clip(upper=500)
        ax.plot(df["Day"], lcr_capped,
                label=scenario_name,
                color=COLORS[scenario_name],
                linewidth=2.5,
                marker="s", markersize=3)

    # Regulatory minimum line
    ax.axhline(y=100, color="red", linestyle="--", linewidth=2,
               label="📏 Regulatory Minimum (100%)")
    ax.fill_between([0, 31], 0, 100, alpha=0.07, color="red")

    ax.set_title("📊 Liquidity Coverage Ratio (LCR) Over 30 Days",
                 fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Day", fontsize=12)
    ax.set_ylabel("LCR (%)", fontsize=12)
    ax.legend(fontsize=10)
    ax.set_ylim(bottom=0)

    # Add annotation
    ax.annotate("❌ Danger Zone\n(LCR < 100%)",
                xy=(15, 50), fontsize=9, color="red",
                ha="center", style="italic")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"  📊 Chart saved: {save_path}")


def plot_scenario_comparison(all_scenarios, save_path="plots/scenario_comparison.png"):
    """
    Creates a 2x2 grid of charts — one per scenario.
    Each chart shows both Cash and Liquid Assets over time.
    Great for side-by-side comparison!
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("🔍 Stress Scenario Comparison — Cash vs Liquid Assets",
                 fontsize=16, fontweight="bold", y=1.01)

    axes_flat = axes.flatten()

    for i, df in enumerate(all_scenarios):
        ax = axes_flat[i]
        scenario_name = df["Scenario"].iloc[0]

        ax.fill_between(df["Day"], df["Cash ($M)"], alpha=0.3,
                        color=COLORS[scenario_name], label="Cash")
        ax.plot(df["Day"], df["Cash ($M)"],
                color=COLORS[scenario_name], linewidth=2, label="Cash ($M)")
        ax.plot(df["Day"], df["Liquid Assets ($M)"],
                color="steelblue", linewidth=2, linestyle="--",
                label="Liquid Assets ($M)")

        ax.set_title(f"{scenario_name}", fontsize=12, fontweight="bold",
                     color=COLORS[scenario_name])
        ax.set_xlabel("Day", fontsize=9)
        ax.set_ylabel("Amount ($M)", fontsize=9)
        ax.legend(fontsize=8)
        ax.set_ylim(bottom=0)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"  📊 Chart saved: {save_path}")


def plot_cash_flow_projection(bank, days=30, save_path="plots/cash_flow_projection.png"):
    """
    Shows a simple baseline cash flow projection under normal (no stress) conditions.
    This is what the bank HOPES will happen — the best case.
    Compare this with stress scenarios to see the impact!
    """
    days_range = list(range(1, days + 1))
    cash = bank["cash"]
    cash_levels = []
    inflows = []
    outflows = []

    for day in days_range:
        # Small random variation in daily cash flows
        daily_in = bank["daily_inflow"] * np.random.uniform(0.9, 1.1)
        daily_out = bank["daily_outflow"] * np.random.uniform(0.9, 1.1)
        cash = cash + daily_in - daily_out
        cash_levels.append(round(cash, 2))
        inflows.append(round(daily_in, 2))
        outflows.append(round(daily_out, 2))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Top chart: cumulative cash level
    ax1.plot(days_range, cash_levels, color=COLORS["safe"],
             linewidth=2.5, label="Projected Cash Level")
    ax1.fill_between(days_range, cash_levels, alpha=0.2, color=COLORS["safe"])
    ax1.axhline(y=bank["cash"], color="gray", linestyle=":", label="Starting Cash")
    ax1.set_title("📈 30-Day Cash Flow Projection (Baseline — No Stress)",
                  fontsize=14, fontweight="bold")
    ax1.set_ylabel("Cash Balance ($M)", fontsize=11)
    ax1.legend()

    # Bottom chart: daily inflows vs outflows
    x = np.array(days_range)
    ax2.bar(x - 0.2, inflows, width=0.4, label="Daily Inflow",
            color=COLORS["safe"], alpha=0.8)
    ax2.bar(x + 0.2, outflows, width=0.4, label="Daily Outflow",
            color=COLORS["Bank Run"], alpha=0.8)
    ax2.set_title("📊 Daily Cash Inflows vs Outflows", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Day", fontsize=11)
    ax2.set_ylabel("Amount ($M)", fontsize=11)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"  📊 Chart saved: {save_path}")


def plot_stress_test_summary(all_scenarios, save_path="plots/stress_test_summary.png"):
    """
    Creates a summary bar chart showing final LCR and Cash for each scenario.
    This is like a final score card — how did each scenario end?
    """
    summary_data = []
    for df in all_scenarios:
        summary_data.append({
            "Scenario": df["Scenario"].iloc[0],
            "Final Cash ($M)": df["Cash ($M)"].iloc[-1],
            "Min LCR (%)": df["LCR (%)"].min(),
            "Final LCR (%)": df["LCR (%)"].iloc[-1],
        })
    summary = pd.DataFrame(summary_data)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("🏆 Stress Test Summary — Final Scores", fontsize=15, fontweight="bold")

    colors = [COLORS[s] for s in summary["Scenario"]]

    # Final Cash
    bars1 = ax1.bar(summary["Scenario"], summary["Final Cash ($M)"],
                    color=colors, alpha=0.85, edgecolor="white", linewidth=1.5)
    ax1.set_title("Final Cash on Hand ($M)", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Cash ($M)")
    ax1.set_xticklabels(summary["Scenario"], rotation=15, ha="right")
    for bar, val in zip(bars1, summary["Final Cash ($M)"]):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                 f"${val:.0f}M", ha="center", va="bottom", fontweight="bold", fontsize=9)

    # Min LCR
    bars2 = ax2.bar(summary["Scenario"], summary["Min LCR (%)"],
                    color=colors, alpha=0.85, edgecolor="white", linewidth=1.5)
    ax2.axhline(y=100, color="red", linestyle="--", linewidth=2,
                label="Minimum Required (100%)")
    ax2.set_title("Minimum LCR Reached (%)", fontsize=12, fontweight="bold")
    ax2.set_ylabel("LCR (%)")
    ax2.set_xticklabels(summary["Scenario"], rotation=15, ha="right")
    ax2.legend()
    for bar, val in zip(bars2, summary["Min LCR (%)"]):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f"{val:.0f}%", ha="center", va="bottom", fontweight="bold", fontsize=9)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"  📊 Chart saved: {save_path}")


def plot_heat_map(all_scenarios, save_path="plots/heatmap_lcr.png"):
    """
    Heatmap of LCR values across all scenarios over time.
    Red = dangerous, Green = safe.
    Gives a quick visual overview of when each scenario gets critical.
    """
    # Build a matrix: rows = scenarios, columns = days
    lcr_matrix = {}
    for df in all_scenarios:
        name = df["Scenario"].iloc[0]
        lcr_matrix[name] = df["LCR (%)"].clip(upper=300).values

    lcr_df = pd.DataFrame(lcr_matrix).T
    lcr_df.columns = [f"Day {i+1}" for i in range(lcr_df.shape[1])]

    # Only show every 5th day to keep chart readable
    cols_to_show = [c for i, c in enumerate(lcr_df.columns) if (i+1) % 5 == 0]
    lcr_subset = lcr_df[cols_to_show]

    fig, ax = plt.subplots(figsize=(14, 4))
    sns.heatmap(lcr_subset, annot=True, fmt=".0f", cmap="RdYlGn",
                center=100, vmin=0, vmax=300, ax=ax,
                linewidths=0.5, cbar_kws={"label": "LCR (%)"})
    ax.set_title("🌡️ LCR Heatmap — Green = Safe, Red = Danger Zone",
                 fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Day", fontsize=11)
    ax.set_ylabel("Scenario", fontsize=11)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"  📊 Chart saved: {save_path}")


# ─────────────────────────────────────────────────────────
# SECTION 5 — SAVE DATA
# ─────────────────────────────────────────────────────────

def save_simulation_data(all_scenarios, path="data/simulation_results.csv"):
    """
    Combines all scenario results and saves as a CSV file.
    Useful for further analysis in Excel or other tools!
    """
    combined = pd.concat(all_scenarios, ignore_index=True)
    combined.to_csv(path, index=False)
    print(f"\n  💾 Data saved to: {path}")
    print(f"     Shape: {combined.shape[0]} rows × {combined.shape[1]} columns")
    return combined


# ─────────────────────────────────────────────────────────
# SECTION 6 — MAIN RUNNER (Start the Game!)
# ─────────────────────────────────────────────────────────

def run_all_scenarios(
    withdrawal_rate=0.10,
    volatility=0.05,
    collateral_req_increase=0.20,
    discount_rate=0.30,
    forced_selling_pct=0.05,
    funding_reduction_rate=0.08,
    days=30
):
    """
    🎮 MAIN GAME FUNCTION — Run all stress scenarios!

    This is the 'Play Game' button. It runs all 4 scenarios and
    generates all visualizations. You can change the parameters
    to make scenarios harder or easier.

    Parameters (Difficulty Sliders 🎚️):
        withdrawal_rate          : Bank Run severity (higher = worse)
        volatility               : Market turbulence (higher = worse)
        collateral_req_increase  : Margin call severity (higher = worse)
        discount_rate            : Fire sale discount (higher = worse)
        forced_selling_pct       : How much is sold daily in fire sale
        funding_reduction_rate   : How fast funding dries up
        days                     : Length of the simulation

    Returns:
        List of DataFrames (one per scenario)
    """
    print("\n" + "=" * 55)
    print("  🎮  LIQUIDITY RISK SIMULATION STARTING...")
    print("=" * 55)

    # Setup the bank
    my_bank = setup_bank()

    # Run all 4 scenarios
    df_bank_run = scenario_bank_run(my_bank, withdrawal_rate, days)
    df_margin   = scenario_margin_call(my_bank, volatility, collateral_req_increase, days)
    df_fire     = scenario_fire_sale(my_bank, discount_rate, forced_selling_pct, days)
    df_funding  = scenario_funding_crisis(my_bank, funding_reduction_rate, days)

    all_scenarios = [df_bank_run, df_margin, df_fire, df_funding]

    # Generate all plots
    print("\n" + "=" * 55)
    print("  📊  GENERATING VISUALIZATIONS...")
    print("=" * 55)

    plot_cash_levels(all_scenarios)
    plot_lcr_over_time(all_scenarios)
    plot_scenario_comparison(all_scenarios)
    plot_cash_flow_projection(my_bank, days)
    plot_stress_test_summary(all_scenarios)
    plot_heat_map(all_scenarios)

    # Save data
    combined_df = save_simulation_data(all_scenarios)

    # Print final summary table
    print("\n" + "=" * 55)
    print("  📋  FINAL SUMMARY TABLE")
    print("=" * 55)
    for df in all_scenarios:
        name = df["Scenario"].iloc[0]
        final_cash = df["Cash ($M)"].iloc[-1]
        min_lcr = df["LCR (%)"].min()
        status = "✅ SAFE" if min_lcr >= 100 else "❌ FAILED LCR"
        print(f"  {name:<18} | Final Cash: ${final_cash:>6.1f}M | Min LCR: {min_lcr:>6.1f}% | {status}")
    print("=" * 55)

    return all_scenarios, combined_df


# ─────────────────────────────────────────────────────────
# RUN IF EXECUTED DIRECTLY
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    # 🎮 DEFAULT GAME — Run with standard difficulty
    scenarios, data = run_all_scenarios()

    # 🎮 TRY HARD MODE — Uncomment to test with more severe parameters!
    # scenarios, data = run_all_scenarios(
    #     withdrawal_rate=0.20,       # 20% daily withdrawals (very severe bank run)
    #     volatility=0.10,            # High market volatility
    #     collateral_req_increase=0.40,
    #     discount_rate=0.50,         # 50% fire sale discount
    #     forced_selling_pct=0.10,
    #     funding_reduction_rate=0.15
    # )
