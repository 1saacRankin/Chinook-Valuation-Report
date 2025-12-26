import streamlit as st
import pandas as pd
import json
from datetime import datetime
import io

# Set page config
st.set_page_config(page_title="Business Valuation Report Generator", layout="wide")

# Helper function to convert score to text answer
def score_to_answer(score, question_type):
    """Convert numeric score (1-5) to text answer"""
    answers = {
        'yes_no': {1: 'No', 2: 'Rarely', 3: 'Sometimes', 4: 'Usually', 5: 'Yes'},
        'percentage_low': {1: '>50%', 2: '31-50%', 3: '16-30%', 4: '6-15%', 5: '<5%'},
        'percentage_high': {1: '<1%', 2: '1-5%', 3: '6-10%', 4: '11-20%', 5: '>20%'},
        'percentage_reverse': {1: '0%', 2: '1-10%', 3: '11-25%', 4: '26-50%', 5: '>50%'},
        'ease': {1: "No - It's me and irreplaceable", 2: 'Very difficult', 3: 'Somewhat difficult', 4: 'Possible with training', 5: 'Yes - Easily replaceable'},
        'revenue_model': {1: 'Transactional/walk-in only', 2: 'Some repeat customers', 3: 'Mix of recurring and transactional', 4: 'Mostly recurring revenue', 5: 'High recurring revenue contracts'}
    }
    return answers[question_type].get(score, str(score))

# Initialize session state for data persistence
if 'financial_data' not in st.session_state:
    st.session_state.financial_data = pd.DataFrame({
        'Year': ['2021', '2022', '2023', '2024', '2025 proj.'],
        'Revenue': [1730366, 2280483, 2615371, 3312931, 2963256],
        'Cost of Goods': [1260059, 1593521, 2117285, 2282139, 1346344],
        'Total Expenses': [406140, 445220, 468856, 475083, 1106037],
        'Other Income': [0, 0, 20000, 0, 0]
    })

if 'normalization_data' not in st.session_state:
    st.session_state.normalization_data = pd.DataFrame({
        'Year': ['2021', '2022', '2023', '2024', '2025 proj.'],
        'Amortization': [114858, 103448, 104370, 98792, 0],
        'Interest (Capital Lease)': [14951, 15007, 11606, 4171, 0],
        'Management Salary': [0, 0, 0, 0, 230000],
        'Discretionary Expense': [0, 0, 0, 0, 0],
        'Manager Salary': [90000, 100000, 110000, 120000, 120000],
        'Year Weighting (%)': [0, 0, 0, 50, 50]
    })

# Title
st.title("🏢 Business Valuation Report Generator")
st.markdown("Generate comprehensive valuation report data in JSON format")

# Tabs for organization
tab1, tab2, tab3, tab4 = st.tabs(["📋 Company Info", "💰 Financial Data", "📊 Scorecard", "⬇️ Export"])

# ==================== TAB 1: COMPANY INFO ====================
with tab1:
    st.header("Company Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input("Company Name", value="Persaj Countertops Inc.")
        naics_code = st.text_input("NAICS Industry Code", value="Wood Kitchen Cabinet and Countertop Manufacturing (33711)")
    
    with col2:
        report_date = st.date_input("Report Date", value=datetime(2025, 11, 22))
        
    st.divider()
    
    st.subheader("Industry Benchmarks")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sample_size = st.number_input("Sample Size", value=1768, step=1)
        cost_of_goods_avg = st.number_input("Cost of Goods Avg (%)", value=65.68, step=0.01)
    
    with col2:
        total_expenses_avg = st.number_input("Total Expenses Avg (%)", value=28.55, step=0.01)
        total_employment_costs_avg = st.number_input("Employment Costs Avg (%)", value=33.06, step=0.01)
    
    with col3:
        your_cost_of_goods = st.number_input("Your Cost of Goods (%)", value=57.81, step=0.01)
        your_total_expenses = st.number_input("Your Total Expenses (%)", value=25.19, step=0.01)
        your_employment_costs = st.number_input("Your Employment Costs (%)", value=0.0, step=0.01)

# ==================== TAB 2: FINANCIAL DATA ====================
with tab2:
    st.header("Financial Data")
    
    # File upload option
    st.subheader("📁 Upload Financial Data (Optional)")
    uploaded_file = st.file_uploader("Upload CSV or Excel file with financial data", type=['csv', 'xlsx'])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("File uploaded successfully!")
            st.session_state.financial_data = df
        except Exception as e:
            st.error(f"Error reading file: {e}")
    
    st.divider()
    
    # Financial Data Table
    st.subheader("Income Statement Data")
    st.markdown("*Edit the table directly. Gross Profit and Net Income will be calculated automatically.*")
    
    edited_financial = st.data_editor(
        st.session_state.financial_data,
        use_container_width=True,
        num_rows="fixed",
        key="financial_editor"
    )
    
    # Calculate derived values
    edited_financial['Gross Profit'] = edited_financial['Revenue'] - edited_financial['Cost of Goods']
    edited_financial['Net Income'] = edited_financial['Gross Profit'] - edited_financial['Total Expenses'] + edited_financial['Other Income']
    
    # Display calculated values
    st.subheader("Calculated Values")
    calc_df = edited_financial[['Year', 'Gross Profit', 'Net Income']]
    st.dataframe(calc_df, use_container_width=True)
    
    st.session_state.financial_data = edited_financial
    
    st.divider()
    
    # Normalization Table
    st.subheader("Normalizations & Adjustments")
    
    edited_normalization = st.data_editor(
        st.session_state.normalization_data,
        use_container_width=True,
        num_rows="fixed",
        key="normalization_editor"
    )
    
    st.session_state.normalization_data = edited_normalization
    
    # Calculate SDE and Adj EBITDA
    total_adjustments = (edited_normalization['Amortization'] + 
                        edited_normalization['Interest (Capital Lease)'] + 
                        edited_normalization['Management Salary'] + 
                        edited_normalization['Discretionary Expense'])
    
    sde = edited_financial['Net Income'] + total_adjustments
    adj_ebitda = sde - edited_normalization['Manager Salary']
    
    calc_norm_df = pd.DataFrame({
        'Year': edited_normalization['Year'],
        'Total Adjustments': total_adjustments,
        'SDE': sde,
        'Adj. EBITDA': adj_ebitda
    })
    
    st.subheader("Calculated Normalization Values")
    st.dataframe(calc_norm_df, use_container_width=True)

# ==================== TAB 3: SCORECARD ====================
with tab3:
    st.header("Qualitative Scorecard")
    st.markdown("Rate each aspect from 1 (Poor) to 5 (Excellent)")
    
    # Finance & Operations
    st.subheader("🏦 Finance and General Operations")
    st.markdown("**Weight: 6.25% of valuation**")
    
    col1, col2 = st.columns(2)
    with col1:
        documented_processes = st.slider(
            "Does your firm have documented systemized business processes?",
            1, 5, 3,
            help="1 = No documentation, 5 = Fully documented"
        )
        st.caption(f"Answer: {score_to_answer(documented_processes, 'yes_no')}")
        
        accountant = st.slider(
            "Do you hire an accountant for year-end statements/tax returns?",
            1, 5, 5,
            help="1 = No, 5 = Yes, certified accountant"
        )
        st.caption(f"Answer: {score_to_answer(accountant, 'yes_no')}")
    
    with col2:
        annual_budget = st.slider(
            "Do you prepare an annual operating budget?",
            1, 5, 2,
            help="1 = No, 5 = Yes, detailed budget"
        )
        st.caption(f"Answer: {score_to_answer(annual_budget, 'yes_no')}")
        
        payables_on_time = st.slider(
            "Are your payables always paid in full and on-time?",
            1, 5, 5,
            help="1 = Often late, 5 = Always on time"
        )
        st.caption(f"Answer: {score_to_answer(payables_on_time, 'yes_no')}")
    
    st.divider()
    
    # Owner Dependency
    st.subheader("👤 Owner Dependency")
    st.markdown("**Weight: 6.25% of valuation**")
    
    col1, col2 = st.columns(2)
    with col1:
        thrive_without_owner = st.slider(
            "Would your company thrive if you left for 2 months?",
            1, 5, 2,
            help="1 = Would collapse, 5 = Would thrive"
        )
        st.caption(f"Answer: {score_to_answer(thrive_without_owner, 'yes_no')}")
        
        vacation_over_month = st.slider(
            "Have you taken a vacation longer than 1 month in the past 2 years?",
            1, 5, 1,
            help="1 = No, 5 = Yes, multiple times"
        )
        st.caption(f"Answer: {score_to_answer(vacation_over_month, 'yes_no')}")
    
    with col2:
        customers_ask_by_name = st.slider(
            "What percentage of customers ask for you by name?",
            1, 5, 5,
            help="1 = >50%, 5 = 0%"
        )
        st.caption(f"Answer: {score_to_answer(customers_ask_by_name, 'percentage_low')}")
    
    st.divider()
    
    # Growth Potential
    st.subheader("📈 Growth Potential")
    st.markdown("**Weight: 3.75% of valuation**")
    
    col1, col2 = st.columns(2)
    with col1:
        identified_opportunities = st.slider(
            "Have you identified growth opportunities in your business?",
            1, 5, 4,
            help="1 = No opportunities, 5 = Multiple documented opportunities"
        )
        st.caption(f"Answer: {score_to_answer(identified_opportunities, 'yes_no')}")
    
    with col2:
        revenue_increase_capacity = st.slider(
            "By how much could you increase revenues with current resources?",
            1, 5, 3,
            help="1 = 0%, 5 = >50%"
        )
        st.caption(f"Answer: {score_to_answer(revenue_increase_capacity, 'percentage_reverse')}")
    
    st.divider()
    
    # Recurring Revenues
    st.subheader("🔄 Recurring Revenues")
    st.markdown("**Weight: 2.5% of valuation**")
    
    revenue_model = st.slider(
        "Revenue Model Quality",
        1, 5, 2,
        help="1 = Transactional/walk-in only, 5 = High recurring revenue contracts"
    )
    st.caption(f"Answer: {score_to_answer(revenue_model, 'revenue_model')}")
    
    st.divider()
    
    # Organizational Stability
    st.subheader("🏛️ Organizational Stability")
    st.markdown("**Weight: 3.75% of valuation**")
    
    col1, col2 = st.columns(2)
    with col1:
        largest_customer = st.slider(
            "How much revenue does your largest customer represent?",
            1, 5, 5,
            help="1 = >25%, 5 = <5%"
        )
        st.caption(f"Answer: {score_to_answer(largest_customer, 'percentage_low')}")
        
        top_5_customers = st.slider(
            "How much revenue do your top 5 customers represent?",
            1, 5, 4,
            help="1 = >50%, 5 = <10%"
        )
        st.caption(f"Answer: {score_to_answer(top_5_customers, 'percentage_low')}")
        
        replace_sales_person = st.slider(
            "Could you easily replace the person most responsible for sales?",
            1, 5, 1,
            help="1 = It's me and irreplaceable, 5 = Easily replaceable"
        )
        st.caption(f"Answer: {score_to_answer(replace_sales_person, 'ease')}")
    
    with col2:
        replace_delivery_person = st.slider(
            "Could you easily replace the person most responsible for delivery?",
            1, 5, 1,
            help="1 = It's me and irreplaceable, 5 = Easily replaceable"
        )
        st.caption(f"Answer: {score_to_answer(replace_delivery_person, 'ease')}")
        
        replace_supplier = st.slider(
            "Could you easily replace your most important supplier?",
            1, 5, 5,
            help="1 = No alternatives, 5 = Multiple alternatives"
        )
        st.caption(f"Answer: {score_to_answer(replace_supplier, 'ease')}")
    
    st.divider()
    
    # Sales & Marketing
    st.subheader("📢 Sales and Marketing")
    st.markdown("**Weight: 2.5% of valuation**")
    
    col1, col2 = st.columns(2)
    with col1:
        customer_feedback = st.slider(
            "Do you collect customer feedback with a documented process?",
            1, 5, 2,
            help="1 = No, 5 = Yes, systematic process"
        )
        st.caption(f"Answer: {score_to_answer(customer_feedback, 'yes_no')}")
        
        marketing_spend = st.slider(
            "How much do you spend on marketing as % of revenue?",
            1, 5, 3,
            help="1 = <1%, 5 = >10%"
        )
        st.caption(f"Answer: {score_to_answer(marketing_spend, 'percentage_high')}")
    
    with col2:
        google_first_page = st.slider(
            "Do you show up on first page of local Google search?",
            1, 5, 5,
            help="1 = No, 5 = Yes, top result"
        )
        st.caption(f"Answer: {score_to_answer(google_first_page, 'yes_no')}")
        
        written_acquisition_strategy = st.slider(
            "Do you have a written customer acquisition strategy?",
            1, 5, 2,
            help="1 = No, 5 = Yes, comprehensive"
        )
        st.caption(f"Answer: {score_to_answer(written_acquisition_strategy, 'yes_no')}")

# ==================== TAB 4: EXPORT ====================
with tab4:
    st.header("Export Data")
    
    st.markdown("""
    Review your inputs and download the JSON file to use with the report generator.
    
    **Next Steps:**
    1. Review the data summary below
    2. Click 'Download JSON' to save the file
    3. Run: `python generate_report.py your_file.json`
    """)
    
    st.divider()
    
    # Calculate all derived values for export
    fin_data = st.session_state.financial_data
    norm_data = st.session_state.normalization_data
    
    gross_profit = (fin_data['Revenue'] - fin_data['Cost of Goods']).tolist()
    net_income = (fin_data['Gross Profit'] - fin_data['Total Expenses'] + fin_data['Other Income']).tolist()
    
    total_adjustments = (norm_data['Amortization'] + 
                        norm_data['Interest (Capital Lease)'] + 
                        norm_data['Management Salary'] + 
                        norm_data['Discretionary Expense']).tolist()
    
    sde_values = [net_income[i] + total_adjustments[i] for i in range(len(net_income))]
    adj_ebitda_values = [sde_values[i] - norm_data['Manager Salary'].tolist()[i] for i in range(len(sde_values))]
    
    # Calculate weighted averages (using last 2 years with 50% each)
    weighted_avg_revenue = (fin_data['Revenue'].iloc[3] * 0.5 + fin_data['Revenue'].iloc[4] * 0.5)
    weighted_avg_sde = (sde_values[3] * 0.5 + sde_values[4] * 0.5)
    
    # Simple valuation calculation (these would normally come from comparable transactions)
    revenue_multiple = 0.84
    sde_multiple = 3.7
    adj_ebitda_multiple = 4.45
    mpsp = int(weighted_avg_revenue * revenue_multiple)
    
    # Calculate scorecard adjustments based on scores
    def calculate_section_adjustment(scores, weight):
        """Calculate valuation adjustment for a section based on scores"""
        avg_score = sum(scores) / len(scores)
        # Score of 3 = neutral (0% adjustment)
        # Score of 1 = -weight% adjustment
        # Score of 5 = +weight% adjustment
        adjustment_pct = ((avg_score - 3) / 2) * weight
        return adjustment_pct
    
    # Calculate adjustments for each section
    finance_adj = calculate_section_adjustment(
        [documented_processes, accountant, annual_budget, payables_on_time], 6.25
    )
    owner_adj = calculate_section_adjustment(
        [thrive_without_owner, vacation_over_month, customers_ask_by_name], 6.25
    )
    growth_adj = calculate_section_adjustment(
        [identified_opportunities, revenue_increase_capacity], 3.75
    )
    recurring_adj = calculate_section_adjustment([revenue_model], 2.5)
    org_adj = calculate_section_adjustment(
        [largest_customer, top_5_customers, replace_sales_person, replace_delivery_person, replace_supplier], 3.75
    )
    sales_adj = calculate_section_adjustment(
        [customer_feedback, marketing_spend, google_first_page, written_acquisition_strategy], 2.5
    )
    
    total_adjustment_pct = finance_adj + owner_adj + growth_adj + recurring_adj + org_adj + sales_adj
    adjusted_mpsp = int(mpsp * (1 + total_adjustment_pct / 100))
    
    # Build JSON structure
    output_data = {
        "company": {
            "name": company_name,
            "naics_code": naics_code,
            "report_date": report_date.strftime("%B %d, %Y")
        },
        "valuation": {
            "mpsp": adjusted_mpsp,
            "base_mpsp": mpsp,
            "revenue_multiple": revenue_multiple,
            "sde_multiple": sde_multiple,
            "adj_ebitda_multiple": adj_ebitda_multiple,
            "weighted_avg_revenue": int(weighted_avg_revenue),
            "weighted_avg_sde": int(weighted_avg_sde)
        },
        "financial_data": {
            "years": fin_data['Year'].tolist(),
            "revenue": fin_data['Revenue'].tolist(),
            "cost_of_goods": fin_data['Cost of Goods'].tolist(),
            "gross_profit": gross_profit,
            "total_expenses": fin_data['Total Expenses'].tolist(),
            "net_income": net_income,
            "other_income": fin_data['Other Income'].tolist()
        },
        "normalizations": {
            "years": norm_data['Year'].tolist(),
            "amortization": norm_data['Amortization'].tolist(),
            "interest_capital_lease": norm_data['Interest (Capital Lease)'].tolist(),
            "management_salary": norm_data['Management Salary'].tolist(),
            "discretionary_expense": norm_data['Discretionary Expense'].tolist(),
            "total_adjustments": total_adjustments,
            "sde": sde_values,
            "manager_salary": norm_data['Manager Salary'].tolist(),
            "adj_ebitda": adj_ebitda_values,
            "year_weighting": norm_data['Year Weighting (%)'].tolist()
        },
        "industry_benchmarks": {
            "sample_size": sample_size,
            "cost_of_goods_avg": cost_of_goods_avg,
            "total_expenses_avg": total_expenses_avg,
            "total_employment_costs_avg": total_employment_costs_avg,
            "your_cost_of_goods": your_cost_of_goods,
            "your_total_expenses": your_total_expenses,
            "your_employment_costs": your_employment_costs
        },
        "scorecard": {
            "optimized_valuation": int(mpsp * 1.25),
            "minimum_valuation": int(mpsp * 0.75),
            "total_adjustment_pct": round(total_adjustment_pct, 2),
            "sections": {
                "finance_operations": {
                    "weight": 6.25,
                    "adjustment_pct": round(finance_adj, 2),
                    "questions": {
                        "documented_processes": score_to_answer(documented_processes, 'yes_no'),
                        "accountant": score_to_answer(accountant, 'yes_no'),
                        "annual_budget": score_to_answer(annual_budget, 'yes_no'),
                        "payables_on_time": score_to_answer(payables_on_time, 'yes_no')
                    },
                    "scores": {
                        "documented_processes": documented_processes,
                        "accountant": accountant,
                        "annual_budget": annual_budget,
                        "payables_on_time": payables_on_time,
                        "average": round(sum([documented_processes, accountant, annual_budget, payables_on_time]) / 4, 2)
                    }
                },
                "owner_dependency": {
                    "weight": 6.25,
                    "adjustment_pct": round(owner_adj, 2),
                    "questions": {
                        "thrive_without_owner": score_to_answer(thrive_without_owner, 'yes_no'),
                        "vacation_over_month": score_to_answer(vacation_over_month, 'yes_no'),
                        "customers_ask_by_name_pct": score_to_answer(customers_ask_by_name, 'percentage_low')
                    },
                    "scores": {
                        "thrive_without_owner": thrive_without_owner,
                        "vacation_over_month": vacation_over_month,
                        "customers_ask_by_name": customers_ask_by_name,
                        "average": round(sum([thrive_without_owner, vacation_over_month, customers_ask_by_name]) / 3, 2)
                    }
                },
                "growth_potential": {
                    "weight": 3.75,
                    "adjustment_pct": round(growth_adj, 2),
                    "questions": {
                        "identified_opportunities": score_to_answer(identified_opportunities, 'yes_no'),
                        "revenue_increase_capacity": score_to_answer(revenue_increase_capacity, 'percentage_reverse')
                    },
                    "scores": {
                        "identified_opportunities": identified_opportunities,
                        "revenue_increase_capacity": revenue_increase_capacity,
                        "average": round(sum([identified_opportunities, revenue_increase_capacity]) / 2, 2)
                    }
                },
                "recurring_revenues": {
                    "weight": 2.5,
                    "adjustment_pct": round(recurring_adj, 2),
                    "questions": {
                        "revenue_model": score_to_answer(revenue_model, 'revenue_model')
                    },
                    "scores": {
                        "revenue_model": revenue_model,
                        "average": revenue_model
                    }
                },
                "organizational_stability": {
                    "weight": 3.75,
                    "adjustment_pct": round(org_adj, 2),
                    "questions": {
                        "largest_customer_pct": score_to_answer(largest_customer, 'percentage_low'),
                        "top_5_customers_pct": score_to_answer(top_5_customers, 'percentage_low'),
                        "replace_sales_person": score_to_answer(replace_sales_person, 'ease'),
                        "replace_delivery_person": score_to_answer(replace_delivery_person, 'ease'),
                        "replace_supplier": score_to_answer(replace_supplier, 'ease')
                    },
                    "scores": {
                        "largest_customer": largest_customer,
                        "top_5_customers": top_5_customers,
                        "replace_sales_person": replace_sales_person,
                        "replace_delivery_person": replace_delivery_person,
                        "replace_supplier": replace_supplier,
                        "average": round(sum([largest_customer, top_5_customers, replace_sales_person, replace_delivery_person, replace_supplier]) / 5, 2)
                    }
                },
                "sales_marketing": {
                    "weight": 2.5,
                    "adjustment_pct": round(sales_adj, 2),
                    "questions": {
                        "customer_feedback": score_to_answer(customer_feedback, 'yes_no'),
                        "marketing_spend_pct": score_to_answer(marketing_spend, 'percentage_high'),
                        "google_first_page": score_to_answer(google_first_page, 'yes_no'),
                        "written_acquisition_strategy": score_to_answer(written_acquisition_strategy, 'yes_no')
                    },
                    "scores": {
                        "customer_feedback": customer_feedback,
                        "marketing_spend": marketing_spend,
                        "google_first_page": google_first_page,
                        "written_acquisition_strategy": written_acquisition_strategy,
                        "average": round(sum([customer_feedback, marketing_spend, google_first_page, written_acquisition_strategy]) / 4, 2)
                    }
                }
            }
        },
        "comparable_transactions": {
            "count": 16,
            "revenue_range": [2816110, 3705479],
            "transactions": [
                {"naics": "336411", "revenue": 3702307, "sde": 952988, "adj_ebitda": 812988, "price": 4250000, "rev_mult": 1.15, "sde_mult": 4.46, "ebitda_mult": 5.23},
                {"naics": "336211", "revenue": 3648000, "sde": 853000, "adj_ebitda": 753000, "price": 2900000, "rev_mult": 0.79, "sde_mult": 3.4, "ebitda_mult": 3.85},
                {"naics": "333318", "revenue": 3136708, "sde": 784618, "adj_ebitda": 692740, "price": 2950000, "rev_mult": 0.94, "sde_mult": 3.76, "ebitda_mult": 4.26},
                {"naics": "332710", "revenue": 3705479, "sde": 758541, "adj_ebitda": 670992, "price": 2712283, "rev_mult": 0.73, "sde_mult": 3.58, "ebitda_mult": 4.04},
                {"naics": "332721", "revenue": 3276000, "sde": 877000, "adj_ebitda": 604000, "price": 4864000, "rev_mult": 1.48, "sde_mult": 5.55, "ebitda_mult": 8.05},
                {"naics": "336310", "revenue": 3673000, "sde": 694878, "adj_ebitda": 603000, "price": 2139000, "rev_mult": 0.58, "sde_mult": 3.08, "ebitda_mult": 3.55},
                {"naics": "336390", "revenue": 3172000, "sde": 743000, "adj_ebitda": 574000, "price": 1900000, "rev_mult": 0.6, "sde_mult": 2.56, "ebitda_mult": 3.31},
                {"naics": "333111", "revenue": 3127292, "sde": 588895, "adj_ebitda": 549500, "price": 2400000, "rev_mult": 0.77, "sde_mult": 4.08, "ebitda_mult": 4.37},
                {"naics": "332919", "revenue": 3493053, "sde": 934056, "adj_ebitda": 700056, "price": 2500000, "rev_mult": 0.72, "sde_mult": 2.68, "ebitda_mult": 3.57},
                {"naics": "332313", "revenue": 3445726, "sde": 721348, "adj_ebitda": 629470, "price": 4000000, "rev_mult": 1.16, "sde_mult": 5.55, "ebitda_mult": 6.35},
                {"naics": "337127", "revenue": 3317418, "sde": 710828, "adj_ebitda": 618950, "price": 2700000, "rev_mult": 0.81, "sde_mult": 3.8, "ebitda_mult": 4.36},
                {"naics": "332710", "revenue": 3404875, "sde": 881344, "adj_ebitda": 606344, "price": 3500000, "rev_mult": 1.03, "sde_mult": 3.97, "ebitda_mult": 5.77},
                {"naics": "332710", "revenue": 2833249, "sde": 653072, "adj_ebitda": 546072, "price": 1900000, "rev_mult": 0.67, "sde_mult": 2.91, "ebitda_mult": 3.48},
                {"naics": "334516", "revenue": 2816110, "sde": 700853, "adj_ebitda": 538138, "price": 2100000, "rev_mult": 0.75, "sde_mult": 3.0, "ebitda_mult": 3.9},
                {"naics": "332322", "revenue": 2844787, "sde": 571739, "adj_ebitda": 451739, "price": 2400000, "rev_mult": 0.84, "sde_mult": 4.2, "ebitda_mult": 5.31},
                {"naics": "339950", "revenue": 3200000, "sde": 713000, "adj_ebitda": 621122, "price": 2725000, "rev_mult": 0.85, "sde_mult": 3.82, "ebitda_mult": 4.39}
            ]
        }
    }
    
    # Display summary
    st.subheader("📊 Valuation Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Base MPSP", f"${mpsp:,.0f}")
        st.metric("Adjusted MPSP", f"${adjusted_mpsp:,.0f}", 
                  delta=f"{total_adjustment_pct:+.1f}%")
    with col2:
        st.metric("Weighted Avg Revenue", f"${weighted_avg_revenue:,.0f}")
    with col3:
        st.metric("Weighted Avg SDE", f"${weighted_avg_sde:,.0f}")
    
    st.divider()
    
    # Scorecard breakdown
    st.subheader("📈 Scorecard Breakdown")
    
    sections_data = [
        ("Finance & Operations", finance_adj, (documented_processes + accountant + annual_budget + payables_on_time) / 4),
        ("Owner Dependency", owner_adj, (thrive_without_owner + vacation_over_month + customers_ask_by_name) / 3),
        ("Growth Potential", growth_adj, (identified_opportunities + revenue_increase_capacity) / 2),
        ("Recurring Revenues", recurring_adj, revenue_model),
        ("Organizational Stability", org_adj, (largest_customer + top_5_customers + replace_sales_person + replace_delivery_person + replace_supplier) / 5),
        ("Sales & Marketing", sales_adj, (customer_feedback + marketing_spend + google_first_page + written_acquisition_strategy) / 4)
    ]
    
    for section_name, adjustment, avg_score in sections_data:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**{section_name}**")
        with col2:
            st.metric("Avg Score", f"{avg_score:.2f}/5", delta=None)
        with col3:
            st.metric("Adjustment", f"{adjustment:+.2f}%")
    
    st.divider()
    
    # JSON preview
    with st.expander("🔍 Preview JSON Output"):
        st.json(output_data)
    
    # Download button
    json_string = json.dumps(output_data, indent=2)
    
    st.download_button(
        label="⬇️ Download JSON File",
        data=json_string,
        file_name=f"{company_name.replace(' ', '_').replace('.', '')}_valuation_data.json",
        mime="application/json",
        use_container_width=True
    )
    
    st.success("✅ Ready to download! Use this JSON file with: `python generate_report.py your_file.json`")

# Sidebar with instructions
with st.sidebar:
    st.title("📖 Instructions")
    
    st.markdown("""
    ### How to Use
    
    1. **Company Info**: Enter basic company details and benchmarks
    2. **Financial Data**: 
       - Upload CSV/Excel or use default data
       - Edit financial tables directly
       - Review calculated values
    3. **Scorecard**: Rate qualitative factors (1-5)
       - 1 = Poor/Needs Improvement
       - 3 = Average/Neutral
       - 5 = Excellent/Best
    4. **Export**: 
       - Review summary and adjustments
       - Download JSON file
       - Generate PDF report
    
    ### Scorecard Impact
    - Each section has a weight (% of valuation)
    - Scores above 3 increase valuation
    - Scores below 3 decrease valuation
    - Total adjustment: ±25% maximum
    
    ### Generate Report
    ```bash
    python generate_report.py your_file.json
    pdflatex valuation_report.tex
    ```
    """)
    
    st.divider()
    
    st.info("💡 **Tip**: Hover over sliders for detailed descriptions of each rating level.")