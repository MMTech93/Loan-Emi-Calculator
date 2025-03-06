import streamlit as st
import numpy as np

def calculate_emi(principal, rate, time):
    # Convert interest rate from percentage to decimal and monthly rate
    rate = rate / (12 * 100)
    
    # Calculate EMI using the formula: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    emi = principal * rate * (1 + rate)**time / ((1 + rate)**time - 1)
    
    return emi

def main():
    st.title("Loan EMI Calculator")
    
    # Add a header image (optional)
    st.image("https://img.freepik.com/free-vector/loan-concept-illustration_114360-7534.jpg", width=300)
    
    # Create input fields
    principal = st.number_input("Enter Loan Amount (₹)", min_value=1000, value=100000, step=1000)
    
    rate = st.number_input("Enter Annual Interest Rate (%)", min_value=1.0, max_value=30.0, value=10.0, step=0.1)
    
    tenure_years = st.number_input("Enter Loan Tenure (Years)", min_value=1, max_value=30, value=5, step=1)
    tenure_months = tenure_years * 12
    
    if st.button("Calculate EMI"):
        # Calculate EMI
        monthly_emi = calculate_emi(principal, rate, tenure_months)
        
        # Calculate total payment and interest
        total_payment = monthly_emi * tenure_months
        total_interest = total_payment - principal
        
        # Display results in a nice format
        st.success(f"Monthly EMI: ₹{monthly_emi:,.2f}")
        
        # Create columns for displaying additional information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"Principal Amount:\n₹{principal:,.2f}")
        
        with col2:
            st.info(f"Total Interest:\n₹{total_interest:,.2f}")
        
        with col3:
            st.info(f"Total Payment:\n₹{total_payment:,.2f}")
        
        # Display payment breakdown in a pie chart
        st.subheader("Payment Breakdown")
        import plotly.express as px
        
        fig = px.pie(
            values=[principal, total_interest],
            names=['Principal', 'Interest'],
            title='Loan Payment Breakdown'
        )
        st.plotly_chart(fig)
        
        # Display monthly payment schedule
        st.subheader("Monthly Payment Schedule")
        
        balance = principal
        schedule_data = []
        
        for month in range(1, tenure_months + 1):
            interest_payment = balance * (rate / (12 * 100))
            principal_payment = monthly_emi - interest_payment
            balance = balance - principal_payment
            
            schedule_data.append({
                "Month": month,
                "EMI": monthly_emi,
                "Principal": principal_payment,
                "Interest": interest_payment,
                "Balance": balance if balance > 0 else 0
            })
        
        import pandas as pd
        schedule_df = pd.DataFrame(schedule_data)
        st.dataframe(schedule_df.style.format({
            "EMI": "₹{:,.2f}",
            "Principal": "₹{:,.2f}",
            "Interest": "₹{:,.2f}",
            "Balance": "₹{:,.2f}"
        }))

if __name__ == "__main__":
    main()