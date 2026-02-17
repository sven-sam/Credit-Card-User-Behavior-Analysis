import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import json  
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit.components.v1 import html
import os

credit_cards_db = {
     "travel": [
        {"Card": "American Express Platinum Travel Card", "Offers": "2X Membership Rewards Points on travel", "Eligibility": {"min_income": 1200000, "min_score": 700}},
        {"Card": "Citi Premier Card", "Offers": "3X points on travel; $100 annual hotel credit", "Eligibility": {"min_income": 800000, "min_score": 700}},
        {"Card": "Capital One Venture Rewards Credit Card", "Offers": "2X miles on every purchase; 50,000 bonus miles", "Eligibility": {"min_income": 600000, "min_score": 700}},
        {"Card": "Barclaycard Arrival Plus World Elite MasterCard", "Offers": "2X miles on all purchases; 70,000 bonus miles", "Eligibility": {"min_income": 1200000, "min_score": 700}},
        {"Card": "The Platinum Card® from American Express", "Offers": "5X points on flights; $200 annual airline fee credit", "Eligibility": {"min_income": 2500000, "min_score": 750}},
        {"Card": "Delta SkyMiles® Gold American Express Card", "Offers": "2X miles on Delta purchases, restaurants, and U.S. supermarkets", "Eligibility": {"min_income": 600000, "min_score": 700}},
        {"Card": "United Explorer Card", "Offers": "2X miles on United purchases, dining, and hotels", "Eligibility": {"min_income": 500000, "min_score": 700}}
    ],
    "shopping": [
        {"Card": "Amazon Prime Rewards Visa Signature Card", "Offers": "5% back on Amazon.com and Whole Foods", "Eligibility": {"min_income": 0, "min_score": 650}},
        {"Card": "Wells Fargo Active Cash® Card", "Offers": "2% cash back on purchases; $200 cash rewards", "Eligibility": {"min_income": 500000, "min_score": 700}},
        {"Card": "Chase Freedom Flex", "Offers": "5% cash back on rotating categories; 1% on all other purchases", "Eligibility": {"min_income": 500000, "min_score": 700}},
        {"Card": "Target RedCard", "Offers": "5% off at Target; Free shipping on most Target orders", "Eligibility": {"min_income": 0, "min_score": 700}},
        {"Card": "Best Buy® Credit Card", "Offers": "5% back on purchases; 0% financing for 24 months on purchases over $499", "Eligibility": {"min_income": 500000, "min_score": 600}},
        {"Card": "Sam's Club® Mastercard®", "Offers": "5% cash back on gas; 3% on dining and travel", "Eligibility": {"min_income": 0, "min_score": 700}},
        {"Card": "Costco Anywhere Visa® Card by Citi", "Offers": "4% back on gas; 3% on restaurants and travel", "Eligibility": {"min_income": 0, "min_score": 700}},
        {"Card": "The Blue Cash Everyday® Card from American Express", "Offers": "3% cash back on U.S. supermarkets; 1% on other purchases", "Eligibility": {"min_income": 500000, "min_score": 700}}
    ],
    "premium": [
        {"Card": "Chase Sapphire Reserve®", "Offers": "3X points on travel and dining; $300 annual travel credit", "Eligibility": {"min_income": 2000000, "min_score": 750}},
        {"Card": "American Express® Gold Card", "Offers": "4X points on dining; 3X points on flights", "Eligibility": {"min_income": 1200000, "min_score": 750}},
        {"Card": "Citi Prestige® Card", "Offers": "5X points on air travel; $250 annual travel credit", "Eligibility": {"min_income": 2500000, "min_score": 750}},
        {"Card": "The Business Platinum® Card from American Express", "Offers": "5X points on flights; 1.5X points on eligible purchases", "Eligibility": {"min_income": 3000000, "min_score": 750}},
        {"Card": "The Ritz-Carlton Rewards Credit Card", "Offers": "5X points on hotels; 2X points on airfare", "Eligibility": {"min_income": 2500000, "min_score": 750}}
    ],
    "basic": [
        {"Card": "Capital One QuicksilverOne Cash Rewards Credit Card", "Offers": "1.5% cash back on purchases", "Eligibility": {"min_score": 600, "annual_fee": 5000}},
        {"Card": "Discover it® Student Cash Back", "Offers": "5% cashback on rotating categories; 1% on other purchases", "Eligibility": "Student with a good credit history"},
        {"Card": "Indigo® Platinum Mastercard®", "Offers": "Pre-qualification without impacting your credit score", "Eligibility": {"min_score": 550, "annual_fee": 0}},
        {"Card": "Milestone® Gold Mastercard®", "Offers": "Regular reporting to all 3 major credit bureaus", "Eligibility": {"min_score": 550, "annual_fee": 35}},
        {"Card": "OpenSky® Secured Visa® Credit Card", "Offers": "No credit check to apply", "Eligibility": "Secured card; Bad credit or no credit history"},
        {"Card": "Total Visa® Card", "Offers": "Credit limit of 24,000 to 80,000; No hidden fees", "Eligibility": {"min_score": 500, "annual_fee": 75}}
    ],
    "dining & food": [
        {"Card": "HDFC Bank Millennia Credit Card", "Offers": "5% cashback on dining, groceries & utilities", "Eligibility": {"min_income": 600000, "min_score": 700}},
        {"Card": "SBI Card Elite", "Offers": "10X points on dining and movies", "Eligibility": {"min_income": 700000, "min_score": 700}},
        {"Card": "ICICI Bank Coral Credit Card", "Offers": "2 Payback points per ₹100 spent on dining", "Eligibility": {"min_income": 450000, "min_score": 700}},
        {"Card": "Axis Bank Flipkart Credit Card", "Offers": "5% cashback on dining and 4% on Flipkart purchases", "Eligibility": {"min_income": 500000, "min_score": 700}}
    ],
    "fuel": [
        {"Card": "IndianOil Citi Platinum Credit Card", "Offers": "4X reward points on fuel; 1 reward point = ₹1", "Eligibility": {"min_income": 400000, "min_score": 700}},
        {"Card": "HDFC Bank Bharat Petroleum Credit Card", "Offers": "5% cashback on fuel and 1% on all other spends", "Eligibility": {"min_income": 500000, "min_score": 700}},
        {"Card": "BPCL SBI Card", "Offers": "4.25% cashback on fuel purchases", "Eligibility": {"min_income": 450000, "min_score": 700}}
    ],
     "education": [
        {"Card": "ICICI Bank Student Travel Card", "Offers": "Cashback on education-related travel expenses, books, and supplies", "Eligibility": {"min_income": 300000, "min_score": 650}},
        {"Card": "Axis Bank Education Advantage Credit Card", "Offers": "Discounts on educational services, tuition fee payments, and books", "Eligibility": {"min_income": 300000, "min_score": 600}},
        {"Card": "SBI Student Card", "Offers": "Discounts and cashback on school/college fees, books, and stationery", "Eligibility": {"min_income": 300000, "min_score": 700}},
        {"Card": "Bajaj Finserv RBL Bank Credit Card (Education Loan Repayment)", "Offers": "Benefits on education loan repayment along with cashback on book purchases", "Eligibility": {"min_income": 600000, "min_score": 700}}
    ],
    "fitness_and_medical": [
        {"Card": "ICICI Bank Health and Wellness Credit Card", "Offers": "5% cashback on medical expenses, gym memberships, and healthcare services", "Eligibility": {"min_income": 600000, "min_score": 700}},
        {"Card": "SBI Card Wellness", "Offers": "5% cashback on gym memberships, fitness-related services, and health insurance premiums", "Eligibility": {"min_income": 500000, "min_score": 700}},
        {"Card": "HDFC Bank Health Credit Card", "Offers": "10% cashback on hospital bills, medical insurance, and pharmacy purchases", "Eligibility": {"min_income": 400000, "min_score": 700}},
        {"Card": "Religare Health Insurance Credit Card", "Offers": "Cashback on premium payments and health check-up services", "Eligibility": {"min_income": 500000, "min_score": 700}},
        {"Card": "Axis Bank Arogya Card", "Offers": "Discounted rates for medical treatments and regular health check-ups", "Eligibility": {"min_income": 400000, "min_score": 700}},
        {"Card": "Bajaj Finserv Health EMI Network Card", "Offers": "Instant EMIs for medical expenses; Discounts at partner hospitals and clinics", "Eligibility": {"min_income": 400000, "min_score": 700}}
    ],
    "online_shopping": [
        {"Card": "Amazon Pay ICICI Bank Credit Card", "Offers": "5% cashback on Amazon purchases", "Eligibility": {"min_income": 300000, "min_score": 700}},
        {"Card": "Flipkart Axis Bank Credit Card", "Offers": "5% cashback on Flipkart, Myntra, and other partner brands", "Eligibility": {"min_income": 350000, "min_score": 700}},
        {"Card": "HDFC Bank Regalia Credit Card", "Offers": "Cashback & rewards on online purchases, priority access to sales", "Eligibility": {"min_income": 500000, "min_score": 700}},
        {"Card": "Standard Chartered Manhattan Platinum Credit Card", "Offers": "5% cashback on dining, fuel, and online shopping", "Eligibility": {"min_income": 300000}},
        {"Card": "SBI SimplyCLICK Credit Card", "Offers": "10x reward points on online shopping with major partners like Amazon, Flipkart", "Eligibility": {"min_income": 300000, "min_score": 700}}
    ],
    "entertainment": [
        {"Card": "HDFC Bank Millennia Credit Card","Offers": "5% cashback on BookMyShow, Zomato, and Swiggy","Eligibility": {"min_income": 300000, "min_score": 700}},
        {"Card": "SBI Card ELITE","Offers": "Free BookMyShow tickets worth ₹6,000 per year, 5X reward points on dining & movies","Eligibility": {"min_income": 600000, "min_score": 750}},
        {"Card": "ICICI Bank Coral Credit Card","Offers": "25% discount on BookMyShow & INOX tickets, 2X rewards on entertainment spends","Eligibility": {"min_income": 250000, "min_score": 680}},
        {"Card": "Axis Bank Neo Credit Card","Offers": "10% off on BookMyShow, Zomato, and Paytm Movies","Eligibility": {"min_income": 240000, "min_score": 650}},
        {"Card": "Kotak PVR Platinum Credit Card","Offers": "Up to 2 free PVR movie tickets every month","Eligibility": {"min_income": 300000, "min_score": 700}},
        {"Card": "RBL Bank Popcorn Credit Card","Offers": "1+1 free movie ticket on BookMyShow, 10% cashback on food and beverages","Eligibility": {"min_income": 360000, "min_score": 700}},
        {"Card": "Citi Cashback Credit Card","Offers": "5% cashback on movie tickets, 10% cashback on dining","Eligibility": {"min_income": 500000, "min_score": 720}},
        {"Card": "IndusInd Legend Credit Card","Offers": "Buy 1 Get 1 on BookMyShow, 2X rewards on entertainment spends","Eligibility": {"min_income": 480000, "min_score": 710}}
    ]
}

loan_data = pd.DataFrame([
    {"Bank": "HDFC Bank", "Loan Type": "Personal Loan", "Min Credit Score": 700, "Min Income": 300000, "Max Loan Amount": 5000000, "Interest Rate": 10.5, "Collateral": "No"},
    {"Bank": "HDFC Bank", "Loan Type": "Home Loan", "Min Credit Score": 680, "Min Income": 500000, "Max Loan Amount": 30000000, "Interest Rate": 8.0, "Collateral": "Yes"},
    {"Bank": "HDFC Bank", "Loan Type": "Education Loan", "Min Credit Score": 700, "Min Income": 200000, "Max Loan Amount": 2000000, "Interest Rate": 9.5, "Collateral": "No"},

    {"Bank": "SBI Bank", "Loan Type": "Home Loan", "Min Credit Score": 650, "Min Income": 400000, "Max Loan Amount": 20000000, "Interest Rate": 8.2, "Collateral": "Yes"},
    {"Bank": "SBI Bank", "Loan Type": "Auto Loan", "Min Credit Score": 660, "Min Income": 300000, "Max Loan Amount": 1500000, "Interest Rate": 9.0, "Collateral": "No"},
    {"Bank": "SBI Bank", "Loan Type": "Business Loan", "Min Credit Score": 720, "Min Income": 600000, "Max Loan Amount": 10000000, "Interest Rate": 11.5, "Collateral": "Yes"},

    {"Bank": "ICICI Bank", "Loan Type": "Auto Loan", "Min Credit Score": 680, "Min Income": 250000, "Max Loan Amount": 3000000, "Interest Rate": 9.0, "Collateral": "No"},
    {"Bank": "ICICI Bank", "Loan Type": "Personal Loan", "Min Credit Score": 700, "Min Income": 350000, "Max Loan Amount": 4000000, "Interest Rate": 10.2, "Collateral": "No"},
    {"Bank": "ICICI Bank", "Loan Type": "Business Loan", "Min Credit Score": 730, "Min Income": 700000, "Max Loan Amount": 12000000, "Interest Rate": 12.8, "Collateral": "Yes"},

    {"Bank": "Axis Bank", "Loan Type": "Education Loan", "Min Credit Score": 690, "Min Income": 180000, "Max Loan Amount": 3000000, "Interest Rate": 9.3, "Collateral": "No"},
    {"Bank": "Axis Bank", "Loan Type": "Home Loan", "Min Credit Score": 670, "Min Income": 450000, "Max Loan Amount": 25000000, "Interest Rate": 8.5, "Collateral": "Yes"},
    {"Bank": "Axis Bank", "Loan Type": "Business Loan", "Min Credit Score": 720, "Min Income": 500000, "Max Loan Amount": 10000000, "Interest Rate": 12.0, "Collateral": "Yes"},

    {"Bank": "Kotak Bank", "Loan Type": "Education Loan", "Min Credit Score": 700, "Min Income": 200000, "Max Loan Amount": 4000000, "Interest Rate": 9.5, "Collateral": "No"},
    {"Bank": "Kotak Bank", "Loan Type": "Personal Loan", "Min Credit Score": 690, "Min Income": 320000, "Max Loan Amount": 3000000, "Interest Rate": 10.0, "Collateral": "No"},

    {"Bank": "IDFC First", "Loan Type": "Home Loan", "Min Credit Score": 670, "Min Income": 500000, "Max Loan Amount": 25000000, "Interest Rate": 8.0, "Collateral": "Yes"},
    {"Bank": "IDFC First", "Loan Type": "Auto Loan", "Min Credit Score": 660, "Min Income": 270000, "Max Loan Amount": 2000000, "Interest Rate": 9.2, "Collateral": "No"},

    {"Bank": "Yes Bank", "Loan Type": "Business Loan", "Min Credit Score": 740, "Min Income": 650000, "Max Loan Amount": 9000000, "Interest Rate": 12.3, "Collateral": "Yes"},
    {"Bank": "Yes Bank", "Loan Type": "Personal Loan", "Min Credit Score": 680, "Min Income": 350000, "Max Loan Amount": 3000000, "Interest Rate": 11.2, "Collateral": "No"},

    {"Bank": "Bank of Baroda", "Loan Type": "Home Loan", "Min Credit Score": 680, "Min Income": 420000, "Max Loan Amount": 20000000, "Interest Rate": 8.3, "Collateral": "Yes"},
    {"Bank": "Bank of Baroda", "Loan Type": "Education Loan", "Min Credit Score": 690, "Min Income": 180000, "Max Loan Amount": 2500000, "Interest Rate": 9.0, "Collateral": "No"},

    {"Bank": "PNB", "Loan Type": "Home Loan", "Min Credit Score": 670, "Min Income": 400000, "Max Loan Amount": 22000000, "Interest Rate": 8.4, "Collateral": "Yes"},
    {"Bank": "PNB", "Loan Type": "Personal Loan", "Min Credit Score": 700, "Min Income": 280000, "Max Loan Amount": 2500000, "Interest Rate": 10.7, "Collateral": "No"},

    {"Bank": "Canara Bank", "Loan Type": "Education Loan", "Min Credit Score": 680, "Min Income": 150000, "Max Loan Amount": 1500000, "Interest Rate": 8.8, "Collateral": "No"},
    {"Bank": "Canara Bank", "Loan Type": "Business Loan", "Min Credit Score": 710, "Min Income": 550000, "Max Loan Amount": 8000000, "Interest Rate": 11.6, "Collateral": "Yes"},

    {"Bank": "Federal Bank", "Loan Type": "Auto Loan", "Min Credit Score": 670, "Min Income": 260000, "Max Loan Amount": 2500000, "Interest Rate": 9.1, "Collateral": "No"},
    {"Bank": "Federal Bank", "Loan Type": "Home Loan", "Min Credit Score": 690, "Min Income": 450000, "Max Loan Amount": 21000000, "Interest Rate": 8.1, "Collateral": "Yes"},

    {"Bank": "IndusInd Bank", "Loan Type": "Business Loan", "Min Credit Score": 735, "Min Income": 750000, "Max Loan Amount": 11000000, "Interest Rate": 12.5, "Collateral": "Yes"},
    {"Bank": "IndusInd Bank", "Loan Type": "Personal Loan", "Min Credit Score": 705, "Min Income": 330000, "Max Loan Amount": 3500000, "Interest Rate": 10.9, "Collateral": "No"},

    {"Bank": "Union Bank", "Loan Type": "Education Loan", "Min Credit Score": 690, "Min Income": 170000, "Max Loan Amount": 1800000, "Interest Rate": 9.2, "Collateral": "No"},
    {"Bank": "Union Bank", "Loan Type": "Auto Loan", "Min Credit Score": 675, "Min Income": 290000, "Max Loan Amount": 2200000, "Interest Rate": 9.3, "Collateral": "No"}
])

# Load trained model & preprocessors
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "spending_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")
LABEL_ENCODERS_PATH = os.path.join(BASE_DIR, "label_encoders.pkl")

spending_model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
label_encoders = joblib.load(LABEL_ENCODERS_PATH)
st.set_page_config(page_title="Smart Finance Dashboard", layout="wide")
st.title("📊 Credit Card Spending Behavior Analysis and Recommendation System")

st.sidebar.title("👤 Your Financial Profile")

# File uploader
uploaded_file = st.sidebar.file_uploader("📁 Upload Credit Card Statement (CSV)", type=["csv"])
cibil_score = st.sidebar.number_input("📈 CIBIL Score", min_value=300, max_value=900, value=700, step=10)
credit_limit = st.sidebar.number_input("💳 Credit Limit", min_value=500, max_value=1000000, value=60000, step=500)
annual_income = st.sidebar.number_input("💼 Annual Salary", min_value=10000, max_value=500000, value=250000, step=1000)


st.sidebar.title("For Loan Recommendation")
amount = st.sidebar.number_input("💰 Desired Loan Amount (₹)", min_value=50000, step=50000, value=3000000)
loan_type = st.sidebar.selectbox("🏷️ Loan Type", sorted(loan_data["Loan Type"].unique()))
collateral = st.sidebar.radio("🏠 Collateral Available?", ["Yes", "No"])


col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💼 Annual Income", f"₹{annual_income:,}")
with col2:
    st.metric("💳 Credit Limit", f"₹{credit_limit:,}")
with col3:
    st.metric("📈 CIBIL Score", cibil_score)
st.markdown("### 🔎 Financial Profile Summary")
if cibil_score >= 750 and annual_income >= 300000:
    st.success("✅ You have a strong financial profile. Likely to get competitive loan & credit offers.")
elif cibil_score >= 650:
    st.warning("⚠️ Moderate financial health. Some restrictions may apply.")
else:
    st.error("❌ High risk profile. Improve your credit and income.")

st.markdown("""
    <style>
    div[data-baseweb="tabs"] button {
        font-size: 20px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(["📊 SPENDING OVERVIEW", "💳 CREDIT CARD SUGGESTIONS", "🏦 LOAN RECOMMENDATIONS"])

with tab1:
    if uploaded_file is not None:
        # Read the uploaded CSV
        df = pd.read_csv(uploaded_file)
        top_category = df.groupby('category')['amt'].sum().idxmax()

        # Preprocessing: Drop unnecessary columns (if present)
        drop_cols = ['trans_id', 'cc_num', 'merchant', 'first', 'last', 'street', 'city', 
                    'state', 'lat', 'long', 'merch_lat', 'merch_long', 'customer_id', 'is_fraud']
        df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True, errors='ignore')

        # Convert transaction date to useful features
        df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'], errors='coerce')
        df['trans_year'] = df['trans_date_trans_time'].dt.year
        df['trans_month'] = df['trans_date_trans_time'].dt.month
        df['trans_day'] = df['trans_date_trans_time'].dt.day
        df['trans_hour'] = df['trans_date_trans_time'].dt.hour
        df.drop(columns=['trans_date_trans_time'], inplace=True, errors='ignore')

        # Convert DOB to Age
        df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
        df['age'] = 2024 - df['dob'].dt.year
        df.drop(columns=['dob'], inplace=True, errors='ignore')

        # Handle missing values
        df.dropna(subset=['amt'], inplace=True)
        df.fillna(df.median(numeric_only=True), inplace=True)

        # Encode categorical features
        categorical_cols = ['category', 'gender', 'job']
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype(str)
                df[col] = df[col].apply(lambda x: x if x in label_encoders[col].classes_ else "Unknown")
                df[col] = label_encoders[col].transform(df[col])

        # Define features and target
        X = df.drop(columns=['amt'])
        y = np.log1p(df['amt'])

        X_scaled = scaler.transform(X)

        # Predict spending
        predictions = spending_model.predict(X_scaled)
        predicted_spending = np.expm1(predictions)

        # Add predictions to the dataframe
        df['Predicted Spending'] = predicted_spending


        st.subheader("📅 Monthly Spending Analysis")
        monthly_spending = df.groupby('trans_month')['amt'].sum()
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(x=monthly_spending.index, y=monthly_spending.values, marker='o', ax=ax)
        ax.axhline(y=credit_limit, color='r', linestyle='--', label='Credit Limit')
        ax.set_title("Monthly Spending vs Credit Limit")
        st.pyplot(fig)
        st.markdown("---")
        st.write("**Description:** This line graph shows your total spending per month compared to your credit limit. If spending frequently exceeds the limit, it can negatively impact your CIBIL score.")
        st.write("---")
        st.subheader("📢 CIBIL Score Insights & Recommendations")

        high_utilization_months = (monthly_spending / credit_limit) > 0.3
        very_high_utilization_months = (monthly_spending / credit_limit) > 0.7
        months_above_credit_limit = (monthly_spending >= credit_limit).sum()

        if months_above_credit_limit > 0:
            st.warning("⚠️ **High Credit Utilization Alert!**")
            st.write(f"You have exceeded your credit limit in **{months_above_credit_limit} month(s)**.")
            st.write("🔴 This significantly impacts your CIBIL score. Try to keep your spending within the limit to maintain a healthy credit profile.")
            st.write("💡 **Tip:** Consider requesting a credit limit increase or spacing out large purchases over different billing cycles.")

        elif very_high_utilization_months.sum() > len(monthly_spending) * 0.3:
            st.warning("⚠️ **Repeated High Credit Utilization Detected!**")
            st.write("🔴 Your spending exceeds **70% of your credit limit** in multiple months.")
            st.write("This indicates high dependency on credit, which may lower your CIBIL score.")
            st.write("💡 **Tip:** Reduce dependency on credit cards, and if possible, make mid-cycle payments to lower utilization.")

        elif high_utilization_months.sum() > len(monthly_spending) * 0.5:
            st.warning("⚠️ **Frequent High Credit Utilization**")
            st.write("🟠 Your spending often exceeds **50% of your credit limit**.")
            st.write("While this is not as risky as exceeding the limit, lenders prefer lower utilization.")
            st.write("💡 **Tip:** Try to keep your utilization below **30%** and spread expenses across multiple cards if possible.")

        elif high_utilization_months.sum() > 0:
            st.info("ℹ️ **Occasional High Spending**")
            st.write("🟡 You have exceeded **50% of your credit limit** in some months.")
            st.write("This is manageable but repeated high usage can negatively impact your CIBIL score.")
            st.write("💡 **Tip:** Consider making early payments to reduce high utilization during the billing cycle.")

        else:
            st.success("✅ **Healthy Credit Usage!**")
            st.write("🟢 Your spending is well within limits. This is a **positive** factor for your CIBIL Score!")
            st.write("💡 **Tip:** Continue maintaining low utilization, and make payments on time to sustain a good credit history.")
        st.write("---")
        st.subheader("🔍 Personalized Recommendations Based on Your Spending Pattern")

        if months_above_credit_limit > 0:
            st.write("🚨 **Urgent Action Needed:** Exceeding your credit limit frequently can severely damage your credit score.")
            st.write("✔️ Reduce unnecessary expenses and consider setting up alerts to track your usage.")

        if very_high_utilization_months.sum() > 0:
            st.write("📊 **You are heavily dependent on credit!** This pattern can make you appear risky to lenders.")
            st.write("✔️ Aim to reduce utilization or explore alternative financing options.")

        if high_utilization_months.sum() > 0:
            st.write("📉 **Your utilization is frequently high.** This can result in higher interest rates on future loans.")
            st.write("✔️ Try making early payments before your billing date.")

        if high_utilization_months.sum() == 0:
            st.write("🎉 **You have excellent spending habits!** Keep maintaining your responsible credit usage.")
            st.write("✔️ Consider applying for a higher credit limit while keeping utilization low for better financial flexibility.")
        # 📈 **Predicted vs Actual Spending Distribution**
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.histplot(predicted_spending, kde=True, color='blue', label='Predicted Spending', ax=ax2)
        sns.histplot(df['amt'], kde=True, color='red', label='Actual Spending', ax=ax2)
        ax2.legend()
        ax2.set_title("Predicted vs Actual Spending Distribution")
        #st.pyplot(fig2)
        #st.write("**Description:** This histogram compares actual spending (red) with predicted spending (blue). If the distributions align, the model is accurately analyzing spending behavior.")
        st.write("---")
        # 📊 **Total Spending by Category**
        st.subheader("📊 Total Spending by Category")
        category_spending = df.groupby('category')['amt'].sum().sort_values(ascending=False)
        category_labels = {index: label for index, label in enumerate(label_encoders['category'].classes_)}
        category_spending.index = category_spending.index.map(category_labels)
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        sns.barplot(x=category_spending.index, y=category_spending.values, ax=ax3)
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)
        st.pyplot(fig3)
        st.write("**Description:** This bar chart shows spending in different categories (food, travel, shopping, etc.), helping users understand their spending habits.")
        st.write("---")
        st.subheader("📎 Spending Distribution (Pie Chart)")
        fig4, ax4 = plt.subplots(figsize=(6, 6))
        ax4.pie(category_spending, labels=category_spending.index, autopct='%1.1f%%', startangle=140)
        st.pyplot(fig4)
        st.write("**Description:** This pie chart provides a percentage-based breakdown of total spending across categories, useful for optimizing cashback and rewards.")
        st.success(f"🔍 Based on your spending pattern, your top category is **{top_category}**")
        st.write("---")
with tab2:
    st.subheader("💳 Recommended Credit Cards")
    st.markdown("""
        <style>
            .card-style {
                background-color: #1e1e2f;
                padding: 1.5rem;
                border-radius: 15px;
                margin-bottom: 1rem;
                color: white;
                box-shadow: 0 0 10px rgba(0,0,0,0.2);
            }
            .card-style h4 { color: #00ffd5; }
            .card-detail { font-size: 0.9rem; margin: 3px 0; }
        </style>
    """, unsafe_allow_html=True)

    recommended_cards = []
    if 'top_category' in locals():
        for card in credit_cards_db.get(top_category, []):
            try:
                if "Eligibility" not in card or not card["Eligibility"]:
                    continue
                if isinstance(card["Eligibility"], str):
                    card["Eligibility"] = json.loads(card["Eligibility"])
                min_score = int(card["Eligibility"].get("min_score", 0))
                min_income = int(card["Eligibility"].get("min_income", 0))
                if cibil_score >= min_score and annual_income >= min_income:
                    recommended_cards.append(card)
            except Exception as e:
                st.warning(f"Error processing card: {e}")

    if recommended_cards:
        for card in recommended_cards:
            st.markdown(f"""
                <div class="card-style">
                    <h4>{card['Card']}</h4>
                    <div class="card-detail">🎁 Offer: {card['Offers']}</div>
                    <div class="card-detail">💰 Min Income: ₹{card['Eligibility']['min_income']:,}</div>
                    <div class="card-detail">📊 Min Score: {card['Eligibility']['min_score']}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("❌ No matching credit cards found.")



    if cibil_score < 650:
        st.warning("⚠️ **Low CIBIL Score Alert!**")
        st.write("📉 Your CIBIL score is below 650. You may face difficulties in getting new credit cards or loans.")
        st.write("🔍 **Alternative Financial Options:**")
        st.write("""
        - 💳 **Secured Credit Cards:** Use a fixed deposit to get a credit card & rebuild your score.
        - 🛒 **Buy Now, Pay Later (BNPL):** Platforms like ZestMoney & Simpl allow easy EMI-based payments.
        - 🏦 **Microloans:** Consider small personal loans from NBFCs (e.g., KreditBee, PaySense) to improve your credit history.
        """)

# -------------------------
# Loan Recommendation Logic
# -------------------------

def recommend_loans(credit_score, income, amount, loan_type, collateral, data):
    return data[
        (data["Loan Type"].str.lower() == loan_type.lower()) &
        (data["Min Credit Score"] <= credit_score) &
        (data["Min Income"] <= income) &
        (data["Max Loan Amount"] >= amount) &
        ((data["Collateral"].str.lower() == collateral.lower()) | (data["Collateral"].str.lower() == "no"))
    ].sort_values(by="Interest Rate")

# Loan Recommendations UI

with tab3:
        st.markdown("## 🏦 Loan Recommendations")
        st.markdown("Use your profile to explore the best loan options.")
        st.markdown("""
            <style>
                .loan-card {
                    background-color: #1e1e2f;
                    padding: 1.5rem;
                    border-radius: 15px;
                    margin-bottom: 1rem;
                    color: white;
                    box-shadow: 0 0 10px rgba(0,0,0,0.2);
                }
                .loan-card h4 { color: #00ffd5 }
            </style>
        """, unsafe_allow_html=True)

        matching_loans = recommend_loans(
            credit_score=cibil_score,
            income=annual_income,
            amount=amount,
            loan_type=loan_type,
            collateral=collateral,
            data=loan_data
        )

        if not matching_loans.empty:
            for _, loan in matching_loans.iterrows():
                st.markdown(f"""
                    <div class="loan-card">
                        <h4>{loan['Bank']}</h4>
                        <div>💰 Max Loan: ₹{loan['Max Loan Amount']:,}</div>
                        <div>📊 Interest Rate: {loan['Interest Rate']}%</div>
                        <div>🧾 Min Income: ₹{loan['Min Income']:,}</div>
                        <div>📈 Min Credit Score: {loan['Min Credit Score']}</div>
                        <div>🏷️ Collateral Needed: {loan['Collateral']}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Sorry, based on the provided inputs, no loan matches your profile right now.")

