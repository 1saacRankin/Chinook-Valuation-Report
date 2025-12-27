import streamlit as st
import pandas as pd
import json
from datetime import datetime
import io
from rapidfuzz import fuzz, process
import os

# Set page config
st.set_page_config(page_title="Business Valuation Report Generator", layout="wide")

# Complete NAICS Code Structure
NAICS_CODES = {
    "11": "Agriculture, Forestry, Fishing and Hunting",
    "21": "Mining, Quarrying, and Oil and Gas Extraction",
    "22": "Utilities",
    "23": "Construction",
    "31-33": "Manufacturing",
    "42": "Wholesale Trade",
    "44-45": "Retail Trade",
    "48-49": "Transportation and Warehousing",
    "51": "Information",
    "52": "Finance and Insurance",
    "53": "Real Estate and Rental and Leasing",
    "54": "Professional, Scientific, and Technical Services",
    "55": "Management of Companies and Enterprises",
    "56": "Administrative and Support Services",
    "61": "Educational Services",
    "62": "Health Care and Social Assistance",
    "71": "Arts, Entertainment, and Recreation",
    "72": "Accommodation and Food Services",
    "81": "Other Services (except Public Administration)",
    "92": "Public Administration"
}

NAICS_SUBCODES = {
    # Agriculture
    "11": {
        "111": "Crop Production",
        "112": "Animal Production",
        "113": "Forestry and Logging",
        "114": "Fishing, Hunting and Trapping",
        "115": "Support Activities for Agriculture and Forestry"
    },
    # Mining
    "21": {
        "211": "Oil and Gas Extraction",
        "212": "Mining (except Oil and Gas)",
        "213": "Support Activities for Mining"
    },
    # Utilities
    "22": {
        "221": "Utilities"
    },
    # Construction
    "23": {
        "236": "Construction of Buildings",
        "237": "Heavy and Civil Engineering Construction",
        "238": "Specialty Trade Contractors"
    },
    # Manufacturing
    "31-33": {
        "311": "Food Manufacturing",
        "312": "Beverage and Tobacco Product Manufacturing",
        "313": "Textile Mills",
        "314": "Textile Product Mills",
        "315": "Apparel Manufacturing",
        "316": "Leather and Allied Product Manufacturing",
        "321": "Wood Product Manufacturing",
        "322": "Paper Manufacturing",
        "323": "Printing and Related Support Activities",
        "324": "Petroleum and Coal Products Manufacturing",
        "325": "Chemical Manufacturing",
        "326": "Plastics and Rubber Products Manufacturing",
        "327": "Nonmetallic Mineral Product Manufacturing",
        "331": "Primary Metal Manufacturing",
        "332": "Fabricated Metal Product Manufacturing",
        "333": "Machinery Manufacturing",
        "334": "Computer and Electronic Product Manufacturing",
        "335": "Electrical Equipment Manufacturing",
        "336": "Transportation Equipment Manufacturing",
        "337": "Furniture and Related Product Manufacturing",
        "339": "Miscellaneous Manufacturing"
    },
    # Wholesale Trade
    "42": {
        "423": "Merchant Wholesalers, Durable Goods",
        "424": "Merchant Wholesalers, Nondurable Goods",
        "425": "Wholesale Electronic Markets"
    },
    # Retail Trade
    "44-45": {
        "441": "Motor Vehicle and Parts Dealers",
        "442": "Furniture and Home Furnishings Stores",
        "443": "Electronics and Appliance Stores",
        "444": "Building Material and Garden Equipment Dealers",
        "445": "Food and Beverage Stores",
        "446": "Health and Personal Care Stores",
        "447": "Gasoline Stations",
        "448": "Clothing and Accessories Stores",
        "451": "Sporting Goods, Hobby, Book, and Music Stores",
        "452": "General Merchandise Stores",
        "453": "Miscellaneous Store Retailers",
        "454": "Nonstore Retailers"
    },
    # Transportation
    "48-49": {
        "481": "Air Transportation",
        "482": "Rail Transportation",
        "483": "Water Transportation",
        "484": "Truck Transportation",
        "485": "Transit and Ground Passenger Transportation",
        "486": "Pipeline Transportation",
        "487": "Scenic and Sightseeing Transportation",
        "488": "Support Activities for Transportation",
        "492": "Couriers and Messengers",
        "493": "Warehousing and Storage"
    },
    # Information
    "51": {
        "511": "Publishing Industries",
        "512": "Motion Picture and Sound Recording Industries",
        "515": "Broadcasting",
        "517": "Telecommunications",
        "518": "Data Processing, Hosting, and Related Services",
        "519": "Other Information Services"
    },
    # Finance and Insurance
    "52": {
        "521": "Monetary Authorities - Central Bank",
        "522": "Credit Intermediation and Related Activities",
        "523": "Securities, Commodity Contracts, and Other Financial Investments",
        "524": "Insurance Carriers and Related Activities",
        "525": "Funds, Trusts, and Other Financial Vehicles"
    },
    # Real Estate
    "53": {
        "531": "Real Estate",
        "532": "Rental and Leasing Services",
        "533": "Lessors of Nonfinancial Intangible Assets"
    },
    # Professional Services
    "54": {
        "541": "Professional, Scientific, and Technical Services"
    },
    # Management
    "55": {
        "551": "Management of Companies and Enterprises"
    },
    # Administrative Services
    "56": {
        "561": "Administrative and Support Services",
        "562": "Waste Management and Remediation Services"
    },
    # Educational Services
    "61": {
        "611": "Educational Services"
    },
    # Health Care
    "62": {
        "621": "Ambulatory Health Care Services",
        "622": "Hospitals",
        "623": "Nursing and Residential Care Facilities",
        "624": "Social Assistance"
    },
    # Arts and Entertainment
    "71": {
        "711": "Performing Arts, Spectator Sports, and Related Industries",
        "712": "Museums, Historical Sites, and Similar Institutions",
        "713": "Amusement, Gambling, and Recreation Industries"
    },
    # Accommodation and Food
    "72": {
        "721": "Accommodation",
        "722": "Food Services and Drinking Places"
    },
    # Other Services
    "81": {
        "811": "Repair and Maintenance",
        "812": "Personal and Laundry Services",
        "813": "Religious, Grantmaking, Civic, Professional Organizations",
        "814": "Private Households"
    },
    # Manufacturing subcategories
    "311": {
        "3111": "Animal Food Manufacturing",
        "3112": "Grain and Oilseed Milling",
        "3113": "Sugar and Confectionery Product Manufacturing",
        "3114": "Fruit and Vegetable Preserving",
        "3115": "Dairy Product Manufacturing",
        "3116": "Animal Slaughtering and Processing",
        "3117": "Seafood Product Preparation and Packaging",
        "3118": "Bakeries and Tortilla Manufacturing",
        "3119": "Other Food Manufacturing"
    },
    "3119": {
        "31194": "Seasoning and Dressing Manufacturing",
        "31199": "All Other Food Manufacturing"
    },
    "31199": {
        "311999": "All Other Miscellaneous Food Manufacturing"
    },
    "423": {
        "4231": "Motor Vehicle and Parts Merchant Wholesalers",
        "4232": "Furniture and Home Furnishing Merchant Wholesalers",
        "4233": "Lumber and Other Construction Materials Merchant Wholesalers",
        "4234": "Professional and Commercial Equipment Merchant Wholesalers",
        "4235": "Metal and Mineral Merchant Wholesalers",
        "4236": "Household Appliances and Electrical Equipment Merchant Wholesalers",
        "4237": "Hardware, Plumbing, Heating Equipment Merchant Wholesalers",
        "4238": "Machinery, Equipment, and Supplies Merchant Wholesalers",
        "4239": "Miscellaneous Durable Goods Merchant Wholesalers"
    },
    "541": {
        "5411": "Legal Services",
        "5412": "Accounting, Tax Preparation, Bookkeeping Services",
        "5413": "Architectural, Engineering Services",
        "5414": "Specialized Design Services",
        "5415": "Computer Systems Design Services",
        "5416": "Management, Scientific, Technical Consulting Services",
        "5417": "Scientific Research and Development Services",
        "5418": "Advertising, Public Relations Services",
        "5419": "Other Professional, Scientific, Technical Services"
    },
    "621": {
        "6211": "Offices of Physicians",
        "6212": "Offices of Dentists",
        "6213": "Offices of Other Health Practitioners",
        "6214": "Outpatient Care Centers",
        "6215": "Medical and Diagnostic Laboratories",
        "6216": "Home Health Care Services",
        "6219": "Other Ambulatory Health Care Services"
    },
    "722": {
        "7221": "Full-Service Restaurants",
        "7222": "Limited-Service Restaurants",
        "7223": "Special Food Services",
        "7224": "Drinking Places (Alcoholic Beverages)"
    }
}

# Load PeerComps dataset
@st.cache_data
def load_peercomps():
    """Load the PeerComps dataset"""
    try:
        if os.path.exists('PeerComps_dataset.xlsx'):
            df = pd.read_excel('PeerComps_dataset.xlsx')
            # Clean column names - strip whitespace and standardize
            df.columns = df.columns.str.strip()
            
            # Remove any completely empty rows
            df = df.dropna(how='all')
            
            # Remove header rows that might be in the data
            # (sometimes Excel files have multiple header rows)
            if len(df) > 0:
                # Check if first row looks like a header
                first_row = df.iloc[0]
                if any(str(val).lower() in ['naics', 'revenue', 'price', 'year'] for val in first_row):
                    df = df.iloc[1:]
                    df = df.reset_index(drop=True)
            
            # Print column names for debugging
            print(f"PeerComps columns: {df.columns.tolist()}")
            print(f"PeerComps shape: {df.shape}")
            
            return df
        else:
            st.warning("PeerComps_dataset.xlsx not found in current directory. Using sample data.")
            return None
    except Exception as e:
        st.error(f"Error loading PeerComps dataset: {e}")
        import traceback
        print(traceback.format_exc())
        return None

def find_column(df, search_terms, exact_first=True):
    """
    Robustly find a column in the dataframe
    
    Args:
        df: DataFrame to search
        search_terms: List of terms to search for (in order of preference)
        exact_first: If True, try exact matches first
    
    Returns:
        Column name if found, None otherwise
    """
    if df is None or df.empty:
        return None
    
    # Normalize column names
    cols_lower = {col: col.lower().strip() for col in df.columns}
    
    # Try exact matches first
    if exact_first:
        for term in search_terms:
            term_lower = term.lower().strip()
            for col, col_lower in cols_lower.items():
                if col_lower == term_lower:
                    return col
    
    # Try partial matches
    for term in search_terms:
        term_lower = term.lower().strip()
        for col, col_lower in cols_lower.items():
            if term_lower in col_lower:
                return col
    
    return None

def find_comparable_transactions(naics_code, revenue, year_range=5, max_results=20, usd_to_cad=1.40):
    """
    Find comparable transactions from PeerComps dataset
    
    Args:
        naics_code: NAICS code to search for
        revenue: Company's revenue for filtering
        year_range: How many years back to look
        max_results: Maximum number of comparables to return
        usd_to_cad: USD to CAD exchange rate
    """
    df = load_peercomps()
    
    if df is None or df.empty:
        # Return sample data if dataset not available
        return generate_sample_comparables(revenue, usd_to_cad)
    
    # Clean the dataframe
    df = df.copy()
    
    # Find required columns using robust search
    naics_col = find_column(df, ['NAICS Code', 'NAICS', 'naics_code', 'Industry Code'])
    year_col = find_column(df, ['Year', 'year', 'Transaction Year', 'Sale Year'])
    revenue_col = find_column(df, ['Revenue', 'revenue', 'Sales', 'Annual Revenue'])
    price_col = find_column(df, ['Sale Price', 'Price', 'price', 'Transaction Price', 'Purchase Price'])
    sde_col = find_column(df, ['SDE', 'sde', 'Seller Discretionary Earnings'])
    ebitda_col = find_column(df, ['EBITDA', 'ebitda', 'Adj EBITDA', 'Adjusted EBITDA'])
    
    # Find multiple columns
    rev_mult_col = find_column(df, ['P/R', 'p/r', 'Revenue Multiple', 'Price/Revenue'])
    sde_mult_col = find_column(df, ['P/SDE', 'p/sde', 'SDE Multiple', 'Price/SDE'])
    ebitda_mult_col = find_column(df, ['P/EBITDA', 'p/ebitda', 'EBITDA Multiple', 'Price/EBITDA'])
    
    # Debug info
    if naics_col is None:
        available_cols = ", ".join(df.columns.tolist()[:10])
        st.warning(f"Could not find NAICS column. Available columns: {available_cols}... Using sample data.")
        return generate_sample_comparables(revenue, usd_to_cad)
    
    # Extract numeric NAICS code (remove any text descriptions)
    naics_clean = ''.join(filter(str.isdigit, str(naics_code)))
    
    # Current year for filtering
    current_year = datetime.now().year
    min_year = current_year - year_range
    
    # Filter by NAICS code (match first 3-6 digits depending on specificity)
    naics_lengths = [6, 5, 4, 3, 2]  # Try matching from most to least specific
    filtered_df = pd.DataFrame()
    
    for length in naics_lengths:
        if len(naics_clean) >= length:
            naics_prefix = naics_clean[:length]
            try:
                # Convert NAICS column to string and extract digits only
                df['naics_clean'] = df[naics_col].astype(str).apply(lambda x: ''.join(filter(str.isdigit, x)))
                temp_df = df[df['naics_clean'].str[:length] == naics_prefix]
                if not temp_df.empty:
                    filtered_df = temp_df
                    st.info(f"Found {len(filtered_df)} transactions matching NAICS prefix: {naics_prefix} ({length} digits)")
                    break
            except Exception as e:
                continue
    
    if filtered_df.empty:
        st.warning(f"No NAICS matches found for {naics_code}. Using sample data.")
        return generate_sample_comparables(revenue, usd_to_cad)
    
    # Filter by year if column exists
    if year_col and year_col in filtered_df.columns:
        try:
            filtered_df[year_col] = pd.to_numeric(filtered_df[year_col], errors='coerce')
            filtered_df = filtered_df[filtered_df[year_col] >= min_year]
            if not filtered_df.empty:
                st.info(f"Filtered to {len(filtered_df)} transactions from {min_year} onwards")
        except Exception as e:
            st.warning(f"Could not filter by year: {e}")
    
    # Filter by similar revenue (within 50% to 200% of target)
    if revenue_col and revenue_col in filtered_df.columns and revenue > 0:
        try:
            filtered_df[revenue_col] = pd.to_numeric(filtered_df[revenue_col], errors='coerce')
            before_count = len(filtered_df)
            filtered_df = filtered_df[
                (filtered_df[revenue_col] >= revenue * 0.5) & 
                (filtered_df[revenue_col] <= revenue * 2.0)
            ]
            if len(filtered_df) < before_count:
                st.info(f"Filtered to {len(filtered_df)} transactions with similar revenue (${revenue*0.5:,.0f} - ${revenue*2:,.0f})")
        except Exception as e:
            st.warning(f"Could not filter by revenue: {e}")
    
    # Sort by year (most recent first) and revenue similarity
    if not filtered_df.empty:
        try:
            sort_cols = []
            if year_col and year_col in filtered_df.columns:
                sort_cols.append(year_col)
            if revenue_col and revenue_col in filtered_df.columns and revenue > 0:
                filtered_df['revenue_diff'] = abs(filtered_df[revenue_col] - revenue)
                sort_cols.append('revenue_diff')
            
            if sort_cols:
                filtered_df = filtered_df.sort_values(sort_cols, ascending=[False] * len(sort_cols))
                if 'revenue_diff' in filtered_df.columns:
                    filtered_df = filtered_df.drop('revenue_diff', axis=1)
        except Exception as e:
            st.warning(f"Could not sort results: {e}")
    
    # Limit results
    filtered_df = filtered_df.head(max_results)
    
    # Convert to transaction format with CAD conversion
    transactions = []
    
    for _, row in filtered_df.iterrows():
        try:
            trans = {
                "naics": str(row.get(naics_col, '')) if naics_col else '',
                "revenue": int(float(row.get(revenue_col, 0)) * usd_to_cad) if revenue_col and pd.notna(row.get(revenue_col)) else 0,
                "sde": int(float(row.get(sde_col, 0)) * usd_to_cad) if sde_col and pd.notna(row.get(sde_col)) else 0,
                "adj_ebitda": int(float(row.get(ebitda_col, 0)) * usd_to_cad) if ebitda_col and pd.notna(row.get(ebitda_col)) else 0,
                "price": int(float(row.get(price_col, 0)) * usd_to_cad) if price_col and pd.notna(row.get(price_col)) else 0,
                "rev_mult": round(float(row.get(rev_mult_col, 0)), 2) if rev_mult_col and pd.notna(row.get(rev_mult_col)) else 0,
                "sde_mult": round(float(row.get(sde_mult_col, 0)), 2) if sde_mult_col and pd.notna(row.get(sde_mult_col)) else 0,
                "ebitda_mult": round(float(row.get(ebitda_mult_col, 0)), 2) if ebitda_mult_col and pd.notna(row.get(ebitda_mult_col)) else 0
            }
            
            # Calculate missing multiples if we have the data
            if trans["price"] > 0:
                if trans["rev_mult"] == 0 and trans["revenue"] > 0:
                    trans["rev_mult"] = round(trans["price"] / trans["revenue"], 2)
                if trans["sde_mult"] == 0 and trans["sde"] > 0:
                    trans["sde_mult"] = round(trans["price"] / trans["sde"], 2)
                if trans["ebitda_mult"] == 0 and trans["adj_ebitda"] > 0:
                    trans["ebitda_mult"] = round(trans["price"] / trans["adj_ebitda"], 2)
            
            transactions.append(trans)
        except Exception as e:
            continue
    
    if not transactions:
        # Return sample data if no matches found
        st.warning("Could not convert transactions to proper format. Using sample data.")
        return generate_sample_comparables(revenue, usd_to_cad)
    
    st.success(f"✅ Successfully loaded {len(transactions)} comparable transactions from PeerComps dataset")
    return transactions

def generate_sample_comparables(revenue, usd_to_cad=1.40):
    """Generate sample comparable transactions if dataset is unavailable"""
    base_revenue = revenue if revenue > 0 else 500000
    transactions = []
    
    for i in range(16):
        rev = base_revenue * (0.8 + i * 0.05)
        sde = rev * (0.15 + i * 0.01)
        ebitda = sde * 0.6
        price = rev * (0.73 + i * 0.01)
        
        trans = {
            "naics": "311999",
            "revenue": int(rev),
            "sde": int(sde),
            "adj_ebitda": int(ebitda),
            "price": int(price),
            "rev_mult": round(price / rev, 2),
            "sde_mult": round(price / sde, 2),
            "ebitda_mult": round(price / ebitda, 2)
        }
        transactions.append(trans)
    
    return transactions

# Required financial row items
REQUIRED_FINANCIAL_ITEMS = [
    "Total Revenue",
    "Total Cost of Goods Sold",
    "Total Operating Expenses",
    "Other Income"
]

REQUIRED_NORMALIZATION_ITEMS = [
    "Amortization",
    "Interest on Capital Lease/Equipment",
    "Owner/Management Salary",
    "Discretionary Expenses",
    "Replacement Manager Salary"
]

# Helper function to convert score to text answer
def score_to_answer(score, question_type):
    """Convert numeric score (1-5) to text answer"""
    answers = {
        'yes_no': {1: 'No', 2: 'Rarely', 3: 'Sometimes', 4: 'Usually', 5: 'Yes'},
        'percentage_low': {1: 'Over 50\\%', 2: '31-50\\%', 3: '16-30\\%', 4: '6-15\\%', 5: 'Under 5\\%'},
        'percentage_high': {1: 'Under 1\\%', 2: '1-5\\%', 3: '6-10\\%', 4: '11-20\\%', 5: 'Over 20\\%'},
        'percentage_reverse': {1: '0\\%', 2: '1-10\\%', 3: '11-25\\%', 4: '26-50\\%', 5: 'Over 50\\%'},
        'ease': {1: "No - It's me and irreplaceable", 2: 'Very difficult', 3: 'Somewhat difficult', 4: 'Possible with training', 5: 'Yes - Easily replaceable'},
        'revenue_model': {1: 'Transactional/walk-in only', 2: 'Some repeat customers', 3: 'Mix of recurring and transactional', 4: 'Mostly recurring revenue', 5: 'High recurring revenue contracts'}
    }
    return answers[question_type].get(score, str(score))

# Initialize session state for default Harry's Honey data
if 'financial_data' not in st.session_state:
    st.session_state.financial_data = pd.DataFrame({
        'Year': ['2020', '2021', '2022', '2023', '2024', '2025'],
        'Revenue': [450000, 520000, 585000, 650000, 710000, 780000],
        'Cost of Goods': [180000, 208000, 234000, 260000, 284000, 312000],
        'Total Expenses': [135000, 145000, 155000, 165000, 175000, 185000],
        'Other Income': [0, 0, 5000, 0, 0, 0]
    })

if 'normalization_data' not in st.session_state:
    st.session_state.normalization_data = pd.DataFrame({
        'Year': ['2020', '2021', '2022', '2023', '2024', '2025'],
        'Amortization': [25000, 28000, 30000, 32000, 34000, 36000],
        'Interest (Capital Lease)': [8000, 7500, 7000, 6500, 6000, 5500],
        'Management Salary': [0, 0, 0, 0, 0, 85000],
        'Discretionary Expense': [0, 0, 0, 0, 0, 0],
        'Manager Salary': [60000, 62000, 64000, 66000, 68000, 70000],
        'Year Weighting (%)': [0, 0, 10, 20, 30, 40]
    })

if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

if 'row_mapping' not in st.session_state:
    st.session_state.row_mapping = {}

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
        company_name = st.text_input("Company Name", value="Harry's Honey")
        
        # NAICS Code Selection - Simplified to Sector and Subsector only
        st.subheader("NAICS Industry Code")
        
        # Level 1: Sector
        sector = st.selectbox(
            "Select Industry Sector",
            options=list(NAICS_CODES.keys()),
            format_func=lambda x: f"{x} - {NAICS_CODES[x]}",
            index=4  # Manufacturing
        )
        
        # Level 2: Subsector (final level)
        naics_full_code = sector
        naics_description = NAICS_CODES[sector]
        
        if sector in NAICS_SUBCODES:
            subsector_options = list(NAICS_SUBCODES[sector].keys())
            subsector = st.selectbox(
                "Select Subsector",
                options=subsector_options,
                format_func=lambda x: f"{x} - {NAICS_SUBCODES[sector][x]}"
            )
            naics_full_code = subsector
            naics_description = NAICS_SUBCODES[sector][subsector]
        
        st.info(f"**Selected NAICS Code:** {naics_full_code} - {naics_description}")
    
    with col2:
        report_date = st.date_input("Report Date", value=datetime.today())
        
    st.divider()
    
    st.subheader("Industry Benchmarks")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sample_size = st.number_input("Sample Size", value=10, step=1)
        cost_of_goods_avg = st.number_input("Cost of Goods Avg (%)", value=40.0, step=0.01)
    
    with col2:
        total_expenses_avg = st.number_input("Total Expenses Avg (%)", value=30.0, step=0.01)
        total_employment_costs_avg = st.number_input("Employment Costs Avg (%)", value=25.0, step=0.01)
    
    with col3:
        your_cost_of_goods = st.number_input("Your Cost of Goods (%)", value=40.0, step=0.01)
        your_total_expenses = st.number_input("Your Total Expenses (%)", value=28.5, step=0.01)
        your_employment_costs = st.number_input("Your Employment Costs (%)", value=0.0, step=0.01)

# ==================== TAB 2: FINANCIAL DATA ====================
with tab2:
    st.header("Financial Data")
    
    # File upload option
    st.subheader("📁 Upload Financial Data (Optional)")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload CSV or Excel file with financial data", type=['csv', 'xlsx'])
    with col2:
        st.markdown("**Required Items:**")
        for item in REQUIRED_FINANCIAL_ITEMS:
            st.markdown(f"• {item}")
    
    if uploaded_file is not None:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df_uploaded = pd.read_csv(uploaded_file)
            else:
                df_uploaded = pd.read_excel(uploaded_file)
            
            st.session_state.uploaded_data = df_uploaded
            st.success("✅ File uploaded successfully!")
            
            # Show preview
            with st.expander("📊 Preview Uploaded Data"):
                st.dataframe(df_uploaded.head(10), use_container_width=True)
            
            st.divider()
            
            # Map columns using fuzzy matching
            st.subheader("🔗 Map Your Data to Required Fields")
            st.markdown("*We've attempted to automatically match your columns. Please verify and adjust as needed.*")
            
            # Get all potential row/column names from uploaded data
            if 'Year' in df_uploaded.columns or 'year' in df_uploaded.columns:
                # Data is in columns (years as columns)
                available_items = [col for col in df_uploaded.columns if col.lower() not in ['year', 'item', 'category']]
                is_transposed = False
            else:
                # Data is in rows (years as rows)
                if len(df_uploaded.columns) > 1:
                    available_items = df_uploaded.iloc[:, 0].tolist()
                    is_transposed = True
                else:
                    st.error("Could not determine data structure. Please ensure your file has year columns or a description column.")
                    available_items = []
            
            # Create mapping interface for financial items
            st.markdown("**Income Statement Items:**")
            financial_mapping = {}
            
            for required_item in REQUIRED_FINANCIAL_ITEMS:
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**{required_item}**")
                
                with col2:
                    # Try fuzzy matching
                    if available_items:
                        matches = process.extract(required_item, available_items, scorer=fuzz.token_sort_ratio, limit=3)
                        best_match = matches[0][0] if matches and matches[0][1] > 60 else None
                        
                        default_index = available_items.index(best_match) if best_match in available_items else 0
                    else:
                        default_index = 0
                    
                    selected = st.selectbox(
                        "Map to:",
                        options=["[None - Fill with 0]"] + available_items,
                        index=default_index + 1 if available_items and best_match else 0,
                        key=f"map_fin_{required_item}"
                    )
                    
                    financial_mapping[required_item] = None if selected == "[None - Fill with 0]" else selected
                
                with col3:
                    if financial_mapping[required_item] is None:
                        st.warning("⚠️")
            
            st.divider()
            
            # Normalization items
            st.markdown("**Normalization Items:**")
            normalization_mapping = {}
            
            for required_item in REQUIRED_NORMALIZATION_ITEMS:
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**{required_item}**")
                
                with col2:
                    # Try fuzzy matching
                    if available_items:
                        matches = process.extract(required_item, available_items, scorer=fuzz.token_sort_ratio, limit=3)
                        best_match = matches[0][0] if matches and matches[0][1] > 60 else None
                        
                        default_index = available_items.index(best_match) if best_match in available_items else 0
                    else:
                        default_index = 0
                    
                    selected = st.selectbox(
                        "Map to:",
                        options=["[None - Fill with 0]"] + available_items,
                        index=default_index + 1 if available_items and best_match else 0,
                        key=f"map_norm_{required_item}"
                    )
                    
                    normalization_mapping[required_item] = None if selected == "[None - Fill with 0]" else selected
                
                with col3:
                    if normalization_mapping[required_item] is None:
                        st.warning("⚠️")
            
            st.divider()
            
            # Process button
            if st.button("✨ Process Uploaded Data", type="primary", use_container_width=True):
                # Extract years and create new dataframes
                if is_transposed:
                    # Years are in rows
                    year_col_idx = next((i for i, col in enumerate(df_uploaded.columns) if 'year' in col.lower()), 0)
                    years = df_uploaded.iloc[:, year_col_idx].tolist()
                    
                    # Extract financial data
                    revenue_vals = []
                    cogs_vals = []
                    expenses_vals = []
                    other_income_vals = []
                    
                    for item, mapped in financial_mapping.items():
                        if mapped:
                            row_idx = available_items.index(mapped)
                            values = df_uploaded.iloc[row_idx, 1:].tolist()
                        else:
                            values = [0] * len(years)
                        
                        if "Revenue" in item:
                            revenue_vals = values
                        elif "Cost" in item:
                            cogs_vals = values
                        elif "Expenses" in item:
                            expenses_vals = values
                        elif "Other Income" in item:
                            other_income_vals = values
                else:
                    # Years are in columns
                    year_cols = [col for col in df_uploaded.columns if str(col).isdigit() or 'year' in str(col).lower()]
                    years = year_cols
                    
                    # This structure needs more complex handling - simplified for now
                    st.error("Column-based year format not fully implemented. Please transpose your data so years are rows.")
                    revenue_vals = [0] * len(years)
                    cogs_vals = [0] * len(years)
                    expenses_vals = [0] * len(years)
                    other_income_vals = [0] * len(years)
                
                # Calculate projection year
                if len(years) >= 2:
                    # Calculate average growth rate
                    numeric_revenues = [float(x) for x in revenue_vals if str(x).replace('.', '').replace('-', '').isdigit()]
                    if len(numeric_revenues) >= 2:
                        growth_rates = [(numeric_revenues[i] - numeric_revenues[i-1]) / numeric_revenues[i-1] 
                                      for i in range(1, len(numeric_revenues))]
                        avg_growth = sum(growth_rates) / len(growth_rates)
                        
                        # Project next year
                        last_year = int(years[-1]) if str(years[-1]).isdigit() else 2026
                        proj_year = last_year + 1
                        
                        proj_revenue = numeric_revenues[-1] * (1 + avg_growth)
                        proj_cogs = (float(cogs_vals[-1]) * (1 + avg_growth) if cogs_vals[-1] else 0)
                        proj_expenses = (float(expenses_vals[-1]) * (1 + avg_growth) if expenses_vals[-1] else 0)
                        proj_other = 0
                        
                        years.append(str(proj_year))
                        revenue_vals.append(proj_revenue)
                        cogs_vals.append(proj_cogs)
                        expenses_vals.append(proj_expenses)
                        other_income_vals.append(proj_other)
                
                # Create new dataframes
                st.session_state.financial_data = pd.DataFrame({
                    'Year': [str(y) for y in years],
                    'Revenue': revenue_vals,
                    'Cost of Goods': cogs_vals,
                    'Total Expenses': expenses_vals,
                    'Other Income': other_income_vals
                })
                
                # Process normalizations similarly
                amort_vals = []
                interest_vals = []
                mgmt_salary_vals = []
                discr_exp_vals = []
                mgr_salary_vals = []
                
                for item, mapped in normalization_mapping.items():
                    if mapped and is_transposed:
                        row_idx = available_items.index(mapped)
                        values = df_uploaded.iloc[row_idx, 1:len(years)+1].tolist()
                    else:
                        values = [0] * len(years)
                    
                    if "Amortization" in item:
                        amort_vals = values
                    elif "Interest" in item:
                        interest_vals = values
                    elif "Owner" in item or "Management Salary" in item:
                        mgmt_salary_vals = values
                    elif "Discretionary" in item:
                        discr_exp_vals = values
                    elif "Replacement" in item or "Manager Salary" in item:
                        mgr_salary_vals = values
                
                # Create weighting (most recent years get more weight)
                total_years = len(years)
                if total_years <= 3:
                    weightings = [100 // total_years] * total_years
                else:
                    # Last year gets most weight
                    weightings = [0] * (total_years - 3) + [20, 30, 50]
                
                st.session_state.normalization_data = pd.DataFrame({
                    'Year': [str(y) for y in years],
                    'Amortization': amort_vals,
                    'Interest (Capital Lease)': interest_vals,
                    'Management Salary': mgmt_salary_vals,
                    'Discretionary Expense': discr_exp_vals,
                    'Manager Salary': mgr_salary_vals,
                    'Year Weighting (%)': weightings
                })
                
                st.success("✅ Data processed successfully! Scroll down to review and edit.")
                st.rerun()
        
        except Exception as e:
            st.error(f"Error reading file: {e}")
            import traceback
            st.code(traceback.format_exc())
    
    st.divider()
    
    # Financial Data Table
    st.subheader("Income Statement Data")
    st.markdown("*Edit the table directly. Gross Profit and Net Income will be calculated automatically.*")
    
    # Add delete year functionality
    col1, col2 = st.columns([3, 1])
    with col2:
        years_to_delete = st.multiselect(
            "Delete Years:",
            options=st.session_state.financial_data['Year'].tolist(),
            key="delete_years"
        )
        if st.button("🗑️ Delete Selected Years") and years_to_delete:
            st.session_state.financial_data = st.session_state.financial_data[
                ~st.session_state.financial_data['Year'].isin(years_to_delete)
            ].reset_index(drop=True)
            st.session_state.normalization_data = st.session_state.normalization_data[
                ~st.session_state.normalization_data['Year'].isin(years_to_delete)
            ].reset_index(drop=True)
            st.rerun()
    
    edited_financial = st.data_editor(
        st.session_state.financial_data,
        use_container_width=True,
        num_rows="dynamic",
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
        num_rows="dynamic",
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
            1, 5, 3,
            help="1 = No, 5 = Yes, certified accountant"
        )
        st.caption(f"Answer: {score_to_answer(accountant, 'yes_no')}")
    
    with col2:
        annual_budget = st.slider(
            "Do you prepare an annual operating budget?",
            1, 5, 3,
            help="1 = No, 5 = Yes, detailed budget"
        )
        st.caption(f"Answer: {score_to_answer(annual_budget, 'yes_no')}")
        
        payables_on_time = st.slider(
            "Are your payables always paid in full and on-time?",
            1, 5, 3,
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
            1, 5, 3,
            help="1 = Would collapse, 5 = Would thrive"
        )
        st.caption(f"Answer: {score_to_answer(thrive_without_owner, 'yes_no')}")
        
        vacation_over_month = st.slider(
            "Have you taken a vacation longer than 1 month in the past 2 years?",
            1, 5, 3,
            help="1 = No, 5 = Yes, multiple times"
        )
        st.caption(f"Answer: {score_to_answer(vacation_over_month, 'yes_no')}")
    
    with col2:
        customers_ask_by_name = st.slider(
            "What percentage of customers ask for you by name?",
            1, 5, 3,
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
            1, 5, 3,
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
        1, 5, 3,
        help="1 = Transactional/walk-in only, 5 = High recurring revenue contracts"
    )
    st.caption(f"Answer: {score_to_answer(revenue_model, 'revenue_model')}")
    
    st.divider()
    
    # Organizational Stability
    st.subheader("🛡️ Organizational Stability")
    st.markdown("**Weight: 3.75% of valuation**")
    
    col1, col2 = st.columns(2)
    with col1:
        largest_customer = st.slider(
            "How much revenue does your largest customer represent?",
            1, 5, 3,
            help="1 = >25%, 5 = <5%"
        )
        st.caption(f"Answer: {score_to_answer(largest_customer, 'percentage_low')}")
        
        top_5_customers = st.slider(
            "How much revenue do your top 5 customers represent?",
            1, 5, 3,
            help="1 = >50%, 5 = <10%"
        )
        st.caption(f"Answer: {score_to_answer(top_5_customers, 'percentage_low')}")
        
        replace_sales_person = st.slider(
            "Could you easily replace the person most responsible for sales?",
            1, 5, 3,
            help="1 = It's me and irreplaceable, 5 = Easily replaceable"
        )
        st.caption(f"Answer: {score_to_answer(replace_sales_person, 'ease')}")
    
    with col2:
        replace_delivery_person = st.slider(
            "Could you easily replace the person most responsible for delivery?",
            1, 5, 3,
            help="1 = It's me and irreplaceable, 5 = Easily replaceable"
        )
        st.caption(f"Answer: {score_to_answer(replace_delivery_person, 'ease')}")
        
        replace_supplier = st.slider(
            "Could you easily replace your most important supplier?",
            1, 5, 3,
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
            1, 5, 3,
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
            1, 5, 3,
            help="1 = No, 5 = Yes, top result"
        )
        st.caption(f"Answer: {score_to_answer(google_first_page, 'yes_no')}")
        
        written_acquisition_strategy = st.slider(
            "Do you have a written customer acquisition strategy?",
            1, 5, 3,
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
    
    # Calculate weighted averages using the weighting column
    weightings = norm_data['Year Weighting (%)'].tolist()
    total_weight = sum(weightings)
    
    if total_weight > 0:
        weighted_avg_revenue = sum(fin_data['Revenue'].tolist()[i] * weightings[i] / 100 for i in range(len(weightings)))
        weighted_avg_sde = sum(sde_values[i] * weightings[i] / 100 for i in range(len(weightings)))
    else:
        weighted_avg_revenue = fin_data['Revenue'].iloc[-1]
        weighted_avg_sde = sde_values[-1]
    
    # Get comparable transactions from PeerComps dataset
    USD_TO_CAD = 1.40
    transactions = find_comparable_transactions(
        naics_code=naics_full_code,
        revenue=weighted_avg_revenue,
        year_range=5,
        max_results=20,
        usd_to_cad=USD_TO_CAD
    )
    
    # Calculate valuation multiples from comparables
    if transactions:
        revenue_multiples = [t['rev_mult'] for t in transactions if t['rev_mult'] > 0]
        sde_multiples = [t['sde_mult'] for t in transactions if t['sde_mult'] > 0 and t['sde_mult'] < 10]
        ebitda_multiples = [t['ebitda_mult'] for t in transactions if t['ebitda_mult'] > 0 and t['ebitda_mult'] < 15]
        
        revenue_multiple = round(sum(revenue_multiples) / len(revenue_multiples), 2) if revenue_multiples else 0.84
        sde_multiple = round(sum(sde_multiples) / len(sde_multiples), 2) if sde_multiples else 3.7
        adj_ebitda_multiple = round(sum(ebitda_multiples) / len(ebitda_multiples), 2) if ebitda_multiples else 4.45
    else:
        revenue_multiple = 0.84
        sde_multiple = 3.7
        adj_ebitda_multiple = 4.45
    
    mpsp = int(weighted_avg_revenue * revenue_multiple)
    
    # Calculate revenue range from comparables
    if transactions:
        revenues = [t['revenue'] for t in transactions]
        revenue_range = [min(revenues), max(revenues)]
    else:
        revenue_range = [int(weighted_avg_revenue * 0.5), int(weighted_avg_revenue * 1.5)]
    
    # Calculate scorecard adjustments
    def calculate_section_adjustment(scores, weight):
        avg_score = sum(scores) / len(scores)
        adjustment_pct = ((avg_score - 3) / 2) * weight
        return adjustment_pct
    
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
            "naics_code": f"{naics_full_code} - {naics_description}",
            "report_date": report_date.strftime("%B %d, %Y")
        },
        "valuation": {
            "mpsp": adjusted_mpsp,
            "base_mpsp": mpsp,
            "revenue_multiple": revenue_multiple,
            "sde_multiple": sde_multiple,
            "adj_ebitda_multiple": adj_ebitda_multiple,
            "weighted_avg_revenue": int(weighted_avg_revenue),
            "weighted_avg_sde": int(weighted_avg_sde),
            "usd_to_cad_rate": USD_TO_CAD
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
            "count": len(transactions),
            "revenue_range": revenue_range,
            "transactions": transactions
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
        st.metric("Comparable Transactions", len(transactions))
    with col3:
        st.metric("Weighted Avg SDE", f"${weighted_avg_sde:,.0f}")
        st.metric("Revenue Multiple", f"{revenue_multiple}x")
    
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
    
    # Comparables preview
    st.subheader("📋 Comparable Transactions Preview")
    
    if transactions and len(transactions) > 0 and 'naics' in transactions[0]:
        # Check if we're using real data or sample data
        is_sample_data = all(t.get('naics', '') == "311999" for t in transactions)
        
        if is_sample_data:
            st.warning(f"⚠️ Showing {len(transactions)} sample transactions (PeerComps data not available or no matches found)")
        else:
            st.success(f"✅ Found {len(transactions)} real comparable transactions from PeerComps dataset")
            st.info(f"Amounts converted from USD to CAD at rate of {USD_TO_CAD}")
    
    if transactions:
        trans_df = pd.DataFrame(transactions[:10])  # Show first 10
        st.dataframe(trans_df, use_container_width=True)
    else:
        st.error("No comparable transactions available")
    
    st.divider()
    
    # JSON preview
    with st.expander("📄 Preview JSON Output"):
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
    
    1. **Company Info**: 
       - Enter company name
       - Select NAICS code from hierarchical menus
       - Adjust industry benchmarks
    
    2. **Financial Data**: 
       - Upload CSV/Excel or use default data
       - Map uploaded columns to required fields
       - Edit tables directly
       - Delete unwanted years
    
    3. **Scorecard**: Rate qualitative factors (1-5)
       - 1 = Poor/Needs Improvement
       - 3 = Average/Neutral
       - 5 = Excellent/Best
    
    4. **Export**: 
       - Review summary and adjustments
       - Download JSON file
       - Generate PDF report
    
    ### PeerComps Integration
    
    The app automatically searches the PeerComps dataset for comparable transactions based on:
    - NAICS code match (6, 5, 4, or 3 digit)
    - Similar revenue (50%-200% of your business)
    - Recent years (last 5 years)
    - USD amounts converted to CAD at 1.40
    
    ### Generate Report
    ```bash
    python generate_report.py your_file.json
    pdflatex valuation_report.tex
    ```
    
    ### Dependencies
    ```bash
    pip install streamlit pandas rapidfuzz openpyxl
    ```
    """)
    
    st.divider()
    
    # Show dataset status
    df = load_peercomps()
    if df is not None:
        st.success(f"✅ PeerComps dataset loaded ({len(df):,} transactions)")
        
        with st.expander("📊 Dataset Information"):
            st.markdown("**Available Columns:**")
            cols_list = ", ".join(df.columns.tolist())
            st.text(cols_list)
            
            # Show column detection results
            st.markdown("**Detected Key Columns:**")
            naics_col = find_column(df, ['NAICS Code', 'NAICS', 'naics_code'])
            year_col = find_column(df, ['Year', 'year', 'Transaction Year'])
            revenue_col = find_column(df, ['Revenue', 'revenue', 'Sales'])
            price_col = find_column(df, ['Sale Price', 'Price', 'price'])
            
            col_status = []
            col_status.append(f"✅ NAICS: {naics_col}" if naics_col else "❌ NAICS: Not found")
            col_status.append(f"✅ Year: {year_col}" if year_col else "❌ Year: Not found")
            col_status.append(f"✅ Revenue: {revenue_col}" if revenue_col else "❌ Revenue: Not found")
            col_status.append(f"✅ Price: {price_col}" if price_col else "❌ Price: Not found")
            
            for status in col_status:
                st.text(status)
            
            # Show sample data
            st.markdown("**Sample Data (first 5 rows):**")
            st.dataframe(df.head(5), use_container_width=True)
            
            # Test button
            if st.button("🧪 Test Dataset Search"):
                st.markdown("**Testing search for Manufacturing (NAICS 311999)...**")
                test_transactions = find_comparable_transactions(
                    naics_code="311999",
                    revenue=500000,
                    year_range=5,
                    max_results=10,
                    usd_to_cad=1.40
                )
                if test_transactions:
                    st.success(f"Found {len(test_transactions)} test transactions!")
                    st.dataframe(pd.DataFrame(test_transactions[:5]))
                else:
                    st.error("No transactions found in test search")
    else:
        st.warning("⚠️ PeerComps dataset not found. Using sample data.")
        st.info("Place 'PeerComps_dataset.xlsx' in the same directory as this app to use real data.")