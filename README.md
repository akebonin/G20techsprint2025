# Credit Asset Demo – G20 TechSprint 2025

This project demonstrates a novel solution to **Problem Statement 2: Consumer-consented and secure credit data portability**, tailored for underbanked smallholder enterprises operating in informal or grey economies.

## 🔍 Concept

Traditional credit systems fail in environments where financial data is incomplete, informal, or inaccessible. This solution bypasses enterprise-level credit scoring by tying **loan eligibility to individual asset performance** — like a cassava farm — using real-time data and decentralized identity.

## 🎯 Use Case

> A farmer in sub-Saharan Africa may have mixed business activities — some formal (e.g. cassava sales), some informal (e.g. egg sales at local markets). Rather than assessing their entire enterprise, this demo evaluates **a specific productive asset** using sensor data and AI models.

## 🧱 Architecture

![System Architecture](A_system_architecture_diagram_of_a_credit_scoring,.png)

- **Frontend**: A lightweight web dashboard where users connect a MetaMask wallet, consent to share data, and view AI-predicted yields
- **Backend**: Python Flask app serving sensor data, yield predictions (via a Random Forest model), and a federated comparison table
- **Model**: A dummy-trained ML model using soil and temperature to predict cassava yield
- **Smart Contract**: Ethereum-compatible contract that conditionally releases funds if yield exceeds threshold
- **Federated Dataset**: Simulated regional farm data for comparison, stored locally to demonstrate peer analysis
- **User Flow Control**: Tabs and buttons become active only in correct sequence (wallet > consent > yield > review > release)

## 💡 Features

- 🔐 **Self-sovereign wallet connection** (MetaMask)
- 📊 **Sensor-driven yield forecasting**
- 📈 **Federated peer comparison** (lender view)
- 🤝 **Consent-first loan process**
- ⚖️ **Smart contract disbursement logic**
- 🪙 **CBDC/stablecoin-ready contract structure**
- 📶 **Real-time asset monitoring logic (expandable)**

## 🏗️ Stack

- **Frontend**: HTML5, JavaScript, Chart.js, Web3.js
- **Backend**: Python, Flask, Pandas, Scikit-learn
- **Smart Contract**: Solidity (JSON ABI integrated in frontend)
- **Blockchain**: MetaMask testnet integration
- **AI**: Random Forest regression model (`random_forest_model.joblib`)

## 🚀 How to Run

1. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Flask backend**  
   ```bash
   python flask_app.py
   ```

3. **Open `index.html` in browser**

4. **Ensure MetaMask is connected to testnet**

5. **Optional**: Deploy the smart contract separately to your testnet and update the contract address in the frontend if needed.

## 📁 Data Files

- `cassava_farm_data.csv`: Source for borrower predictions
- `federated_farm_data.csv`: Simulated data for lender comparison
- `random_forest_model.joblib`: AI model for predicting yields

## 📌 Notes

- Credit score is computed **on the frontend** using the average predicted yield:
  ```js
  score = Math.min(Math.round(avgYield / 20), 100)
  ```
- FARM10 is synchronized across both borrower and federated datasets to ensure alignment.

## 📬 Contact

> Built by **Alis Grave Nil**  
> For inquiries: `alizgravenil@gmail.com` 

---

© 2025 – G20 TechSprint Demo – All rights reserved.
