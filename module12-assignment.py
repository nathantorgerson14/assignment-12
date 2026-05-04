
# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

import matplotlib
matplotlib.use("Agg")

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Set seed for reproducibility
np.random.seed(42)

# Store information
stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

# Create store dataframe
store_df = pd.DataFrame(store_data)

# Product categories and departments
departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

# Generate sales data for each store
sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

# Base performance factors for each store (relative scale)
store_performance = {
    "Tampa": 1.0,
    "Orlando": 0.85,
    "Miami": 1.2,
    "Jacksonville": 0.75,
    "Gainesville": 0.65
}

# Base performance factors for each department (relative scale)
dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

# Generate daily sales data for each store, department, and category
for date in dates:
    # Seasonal factor (higher in summer and December)
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:  # Summer
        seasonal_factor = 1.15
    elif month == 12:  # December
        seasonal_factor = 1.25
    elif month in [1, 2]:  # Winter
        seasonal_factor = 0.9

    # Day of week factor (weekends are busier)
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0  # Weekend vs weekday

    for store in stores:
        store_factor = store_performance[store]

        for dept in departments:
            dept_factor = dept_performance[dept]

            for category in categories[dept]:
                # Base sales amount
                base_sales = np.random.normal(loc=500, scale=100)

                # Calculate final sales with all factors and some randomness
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount = sales_amount * np.random.normal(loc=1.0, scale=0.1)  # Add noise

                # Calculate profit margin (different base margins for departments)
                base_margin = {
                    "Produce": 0.25,
                    "Dairy": 0.22,
                    "Bakery": 0.35,
                    "Grocery": 0.20,
                    "Prepared Foods": 0.40
                }[dept]
                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)  # Keep within reasonable range

                # Calculate profit
                profit = sales_amount * profit_margin

                # Add record
                sales_data.append({
                    "Date": date,
                    "Store": store,
                    "Department": dept,
                    "Category": category,
                    "Sales": round(sales_amount, 2),
                    "ProfitMargin": round(profit_margin, 4),
                    "Profit": round(profit, 2)
                })

# Create sales dataframe
sales_df = pd.DataFrame(sales_data)

# Generate customer data
customer_data = []
total_customers = 5000

# Age distribution parameters
age_mean, age_std = 42, 15

# Income distribution parameters (in $1000s)
income_mean, income_std = 85, 30

# Create customer segments (will indirectly influence spending)
segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]

# Store preference probabilities (matches store performance somewhat)
store_probs = {
    "Tampa": 0.25,
    "Orlando": 0.20,
    "Miami": 0.30,
    "Jacksonville": 0.15,
    "Gainesville": 0.10
}

for i in range(total_customers):
    # Basic demographics
    age = int(np.random.normal(loc=age_mean, scale=age_std))
    age = max(min(age, 85), 18)  # Keep age in reasonable range

    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])

    income = int(np.random.normal(loc=income_mean, scale=income_std))
    income = max(income, 20)  # Minimum income

    # Customer segment
    segment = np.random.choice(segments, p=segment_probabilities)

    # Preferred store
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))

    # Shopping behavior - influenced by segment
    if segment == "Health Enthusiast":
        visit_frequency = np.random.randint(8, 15)  # Visits per month
        avg_basket = np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency = np.random.randint(4, 10)
        avg_basket = np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency = np.random.randint(5, 12)
        avg_basket = np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency = np.random.randint(6, 10)
        avg_basket = np.random.normal(loc=60, scale=10)
    else:  # Occasional Visitor
        visit_frequency = np.random.randint(1, 5)
        avg_basket = np.random.normal(loc=45, scale=15)

    # Ensure values are reasonable
    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)

    # Loyalty tier based on combination of frequency and spending
    monthly_spend = visit_frequency * avg_basket
    if monthly_spend > 1000:
        loyalty_tier = "Platinum"
    elif monthly_spend > 500:
        loyalty_tier = "Gold"
    elif monthly_spend > 200:
        loyalty_tier = "Silver"
    else:
        loyalty_tier = "Bronze"

    # Add to customer data
    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Age": age,
        "Gender": gender,
        "Income": income * 1000,  # Convert to actual income
        "Segment": segment,
        "PreferredStore": preferred_store,
        "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2),
        "MonthlySpend": round(visit_frequency * avg_basket, 2),
        "LoyaltyTier": loyalty_tier
    })

# Create customer dataframe
customer_df = pd.DataFrame(customer_data)

# Create some calculated operational metrics for stores
operational_data = []

for store in stores:
    # Get store details
    store_row = store_df[store_df["Store"] == store].iloc[0]
    square_footage = store_row["SquareFootage"]
    staff_count = store_row["StaffCount"]

    # Calculate store metrics
    store_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    store_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()

    # Calculate derived metrics
    sales_per_sqft = store_sales / square_footage
    profit_per_sqft = store_profit / square_footage
    sales_per_staff = store_sales / staff_count
    inventory_turnover = np.random.uniform(12, 18) * store_performance[store]
    customer_satisfaction = min(5, np.random.normal(loc=4.0, scale=0.3) *
                                (store_performance[store] ** 0.5))

    # Add to operational data
    operational_data.append({
        "Store": store,
        "AnnualSales": round(store_sales, 2),
        "AnnualProfit": round(store_profit, 2),
        "SalesPerSqFt": round(sales_per_sqft, 2),
        "ProfitPerSqFt": round(profit_per_sqft, 2),
        "SalesPerStaff": round(sales_per_staff, 2),
        "InventoryTurnover": round(inventory_turnover, 2),
        "CustomerSatisfaction": round(customer_satisfaction, 2)
    })

# Create operational dataframe
operational_df = pd.DataFrame(operational_data)

# Print data info
print("\nDataframes created successfully. Ready for analysis!")
print(f"Sales data shape: {sales_df.shape}")
print(f"Customer data shape: {customer_df.shape}")
print(f"Store data shape: {store_df.shape}")
print(f"Operational data shape: {operational_df.shape}")

# Print sample of each dataframe
print("\nSales Data Sample:")
print(sales_df.head(3))
print("\nCustomer Data Sample:")
print(customer_df.head(3))
print("\nStore Data Sample:")
print(store_df)
print("\nOperational Data Sample:")
print(operational_df)
# ----- END OF DATA CREATION -----


def _month_labels():
    return ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _day_labels():
    return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# TODO 1: Descriptive Analytics - Overview of Current Performance
# 1.1 Calculate and display basic descriptive statistics for sales and profit
# REQUIRED: Store results in variables for testing
def analyze_sales_performance():
    """
    Analyze overall sales performance with descriptive statistics
    REQUIRED: Create and return dictionary with keys:
    - 'total_sales': float
    - 'total_profit': float
    - 'avg_profit_margin': float
    - 'sales_by_store': pandas Series
    - 'sales_by_dept': pandas Series
    """
    total_sales = float(sales_df["Sales"].sum())
    total_profit = float(sales_df["Profit"].sum())
    avg_profit_margin = float(sales_df["ProfitMargin"].mean())
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)

    print(f"Total Sales: ${total_sales:,.2f}")
    print(f"Total Profit: ${total_profit:,.2f}")
    print(f"Average Profit Margin: {avg_profit_margin:.2%}")
    print("Top Store by Sales:", sales_by_store.idxmax())
    print("Top Department by Sales:", sales_by_dept.idxmax())

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "avg_profit_margin": avg_profit_margin,
        "sales_by_store": sales_by_store,
        "sales_by_dept": sales_by_dept
    }


# 1.2 Create visualizations showing sales distribution by store, department, and time
# REQUIRED: Return matplotlib figures
def visualize_sales_distribution():
    """
    Create visualizations showing how sales are distributed
    REQUIRED: Return tuple of three figures (store_fig, dept_fig, time_fig)
    """
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)
    monthly_sales = sales_df.groupby(sales_df["Date"].dt.month)["Sales"].sum().reindex(range(1, 13))

    store_fig = plt.figure(figsize=(8, 5))
    plt.bar(sales_by_store.index, sales_by_store.values)
    plt.title("Annual Sales by Store")
    plt.xlabel("Store")
    plt.ylabel("Sales ($)")
    plt.xticks(rotation=20)
    plt.tight_layout()

    dept_fig = plt.figure(figsize=(8, 6))
    plt.pie(sales_by_dept.values, labels=sales_by_dept.index, autopct="%1.1f%%", startangle=90)
    plt.title("Sales Share by Department")
    plt.tight_layout()

    time_fig = plt.figure(figsize=(9, 5))
    plt.plot(_month_labels(), monthly_sales.values, marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales ($)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    return store_fig, dept_fig, time_fig


# 1.3 Analyze customer segments and their spending patterns
# REQUIRED: Return analysis results
def analyze_customer_segments():
    """
    Analyze customer segments and their relationship to spending
    REQUIRED: Return dictionary with keys:
    - 'segment_counts': pandas Series
    - 'segment_avg_spend': pandas Series
    - 'segment_loyalty': pandas DataFrame
    """
    segment_counts = customer_df["Segment"].value_counts()
    segment_avg_spend = customer_df.groupby("Segment")["MonthlySpend"].mean().sort_values(ascending=False)
    segment_loyalty = pd.crosstab(customer_df["Segment"], customer_df["LoyaltyTier"])

    print("\nCustomer Segment Counts:")
    print(segment_counts)
    print("\nAverage Monthly Spend by Segment:")
    print(segment_avg_spend.round(2))

    return {
        "segment_counts": segment_counts,
        "segment_avg_spend": segment_avg_spend,
        "segment_loyalty": segment_loyalty
    }


# TODO 2: Diagnostic Analytics - Understanding Relationships
# 2.1 Identify factors correlated with sales performance
# REQUIRED: Return correlation results
def analyze_sales_correlations():
    """
    Analyze correlations between various factors and sales performance
    REQUIRED: Return dictionary with keys:
    - 'store_correlations': pandas DataFrame
    - 'top_correlations': list of tuples (factor, correlation)
    - 'correlation_fig': matplotlib figure
    """
    store_metrics = store_df.merge(operational_df, on="Store")
    numeric_cols = [
        "SquareFootage", "StaffCount", "YearsOpen", "WeeklyMarketingSpend",
        "AnnualSales", "AnnualProfit", "SalesPerSqFt", "ProfitPerSqFt",
        "SalesPerStaff", "InventoryTurnover", "CustomerSatisfaction"
    ]
    store_correlations = store_metrics[numeric_cols].corr()

    sales_corr = store_correlations["AnnualSales"].drop("AnnualSales").sort_values(key=np.abs, ascending=False)
    top_correlations = [(factor, float(corr)) for factor, corr in sales_corr.head(5).items()]

    correlation_fig = plt.figure(figsize=(9, 5))
    plt.bar(sales_corr.index, sales_corr.values)
    plt.title("Correlation with Annual Sales")
    plt.xlabel("Factor")
    plt.ylabel("Correlation")
    plt.xticks(rotation=45, ha="right")
    plt.axhline(0, linewidth=1)
    plt.tight_layout()

    print("\nTop Factors Correlated with Annual Sales:")
    for factor, corr in top_correlations:
        print(f"{factor}: {corr:.3f}")

    return {
        "store_correlations": store_correlations,
        "top_correlations": top_correlations,
        "correlation_fig": correlation_fig
    }


# 2.2 Compare stores based on operational metrics
# REQUIRED: Return comparison results
def compare_store_performance():
    """
    Compare stores across different operational metrics
    REQUIRED: Return dictionary with keys:
    - 'efficiency_metrics': pandas DataFrame (with SalesPerSqFt, SalesPerStaff)
    - 'performance_ranking': pandas Series (ranked by profit)
    - 'comparison_fig': matplotlib figure
    """
    efficiency_metrics = operational_df.set_index("Store")[["SalesPerSqFt", "SalesPerStaff"]].sort_values(
        by="SalesPerSqFt", ascending=False
    )
    performance_ranking = operational_df.set_index("Store")["AnnualProfit"].sort_values(ascending=False)

    normalized = operational_df.set_index("Store")[
        ["SalesPerSqFt", "ProfitPerSqFt", "CustomerSatisfaction"]
    ].copy()
    normalized = (normalized - normalized.min()) / (normalized.max() - normalized.min())

    comparison_fig = plt.figure(figsize=(9, 5))
    x = np.arange(len(normalized.index))
    width = 0.25
    plt.bar(x - width, normalized["SalesPerSqFt"], width=width, label="SalesPerSqFt")
    plt.bar(x, normalized["ProfitPerSqFt"], width=width, label="ProfitPerSqFt")
    plt.bar(x + width, normalized["CustomerSatisfaction"], width=width, label="CustomerSatisfaction")
    plt.xticks(x, normalized.index, rotation=20)
    plt.title("Normalized Store Performance Comparison")
    plt.xlabel("Store")
    plt.ylabel("Normalized Score")
    plt.legend()
    plt.tight_layout()

    print("\nStore Profit Ranking:")
    print(performance_ranking.round(2))

    return {
        "efficiency_metrics": efficiency_metrics,
        "performance_ranking": performance_ranking,
        "comparison_fig": comparison_fig
    }


# 2.3 Analyze seasonal patterns and their impact
# REQUIRED: Return seasonal analysis
def analyze_seasonal_patterns():
    """
    Identify and visualize seasonal patterns in sales data
    REQUIRED: Return dictionary with keys:
    - 'monthly_sales': pandas Series
    - 'dow_sales': pandas Series (day of week)
    - 'seasonal_fig': matplotlib figure
    """
    monthly_sales = sales_df.groupby(sales_df["Date"].dt.month)["Sales"].sum().reindex(range(1, 13))
    monthly_sales.index = _month_labels()

    dow_sales = sales_df.groupby(sales_df["Date"].dt.dayofweek)["Sales"].mean().reindex(range(7))
    dow_sales.index = _day_labels()

    seasonal_fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    axes[0].plot(monthly_sales.index, monthly_sales.values, marker="o")
    axes[0].set_title("Average Seasonality by Month")
    axes[0].set_xlabel("Month")
    axes[0].set_ylabel("Total Sales ($)")
    axes[0].grid(True, alpha=0.3)

    axes[1].bar(dow_sales.index, dow_sales.values)
    axes[1].set_title("Average Sales by Day of Week")
    axes[1].set_xlabel("Day")
    axes[1].set_ylabel("Average Daily Sales ($)")
    axes[1].tick_params(axis="x", rotation=20)

    seasonal_fig.tight_layout()

    print("\nHighest Sales Month:", monthly_sales.idxmax())
    print("Highest Sales Day:", dow_sales.idxmax())

    return {
        "monthly_sales": monthly_sales,
        "dow_sales": dow_sales,
        "seasonal_fig": seasonal_fig
    }


# TODO 3: Predictive Analytics - Basic Forecasting
# 3.1 Create a simple linear regression model to predict store sales
# REQUIRED: Return model results
def predict_store_sales():
    """
    Use linear regression to predict store sales based on store characteristics
    REQUIRED: Return dictionary with keys:
    - 'coefficients': dict (feature: coefficient)
    - 'r_squared': float
    - 'predictions': pandas Series
    - 'model_fig': matplotlib figure
    """
    model_df = store_df.merge(operational_df[["Store", "AnnualSales"]], on="Store")
    features = ["SquareFootage", "StaffCount", "WeeklyMarketingSpend"]
    X = model_df[features].astype(float).values
    y = model_df["AnnualSales"].astype(float).values

    X_design = np.column_stack([np.ones(len(X)), X])
    beta, _, _, _ = np.linalg.lstsq(X_design, y, rcond=None)
    y_pred = X_design @ beta

    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r_squared = float(1 - (ss_res / ss_tot)) if ss_tot != 0 else 1.0

    coefficients = {"Intercept": float(beta[0])}
    for i, feature in enumerate(features, start=1):
        coefficients[feature] = float(beta[i])

    predictions = pd.Series(y_pred, index=model_df["Store"], name="PredictedSales")

    model_fig = plt.figure(figsize=(7, 5))
    plt.scatter(y, y_pred)
    for actual, pred, label in zip(y, y_pred, model_df["Store"]):
        plt.annotate(label, (actual, pred), textcoords="offset points", xytext=(5, 5))
    line_min = min(y.min(), y_pred.min())
    line_max = max(y.max(), y_pred.max())
    plt.plot([line_min, line_max], [line_min, line_max], linestyle="--")
    plt.title("Actual vs Predicted Store Sales")
    plt.xlabel("Actual Annual Sales ($)")
    plt.ylabel("Predicted Annual Sales ($)")
    plt.tight_layout()

    print(f"\nStore Sales Model R-squared: {r_squared:.4f}")

    return {
        "coefficients": coefficients,
        "r_squared": r_squared,
        "predictions": predictions,
        "model_fig": model_fig
    }


# 3.2 Forecast departmental sales trends
# REQUIRED: Return forecast results
def forecast_department_sales():
    """
    Analyze and forecast departmental sales trends
    REQUIRED: Return dictionary with keys:
    - 'dept_trends': pandas DataFrame
    - 'growth_rates': pandas Series
    - 'forecast_fig': matplotlib figure
    """
    monthly_dept = sales_df.groupby([sales_df["Date"].dt.to_period("M"), "Department"])["Sales"].sum().unstack()
    monthly_dept.index = monthly_dept.index.to_timestamp()
    monthly_dept = monthly_dept.sort_index()

    growth_rates = ((monthly_dept.iloc[-1] - monthly_dept.iloc[0]) / monthly_dept.iloc[0]).sort_values(ascending=False)

    forecast_index = pd.date_range(monthly_dept.index[-1] + pd.offsets.MonthBegin(1), periods=3, freq="MS")
    forecast_values = {}

    x = np.arange(len(monthly_dept))
    for dept in monthly_dept.columns:
        y = monthly_dept[dept].values
        slope, intercept = np.polyfit(x, y, 1)
        future_x = np.arange(len(monthly_dept), len(monthly_dept) + 3)
        forecast_values[dept] = intercept + slope * future_x

    forecast_df = pd.DataFrame(forecast_values, index=forecast_index)
    dept_trends = pd.concat([monthly_dept, forecast_df])

    forecast_fig = plt.figure(figsize=(10, 6))
    for dept in monthly_dept.columns:
        plt.plot(monthly_dept.index, monthly_dept[dept], marker="o", label=f"{dept} Actual")
        plt.plot(forecast_df.index, forecast_df[dept], linestyle="--", marker="o", label=f"{dept} Forecast")
    plt.title("Department Sales Trends and 3-Month Forecast")
    plt.xlabel("Month")
    plt.ylabel("Sales ($)")
    plt.legend(ncol=2, fontsize=8)
    plt.tight_layout()

    print("\nDepartment Growth Rates:")
    print((growth_rates * 100).round(2).astype(str) + "%")

    return {
        "dept_trends": dept_trends,
        "growth_rates": growth_rates,
        "forecast_fig": forecast_fig
    }


# TODO 4: Integrated Analysis - Business Insights and Recommendations
# 4.1 Identify the most profitable combinations of store, department, and customer segments
# REQUIRED: Return opportunity analysis
def identify_profit_opportunities():
    """
    Identify the most profitable combinations and potential opportunities
    REQUIRED: Return dictionary with keys:
    - 'top_combinations': pandas DataFrame (top 10 store-dept combinations)
    - 'underperforming': pandas DataFrame (bottom 10)
    - 'opportunity_score': pandas Series (by store)
    """
    store_dept_profit = sales_df.groupby(["Store", "Department"]).agg(
        AnnualSales=("Sales", "sum"),
        AnnualProfit=("Profit", "sum"),
        AvgMargin=("ProfitMargin", "mean")
    ).reset_index()

    store_segment_spend = customer_df.groupby(["PreferredStore", "Segment"]).agg(
        SegmentMonthlySpend=("MonthlySpend", "sum"),
        AvgBasket=("AvgBasketSize", "mean")
    ).reset_index().rename(columns={"PreferredStore": "Store"})

    combo_df = store_dept_profit.merge(store_segment_spend, on="Store", how="left")
    combo_df["EstimatedOpportunity"] = (
        combo_df["AnnualProfit"] * (combo_df["SegmentMonthlySpend"] / combo_df["SegmentMonthlySpend"].max())
        * (combo_df["AvgMargin"] / combo_df["AvgMargin"].max())
    )

    top_combinations = combo_df.sort_values("EstimatedOpportunity", ascending=False).head(10).reset_index(drop=True)
    underperforming = combo_df.sort_values("EstimatedOpportunity", ascending=True).head(10).reset_index(drop=True)

    store_summary = operational_df.set_index("Store").copy()
    customer_store_spend = customer_df.groupby("PreferredStore")["MonthlySpend"].sum()
    customer_store_spend.name = "CustomerSpendPotential"
    store_summary = store_summary.join(customer_store_spend)
    store_summary["CustomerSpendPotential"] = store_summary["CustomerSpendPotential"].fillna(0)

    score_df = pd.DataFrame(index=store_summary.index)
    score_df["ProfitScore"] = store_summary["AnnualProfit"] / store_summary["AnnualProfit"].max()
    score_df["SatisfactionScore"] = store_summary["CustomerSatisfaction"] / store_summary["CustomerSatisfaction"].max()
    score_df["DemandScore"] = store_summary["CustomerSpendPotential"] / store_summary["CustomerSpendPotential"].max()
    score_df["EfficiencyGap"] = 1 - (store_summary["SalesPerSqFt"] / store_summary["SalesPerSqFt"].max())

    opportunity_score = (
        0.35 * score_df["DemandScore"] +
        0.25 * score_df["EfficiencyGap"] +
        0.20 * score_df["SatisfactionScore"] +
        0.20 * score_df["ProfitScore"]
    ).sort_values(ascending=False)

    print("\nTop Estimated Opportunities:")
    print(top_combinations[["Store", "Department", "Segment", "EstimatedOpportunity"]].head(5))

    return {
        "top_combinations": top_combinations,
        "underperforming": underperforming,
        "opportunity_score": opportunity_score
    }


# 4.2 Develop recommendations for improving performance
# REQUIRED: Return list of recommendations
def develop_recommendations():
    """
    Develop actionable recommendations based on the analysis
    REQUIRED: Return list of at least 5 recommendation strings
    """
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)
    profit_by_dept = sales_df.groupby("Department")["Profit"].sum().sort_values(ascending=False)
    monthly_sales = sales_df.groupby(sales_df["Date"].dt.month)["Sales"].sum()
    weekend_sales = sales_df[sales_df["Date"].dt.dayofweek >= 5]["Sales"].mean()
    weekday_sales = sales_df[sales_df["Date"].dt.dayofweek < 5]["Sales"].mean()
    low_efficiency_store = operational_df.sort_values("SalesPerSqFt").iloc[0]["Store"]
    best_efficiency_store = operational_df.sort_values("SalesPerSqFt", ascending=False).iloc[0]["Store"]
    high_opportunity_store = identify_profit_opportunities()["opportunity_score"].idxmax()
    top_segment = customer_df.groupby("Segment")["MonthlySpend"].mean().sort_values(ascending=False).idxmax()
    top_profit_dept = profit_by_dept.idxmax()
    low_sales_store = sales_by_store.idxmin()
    top_sales_store = sales_by_store.idxmax()

    recommendations = [
        f"Shift more inventory and marketing resources toward {top_profit_dept}, since it produces the highest total profit across the chain.",
        f"Prioritize a performance improvement plan for {low_efficiency_store}, which has the weakest sales per square foot and may benefit from layout, staffing, or assortment changes.",
        f"Use {best_efficiency_store} as the operational benchmark for space productivity, while using {top_sales_store} as the benchmark for total sales generation.",
        f"Target {top_segment} customers with loyalty promotions and personalized offers because they generate the highest average monthly spend.",
        f"Increase staffing, prepared inventory, and promotional activity on weekends because average weekend sales exceed weekday sales by a meaningful margin.",
        f"Plan larger seasonal campaigns for summer and December, when monthly sales peaks suggest stronger demand and better return on marketing spend.",
        f"Focus cross-selling and department bundles in {high_opportunity_store}, which shows the highest overall opportunity score when customer demand and store efficiency are combined."
    ]

    print("\nRecommendations:")
    for i, rec in enumerate(recommendations[:5], start=1):
        print(f"{i}. {rec}")

    return recommendations


# TODO 5: Summary Report
# REQUIRED: Generate comprehensive summary
def generate_executive_summary():
    """
    Generate an executive summary of key findings and recommendations
    REQUIRED: Print executive summary with sections:
    - Overview (1 paragraph)
    - Key Findings (3-5 bullet points)
    - Recommendations (3-5 bullet points)
    - Expected Impact (1 paragraph)
    """
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)
    avg_segment_spend = customer_df.groupby("Segment")["MonthlySpend"].mean().sort_values(ascending=False)
    monthly_sales = sales_df.groupby(sales_df["Date"].dt.month)["Sales"].sum()
    dow_sales = sales_df.groupby(sales_df["Date"].dt.dayofweek)["Sales"].mean()
    opportunity_score = identify_profit_opportunities()["opportunity_score"]
    recommendations = develop_recommendations()

    print("Overview")
    print(
        "GreenGrocer’s 2023 data shows a healthy business with clear differences in performance across stores, "
        "departments, customer segments, and time periods. The analysis points to strong concentration of revenue "
        "in Miami and Tampa, higher-margin contribution from Prepared Foods and Bakery, and clear seasonal demand "
        "lifts during summer, weekends, and December."
    )

    print("\nKey Findings")
    print(f"- {sales_by_store.idxmax()} generated the highest annual sales, while {sales_by_store.idxmin()} lagged the chain.")
    print(f"- {sales_by_dept.idxmax()} led all departments in sales, while {sales_df.groupby('Department')['Profit'].sum().idxmax()} led in total profit.")
    print(f"- {avg_segment_spend.idxmax()} customers had the highest average monthly spend.")
    strongest_month = _month_labels()[int(monthly_sales.idxmax()) - 1]
    print(f"- {strongest_month} was the strongest month for sales, and {_day_labels()[int(dow_sales.idxmax())]} had the highest average daily sales.")
    print(f"- {opportunity_score.idxmax()} has the highest blended opportunity score for future improvement focus.")

    print("\nRecommendations")
    for rec in recommendations[:5]:
        print(f"- {rec}")

    print("\nExpected Impact")
    print(
        "If management reallocates labor, inventory, and marketing toward the strongest departments, peak periods, "
        "and highest-value customer groups while lifting underperforming stores, GreenGrocer should improve both "
        "sales productivity and profit quality. The biggest gains are likely to come from better store-level "
        "execution, stronger seasonal planning, and more targeted loyalty marketing."
    )


# Main function to execute all analyses
# REQUIRED: Do not modify function name
def main():
    print("\n" + "=" * 60)
    print("GREENGROCER BUSINESS ANALYTICS RESULTS")
    print("=" * 60)

    # Execute analyses in a logical order
    # REQUIRED: Store all results for potential testing

    print("\n--- DESCRIPTIVE ANALYTICS: CURRENT PERFORMANCE ---")
    sales_metrics = analyze_sales_performance()
    dist_figs = visualize_sales_distribution()
    customer_analysis = analyze_customer_segments()

    print("\n--- DIAGNOSTIC ANALYTICS: UNDERSTANDING RELATIONSHIPS ---")
    correlations = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    seasonality = analyze_seasonal_patterns()

    print("\n--- PREDICTIVE ANALYTICS: FORECASTING ---")
    sales_model = predict_store_sales()
    dept_forecast = forecast_department_sales()

    print("\n--- BUSINESS INSIGHTS AND RECOMMENDATIONS ---")
    opportunities = identify_profit_opportunities()
    recommendations = develop_recommendations()

    print("\n--- EXECUTIVE SUMMARY ---")
    generate_executive_summary()

    # Save figures so the script runs cleanly in headless environments
    for i, fig_num in enumerate(plt.get_fignums(), start=1):
        plt.figure(fig_num)
        plt.savefig(f"greengrocer_figure_{i}.png", bbox_inches="tight")

    if matplotlib.get_backend().lower() != "agg":
        plt.show()

    # Return results for testing purposes
    return {
        'sales_metrics': sales_metrics,
        'customer_analysis': customer_analysis,
        'correlations': correlations,
        'store_comparison': store_comparison,
        'seasonality': seasonality,
        'sales_model': sales_model,
        'dept_forecast': dept_forecast,
        'opportunities': opportunities,
        'recommendations': recommendations
    }

# Run the main function
if __name__ == "__main__":
    results = main()
