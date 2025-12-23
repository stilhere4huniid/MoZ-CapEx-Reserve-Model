# 📐 Methodology & Mathematical Framework

## 1. Monte Carlo Simulation Engine
Instead of assuming fixed lifespans for assets, this model runs **5,000 to 10,000 discrete simulations**. Each iteration "rolls the dice" on every major component to generate a probability distribution of costs.

## 2. Weibull Distribution for Failure Rates
We use the Weibull distribution (`scipy.stats.weibull_min`) to model component reliability. This allows us to simulate:
* **Infant Mortality:** Early failures due to installation defects.
* **Wear-out Phase:** The increasing likelihood of failure as an asset ages.

## 3. Dual-Currency Inflation Logic
The model acknowledges the unique economic environment of Zimbabwe by applying different scalars to costs:
* **Imported Tech (USD):** Subject to global supply chain inflation and local import premiums (Baseline: 14.2%).
* **Local Labor (ZWG):** Subject to local wage stabilization targets (Baseline: 10.0%).