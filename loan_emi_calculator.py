import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Dynamic Loan EMI Calculator",
    page_icon="💰",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        height: 3em;
        border-radius: 10px;
    }
    .stProgress > div > div > div > div {
        background-color: #ff4b4b;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

def calculate_emi(principal, rate, time):
    rate = rate / (12 * 100)
    emi = principal * rate * (1 + rate)**time / ((1 + rate)**time - 1)
    return emi

def create_amortization_schedule(principal, rate, time, monthly_emi):
    schedule_data = []
    balance = principal
    monthly_rate = rate / (12 * 100)
    
    for month in range(1, time + 1):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_emi - interest_payment
        balance = balance - principal_payment
        
        # Calculate payment date
        payment_date = (datetime.now() + timedelta(days=30*month)).strftime('%Y-%m-%d')
        
        schedule_data.append({
            "Payment Date": payment_date,
            "Month": month,
            "EMI": monthly_emi,
            "Principal": principal_payment,
            "Interest": interest_payment,
            "Balance": max(balance, 0)
        })
    
    return pd.DataFrame(schedule_data)

def main():
    # Header
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>💰 Smart Loan EMI Calculator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em;'>Plan your loan with confidence</p>", unsafe_allow_html=True)
    
    # Create two columns for input and summary
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("### 📝 Loan Details")
        loan_types = ["Home Loan", "Personal Loan", "Car Loan", "Education Loan", "Business Loan"]
        loan_type = st.selectbox("Select Loan Type", loan_types)
        
        principal = st.number_input(
            "Enter Loan Amount ($)",
            min_value=1000,
            value=100000,
            step=1000,
            format="%d"
        )
        
        rate = st.slider(
            "Annual Interest Rate (%)",
            min_value=1.0,
            max_value=30.0,
            value=10.0,
            step=0.1
        )
        
        tenure_years = st.slider(
            "Loan Tenure (Years)",
            min_value=1,
            max_value=30,
            value=5
        )
        
        tenure_months = tenure_years * 12
        
        calculate_button = st.button("Calculate EMI")
    
    if calculate_button:
        monthly_emi = calculate_emi(principal, rate, tenure_months)
        total_payment = monthly_emi * tenure_months
        total_interest = total_payment - principal
        
        with col2:
            st.markdown("### 📊 Loan Summary")
            
            # Display metrics in a more attractive way
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.metric("Monthly EMI", f"${monthly_emi:,.2f}")
            with metric_col2:
                st.metric("Total Interest", f"${total_interest:,.2f}")
            with metric_col3:
                st.metric("Total Payment", f"${total_payment:,.2f}")
            
            # Add a progress bar showing loan completion
            st.markdown("### Loan Progress")
            st.progress(0.0)  # Starting progress
            
            # Create interactive charts
            tab1, tab2 = st.tabs(["📈 Payment Breakdown", "📅 Amortization Schedule"])
            
            with tab1:
                # Create a more detailed payment breakdown
                fig = go.Figure()
                fig.add_trace(go.Pie(
                    labels=['Principal', 'Interest'],
                    values=[principal, total_interest],
                    hole=0.4,
                    marker_colors=['#ff4b4b', '#ff9999']
                ))
                fig.update_layout(
                    title="Loan Payment Distribution",
                    annotations=[dict(text=f'Total\n${total_payment:,.0f}', x=0.5, y=0.5, font_size=15, showarrow=False)]
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Add monthly payment trend
                schedule_df = create_amortization_schedule(principal, rate, tenure_months, monthly_emi)
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(x=schedule_df['Month'], y=schedule_df['Principal'], name='Principal', fill='tonexty'))
                fig2.add_trace(go.Scatter(x=schedule_df['Month'], y=schedule_df['Interest'], name='Interest', fill='tonexty'))
                fig2.update_layout(title='Monthly Payment Trend', xaxis_title='Month', yaxis_title='Amount ($)')
                st.plotly_chart(fig2, use_container_width=True)
            
            with tab2:
                st.markdown("### Detailed Repayment Schedule")
                st.dataframe(
                    schedule_df.style.format({
                        "EMI": "${:,.2f}",
                        "Principal": "${:,.2f}",
                        "Interest": "${:,.2f}",
                        "Balance": "${:,.2f}"
                    }),
                    height=400
                )
                
                # Add download button for the schedule
                csv = schedule_df.to_csv(index=False)
                st.download_button(
                    label="Download Repayment Schedule",
                    data=csv,
                    file_name="loan_schedule.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
