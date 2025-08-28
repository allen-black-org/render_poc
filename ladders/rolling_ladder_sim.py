import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Parameters
initial_investment = 10000
num_rungs = 5
allocation = initial_investment / num_rungs
rung_maturities = [3, 6, 9, 12, 24]  # months
yields = {3: 0.043, 6: 0.041, 9: 0.039, 12: 0.038, 24: 0.0374}

# Simulation parameters
years_to_simulate = 10
start_date = datetime.today()

# Function for cash flow
def maturity_cash_flow(principal, annual_rate, months):
    return principal * (1 + annual_rate * (months/12))

# Rolling ladder simulation
events = []
portfolio = []

# Initialize ladder
for m in rung_maturities:
    maturity_date = start_date + timedelta(days=30*m)
    cash_flow = maturity_cash_flow(allocation, yields[m], m)
    portfolio.append((maturity_date, m, allocation, cash_flow))

# Simulate over time
end_date = start_date + timedelta(days=365*years_to_simulate)
current_date = start_date

while current_date <= end_date:
    matured = [p for p in portfolio if p[0] <= current_date]
    for p in matured:
        _, m, principal, cash_flow = p
        # Record event
        events.append({
            "Date": current_date.date(),
            "Matured Rung (Months)": m,
            "Principal": principal,
            "Maturity Value": round(cash_flow, 2)
        })
        # Reinvest into longest maturity (24 months)
        new_maturity_date = current_date + timedelta(days=30*24)
        new_cash_flow = maturity_cash_flow(principal, yields[24], 24)
        portfolio.append((new_maturity_date, 24, principal, new_cash_flow))
        portfolio.remove(p)
    # Advance one month
    current_date += timedelta(days=30)

ladder_rolling_df = pd.DataFrame(events)


# Aggregate portfolio size over time from rolling ladder simulation
portfolio_growth = ladder_rolling_df.groupby("Date")["Maturity Value"].sum().cumsum().reset_index()
portfolio_growth.columns = ["Date", "Cumulative Value"]

# Plot
plt.figure(figsize=(10,6))
plt.plot(portfolio_growth["Date"], portfolio_growth["Cumulative Value"], marker="o")
plt.title("Rolling Treasury Ladder Portfolio Growth (10 Years)")
plt.xlabel("Date")
plt.ylabel("Cumulative Portfolio Value ($)")
plt.grid(True)
plt.tight_layout()
plt.show()