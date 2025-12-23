# 📘 Project Documentation & User Guide

## 📂 File Overview

- **`app.py`**  
  Core application logic containing:
  - Monte Carlo simulation engine  
  - Streamlit dashboard UI  
  - PDF report generation class (`MoZReport`)

- **`Untitled.ipynb`**  
  Jupyter Notebook used for:
  - Initial data exploration  
  - Algorithm testing  
  - Statistical validation of Weibull distributions

- **`requirements.txt`**  
  List of all Python dependencies required to run the project.

---

## ⚙️ How to Use the Dashboard

### 1. Launching the App

Open a terminal in the project directory and run:

```bash
streamlit run app.py
```
This will open the dashboard in your default web browser (usually at http://localhost:8501).

---

### 2. The Economic Stress Test (Sidebar)
The sidebar controls allow you to stress-test the Mall's financial resilience against two key inflation metrics:

USD Import Inflation (%): Adjust this slider (2% - 20%) to simulate changes in global logistics costs and import duties for high-tech components like AI-HVAC and Solar systems.

**Baseline:** 14.2%

Local Labor Inflation (%): Adjust this slider (2% - 50%) to reflect changes in the local wage market for civil works and onsite maintenance.

**Baseline:** 10.0%

---

### 3. Simulation Precision
1,000 Iterations: Faster computation, useful for quick "what-if" scenarios.

10,000 Iterations: High precision, recommended for final Board Reporting. This minimizes statistical noise in the P95 Risk Case.

---

### 4. Running the Forecast
Set your desired inflation parameters.

Click the 🚀 Run button.

**The dashboard will display:**

**Avg. 20-Year Spend:** The mean expected cost of asset maintenance.

**P95 Risk Case:** The "worst-case" scenario (95th percentile).

Annual Reserve Needed: The recommended yearly contribution to the sinking fund.

Waterfall Chart: A visual timeline showing when major systems are likely to fail.

---

### 5. Generating the Executive Report
Once a simulation is complete, a button labeled 📑 Generate & Download PDF Report will appear. Clicking this will:

Capture the current Waterfall Chart from your screen.

Embed the chart into a formal PDF.

Dynamically write the "Strategic Interpretation" based on your specific simulation results.

Download the file as MoZ_Strategic_Report.pdf.

---

## 📦 Dependencies & Engines
This project relies on several key libraries:

**Streamlit:** For the interactive web interface.

**Plotly:** For generating the interactive financial waterfall charts.

**Kaleido:** An engine required to convert Plotly charts into static images for the PDF report.

**FPDF2:** For programmatically generating the PDF documents.

**Scipy:** For generating the Weibull probability distributions used in the Monte Carlo engine.