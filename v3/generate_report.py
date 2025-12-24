# #!/usr/bin/env python3
# """
# Valuation Report Generator
# Creates a professional business valuation report from JSON data
# """

# import json
# import os
# import sys
# from pathlib import Path


# def format_currency(value):
#     """Format number as currency with $ and commas"""
#     return f"\\${value:,.0f}"


# def format_percent(value):
#     """Format number as percentage"""
#     return f"{value:.2f}\\%"


# def calculate_gross_profit_percent(gross_profit, revenue):
#     """Calculate gross profit percentage"""
#     if revenue == 0:
#         return 0
#     return (gross_profit / revenue) * 100


# def calculate_net_income_percent(net_income, revenue):
#     """Calculate net income percentage"""
#     if revenue == 0:
#         return 0
#     return (net_income / revenue) * 100


# def generate_latex(data):
#     """Generate complete LaTeX document from data"""
    
#     # Extract commonly used values
#     company_name = data['company']['name']
#     report_date = data['company']['report_date']
#     mpsp = data['valuation']['mpsp']
#     naics = data['company']['naics_code']
    
#     # Calculate scorecard ranges
#     min_val = data['scorecard']['minimum_valuation']
#     max_val = data['scorecard']['optimized_valuation']
    
#     # Calculate section ranges
#     sections_range = {}
#     for section_name, section_data in data['scorecard']['sections'].items():
#         weight = section_data['weight']
#         range_amount = int(mpsp * weight / 100)
#         sections_range[section_name] = range_amount
    
#     # Start building LaTeX
#     latex = r'''\documentclass[11pt,letterpaper]{article}
# \usepackage[letterpaper,margin=1in,top=1in,bottom=1in]{geometry}
# \usepackage{graphicx}
# \usepackage{xcolor}
# \usepackage{array}
# \usepackage{longtable}
# \usepackage{booktabs}
# \usepackage{multirow}
# \usepackage{colortbl}
# \usepackage{fancyhdr}
# \usepackage{lastpage}
# \usepackage{tocloft}
# \usepackage{titlesec}
# \usepackage{enumitem}
# \usepackage{amsmath}
# \usepackage[hidelinks]{hyperref}

# % Define colors
# \definecolor{primaryblue}{RGB}{41,128,185}
# \definecolor{lightgray}{RGB}{240,240,240}
# \definecolor{darkgray}{RGB}{100,100,100}
# \definecolor{tableheader}{RGB}{52,152,219}
# \definecolor{tableodd}{RGB}{235,245,251}

# % Header and footer
# \pagestyle{fancy}
# \fancyhf{}
# \fancyhead[L]{\small Most Probable Selling Price Report}
# \fancyhead[R]{\small ''' + company_name + r'''}
# \fancyfoot[L]{\small Chinook Business Advisory}
# \fancyfoot[R]{\small \thepage\ of \pageref{LastPage}}
# \renewcommand{\headrulewidth}{0.5pt}
# \renewcommand{\footrulewidth}{0.5pt}

# % Title formatting
# \titleformat{\section}
#   {\normalfont\Large\bfseries\color{primaryblue}}
#   {\thesection}{1em}{}
# \titleformat{\subsection}
#   {\normalfont\large\bfseries\color{primaryblue}}
#   {\thesubsection}{1em}{}

# % TOC formatting
# \renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}
# \setlength{\cftbeforesecskip}{8pt}

# % List formatting
# \setlist[itemize]{leftmargin=*,topsep=6pt,itemsep=3pt}

# \begin{document}

# % Title Page
# \begin{titlepage}
# \centering
# \vspace*{1cm}

# {\Huge\bfseries\color{primaryblue} Most Probable Selling Price Report\par}
# \vspace{1.5cm}

# {\LARGE\bfseries ''' + company_name + r'''\par}
# \vspace{1cm}

# {\Large ''' + report_date + r'''\par}
# \vspace{2cm}

# \includegraphics[width=0.4\textwidth]{Chinook_logo.png}

# \vfill

# {\large Chinook Business Advisory\par}

# \end{titlepage}

# % Table of Contents
# \tableofcontents
# \clearpage

# % Main Content
# \section*{Purpose \& Scope}
# \addcontentsline{toc}{section}{Purpose \& Scope}

# This report will provide an opinion of the Most Probable Selling Price (`MPSP') to the User, where the User is the Client or the agent or representative of the Client (the `User').

# This is the price for the enterprise (the `Business') and its assets if to be sold as a going concern. This price includes normal inventory but does not include any other components of working capital.

# The purpose of this report is to provide an opinion of the Business's MPSP. It is not intended to be a formal valuation of the business, enterprise, or the assets thereof. It is a limited assessment of the MPSP, which is defined by the International Business Brokers Association (IBBA) as, `that price for the assets or shares intended for sale which represents the total consideration most likely to be established between a buyer and a seller considering compulsion on the part of either the buyer or the seller, and potential financial strategic or non-financial benefits to the seller and probable buyer'. This report is intended for the sole use of the User and specifically for the purpose cited herein; all others possessing this report are not intended users. The use of this report by anyone other than the intended person and for the intended purpose, is not authorized.

# \subsection*{Valuation Assumptions}

# The generation of this report relied upon:

# \begin{enumerate}[itemsep=3pt]
# \item A qualitative questionnaire completed by the user.
# \item The Income Statements and/or Balance Sheets provided by the user.
# \item Comparable transaction data.
# \end{enumerate}

# \subsection*{General Assumptions}

# The following assumptions were made when preparing this report.

# \begin{enumerate}[itemsep=3pt]
# \item The Business is a sole proprietorship, legal partnership, or a corporation.
# \item The Business has no contingent liabilities, unusual contractual obligations, or substantial commitments, other than in the ordinary course of business.
# \item The Business has no litigation pending or threatened.
# \item Chinook Business Advisory did not audit or otherwise verify the financial information submitted.
# \end{enumerate}

# \clearpage

# \section*{Disclaimer}
# \addcontentsline{toc}{section}{Disclaimer}

# Chinook Business Advisory, does not warrant any information contained herein and is not responsible for any results whatsoever as a result of, or as a consequence of, using the information provided in this report. It is understood that market conditions are variable, business operations and the perceived risks associated with them are subject to change, and that the motivations of both Purchasers and Vendors may differ and result in an ultimate sale price either higher or lower than predicted in the report. The valuation of the business assets, goodwill and/or share value is not warranted in any way.

# The User has supplied the information contained in this report. Chinook Business Advisory has not audited or otherwise confirmed this information and makes no representations, expressed or implied, as to its accuracy or completeness or the conclusions to be drawn and shall in no way be responsible for the content, accuracy and truthfulness of such information.

# The information presented in this report is the result of the User's input, representations and calculations. Additional information, such as market data from reliable sources, will also be considered. The Report will contain information and conclusions deemed to be relevant to the User but is offered without any guarantees or warranties relating to specific statements or implied statements contained herein.

# An essential step in the review of a company is an analysis of its financial performance over time. Analyzing a company's financial statements provides an indication of historical growth, liquidity, leverage, and profitability, all of which influence the value of a company's assets or equity. The following section of this report examines the trend of the company's financial performance in the previous fiscal years.

# The subject company's historical income statements have been adjusted by the User to present the business as if it had been managed to maximize profitability. Since private companies tend to keep reported profits and resulting taxes as low as possible, adjusting the financial statements is an important element to understanding the true earning capacity of the business.

# Adjustments include any fringe benefits the owner may have had, unusual circumstances, liens that will be paid off, as well as the standard adjustments used to determine Adjusted EBITDA (Earnings before Interest, Taxes, Depreciation, and Amortization). This will reflect a more realistic income for a new owner and allow a prospective purchaser to compare ``apples to apples''.

# This adjusted profit is known as SDE (Seller's Discretionary Earnings). SDE could be defined as the total financial benefit available to a single person who owns and is fully employed in the operation of the business. Put another way, Adj. EBITDA = SDE minus a manager's salary. Analysis of the subject Company is based on the adjusted totals. A summary of the adjusted historical financial statements is contained in the following section.

# Chinook Business Advisory does not audit or review the financial statements of the subject company nor any of the adjustments made by the User and bears no responsibility for the use of this report.

# \clearpage

# \section*{Valuation}
# \addcontentsline{toc}{section}{Valuation}

# \vspace{1cm}

# \noindent
# Based on the information provided, the report has determined the Most Probable Selling Price (MPSP) for ''' + company_name + r''' to be:

# \begin{center}
# {\Huge\bfseries\color{primaryblue} ''' + format_currency(mpsp) + r'''}
# \end{center}

# \vspace{1cm}

# \subsection*{Valuation Multiples}

# This price was determined using a market-based approach which examined ''' + str(data['comparable_transactions']['count']) + r''' comparable transactions. These transactions included businesses with revenues between ''' + format_currency(data['comparable_transactions']['revenue_range'][0]) + r''' and ''' + format_currency(data['comparable_transactions']['revenue_range'][1]) + r'''. An asking price of ''' + format_currency(mpsp) + r''' represents the following valuation multiples:

# \vspace{0.5cm}

# \begin{center}
# \begin{tabular}{>{\raggedright}p{4cm}r}
# \rowcolor{tableheader}
# \textcolor{white}{\textbf{Valuation Metric}} & \textcolor{white}{\textbf{Multiple}} \\
# \rowcolor{tableodd}
# Revenue & ''' + str(data['valuation']['revenue_multiple']) + r''' \\
# \rowcolor{white}
# SDE & ''' + str(data['valuation']['sde_multiple']) + r''' \\
# \rowcolor{tableodd}
# Adj. EBITDA & ''' + str(data['valuation']['adj_ebitda_multiple']) + r''' \\
# \end{tabular}
# \end{center}

# \vspace{0.5cm}

# See Appendix A for comparable transactions.

# \clearpage
# '''

#     # Company Overview Section
#     fin_data = data['financial_data']
#     years = fin_data['years']
    
#     # Calculate gross profit percentages
#     gp_pcts = []
#     for i in range(len(years)):
#         gp_pct = calculate_gross_profit_percent(fin_data['gross_profit'][i], fin_data['revenue'][i])
#         gp_pcts.append(gp_pct)
    
#     # Calculate net income percentages
#     ni_pcts = []
#     for i in range(len(years)):
#         ni_pct = calculate_net_income_percent(fin_data['net_income'][i], fin_data['revenue'][i])
#         ni_pcts.append(ni_pct)
    
#     norm = data['normalizations']
    
#     latex += r'''\section*{Company Overview}
# \addcontentsline{toc}{section}{Company Overview}

# \begin{tabular}{ll}
# \textbf{Name of Business:} & ''' + company_name + r''' \\
# \textbf{NAICS Industry Code:} & ''' + naics + r''' \\
# \textbf{MPSP:} & ''' + format_currency(mpsp) + r''' \\
# \end{tabular}

# \vspace{0.5cm}

# \begin{center}
# \small
# \begin{tabular}{lrrrrr}
# \rowcolor{tableheader}
# \textcolor{white}{} & \textcolor{white}{\textbf{''' + years[4] + r'''}} & \textcolor{white}{\textbf{''' + years[3] + r'''}} & \textcolor{white}{\textbf{''' + years[2] + r'''}} & \textcolor{white}{\textbf{''' + years[1] + r'''}} & \textcolor{white}{\textbf{''' + years[0] + r'''}} \\
# \rowcolor{tableodd}
# \textbf{Total Revenue} & ''' + format_currency(fin_data['revenue'][4]) + r''' & ''' + format_currency(fin_data['revenue'][3]) + r''' & ''' + format_currency(fin_data['revenue'][2]) + r''' & ''' + format_currency(fin_data['revenue'][1]) + r''' & ''' + format_currency(fin_data['revenue'][0]) + r''' \\
# \rowcolor{white}
# \textbf{Total Cost of Goods} & ''' + format_currency(fin_data['cost_of_goods'][4]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][3]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][2]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][1]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][0]) + r''' \\
# \rowcolor{tableodd}
# \textbf{Gross Profit} & ''' + format_currency(fin_data['gross_profit'][4]) + r''' & ''' + format_currency(fin_data['gross_profit'][3]) + r''' & ''' + format_currency(fin_data['gross_profit'][2]) + r''' & ''' + format_currency(fin_data['gross_profit'][1]) + r''' & ''' + format_currency(fin_data['gross_profit'][0]) + r''' \\
# \rowcolor{white}
# \textbf{Total Expenses} & ''' + format_currency(fin_data['total_expenses'][4]) + r''' & ''' + format_currency(fin_data['total_expenses'][3]) + r''' & ''' + format_currency(fin_data['total_expenses'][2]) + r''' & ''' + format_currency(fin_data['total_expenses'][1]) + r''' & ''' + format_currency(fin_data['total_expenses'][0]) + r''' \\
# \rowcolor{tableodd}
# \textbf{Net Income} & ''' + format_currency(fin_data['net_income'][4]) + r''' & ''' + format_currency(fin_data['net_income'][3]) + r''' & ''' + format_currency(fin_data['net_income'][2]) + r''' & ''' + format_currency(fin_data['net_income'][1]) + r''' & ''' + format_currency(fin_data['net_income'][0]) + r''' \\
# \rowcolor{white}
# \textbf{Total Normalizations} & ''' + format_currency(norm['total_adjustments'][4]) + r''' & ''' + format_currency(norm['total_adjustments'][3]) + r''' & ''' + format_currency(norm['total_adjustments'][2]) + r''' & ''' + format_currency(norm['total_adjustments'][1]) + r''' & ''' + format_currency(norm['total_adjustments'][0]) + r''' \\
# \rowcolor{tableodd}
# \textbf{SDE} & ''' + format_currency(norm['sde'][4]) + r''' & ''' + format_currency(norm['sde'][3]) + r''' & ''' + format_currency(norm['sde'][2]) + r''' & ''' + format_currency(norm['sde'][1]) + r''' & ''' + format_currency(norm['sde'][0]) + r''' \\
# \rowcolor{white}
# \textbf{Adj. EBITDA} & ''' + format_currency(norm['adj_ebitda'][4]) + r''' & ''' + format_currency(norm['adj_ebitda'][3]) + r''' & ''' + format_currency(norm['adj_ebitda'][2]) + r''' & ''' + format_currency(norm['adj_ebitda'][1]) + r''' & ''' + format_currency(norm['adj_ebitda'][0]) + r''' \\
# \rowcolor{tableodd}
# \textbf{Year Weighting} & ''' + str(norm['year_weighting'][4]) + r'''\% & ''' + str(norm['year_weighting'][3]) + r'''\% & ''' + str(norm['year_weighting'][2]) + r'''\% & ''' + str(norm['year_weighting'][1]) + r'''\% & ''' + str(norm['year_weighting'][0]) + r'''\% \\
# \end{tabular}
# \end{center}

# \vspace{0.5cm}

# \begin{tabular}{ll}
# \textbf{Weighted Average of Revenue} & ''' + format_currency(data['valuation']['weighted_avg_revenue']) + r''' \\
# \textbf{MPSP Multiple of Revenue} & ''' + str(data['valuation']['revenue_multiple']) + r''' \\
# \textbf{Weighted Average of SDE} & ''' + format_currency(data['valuation']['weighted_avg_sde']) + r''' \\
# \textbf{MPSP Multiple of SDE} & ''' + str(data['valuation']['sde_multiple']) + r''' \\
# \end{tabular}

# \vspace{0.3cm}

# \textit{\small Note: Projected year is calculated from the year to date statement from January 1 to September 30.}

# \clearpage
# '''

#     # Valuation Methodologies
#     latex += r'''\section*{Valuation Methodologies}
# \addcontentsline{toc}{section}{Valuation Methodologies}

# \subsection*{1. Earnings Based Approaches:}

# This method assesses the ability of the Company to produce earnings in the future. With this approach, a valuator uses the Company's operating history to determine its expected level of earnings and the likelihood of the earnings to continue in the future.

# These earnings are normalized for unusual revenue or non-operational expenses. A capitalization factor, often called a multiple, is then applied that reflects a reasonable rate of return based on the perceived risk associated with the continued profitability of the company.

# Within Earning Based Approaches there are several other methodologies used such as Discounted Cash Flow (DCF) where an average of the trend of predicted future earnings is used and divided by the capitalization factor.

# \subsection*{2. Asset Based Approaches:}

# Includes the book value of tangible assets on the balance sheet (inventory/supplies, fixed assets, and all intangible assets) minus liabilities. Simply, the money left over if the company was liquidated.

# The Asset Based Approach are often appropriate in the following situations:

# \begin{enumerate}[itemsep=3pt]
# \item The company is considering liquidating or going out of business
# \item The company has no earnings history
# \item The company's earnings cannot be reliably estimated
# \item The company depends heavily on competitive contracts and there is not a consistent, predictable customer base (e.g., construction companies)
# \item The company derives little or no value from labor or intangible assets (e.g., real estate or holding companies)
# \item A significant portion of the company's assets are composed of liquid assets or other investments (e.g., marketable securities, real estate, mineral rights)
# \end{enumerate}

# As such, the asset approach is for businesses where a large amount of the value is in its tangible assets. Or the business is not generating a high enough return on its assets to warrant ``excess earnings'' or ``goodwill''.

# \subsection*{3. Market Based Approaches:}

# The market-based approach studies recent sales of similar assets, making adjustments for the differences between them. This is similar to how the real estate industry uses ``market comps'' to determine a listing price.

# To find a Company's Most Probable Selling Price (MPSP), the report examines transaction data of businesses of a similar size and industry. The report then makes adjustments to the Company's value based on on the qualitative inputs of the the report User. These are factors such as client concentration, growth opportunities, management structure, etc.

# A market-based valuation represents a reasonable expectation of what the business might sell for in a free and open market based on similar business purchase and sale transactions.

# \clearpage

# \subsection*{Methodology}

# \textbf{Our transaction algorithm} examines a database of 40,000+ transactions to find comparable businesses that have been sold.

# The algorithm selects businesses that are similar in terms of NAICS code and annual revenues. The more businesses that have sold that are similar to yours, the more accurate the MPSP will be.

# \subsection*{The Science}

# Based on information you provide in the financial tables, the report then assigns your business a median business value. That means that if the report finds 15 businesses that were similar it would assign your business the middle value.

# \subsection*{The Art}

# The next part of the process involves taking the answers to the questions we ask and trying to determine if your business is more or less attractive than average.

# This report uses your answers to more accurately position your business on the chart. If your answers suggest that your business is a little better than the average in the dataset, the report will assign a higher Most Probable Selling Price to your business. Conversely, if there are opportunities to improve your business that haven't yet been acted on, the report will assign a lower MPSP.

# \clearpage
# '''

#     # Unadjusted Historical Income Statements
#     latex += r'''\section*{Unadjusted Historical Income Statements}
# \addcontentsline{toc}{section}{Unadjusted Historical Income Statements}

# \textit{Derived from accountant prepared financial statements}

# \vspace{0.5cm}

# \begin{center}
# \small
# \begin{tabular}{lrrrrr}
# \rowcolor{tableheader}
# \textcolor{white}{} & \textcolor{white}{\textbf{''' + years[4] + r'''}} & \textcolor{white}{\textbf{''' + years[3] + r'''}} & \textcolor{white}{\textbf{''' + years[2] + r'''}} & \textcolor{white}{\textbf{''' + years[1] + r'''}} & \textcolor{white}{\textbf{''' + years[0] + r'''}} \\
# \multicolumn{6}{l}{\textbf{Revenue}} \\
# \rowcolor{tableodd}
# Revenue & ''' + format_currency(fin_data['revenue'][4]) + r''' & ''' + format_currency(fin_data['revenue'][3]) + r''' & ''' + format_currency(fin_data['revenue'][2]) + r''' & ''' + format_currency(fin_data['revenue'][1]) + r''' & ''' + format_currency(fin_data['revenue'][0]) + r''' \\
# \rowcolor{white}
# \textbf{Total Revenue} & ''' + format_currency(fin_data['revenue'][4]) + r''' & ''' + format_currency(fin_data['revenue'][3]) + r''' & ''' + format_currency(fin_data['revenue'][2]) + r''' & ''' + format_currency(fin_data['revenue'][1]) + r''' & ''' + format_currency(fin_data['revenue'][0]) + r''' \\
# \multicolumn{6}{l}{\textbf{Cost of Goods}} \\
# \rowcolor{tableodd}
# Cost of Sales & ''' + format_currency(fin_data['cost_of_goods'][4]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][3]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][2]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][1]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][0]) + r''' \\
# \rowcolor{white}
# \textbf{Total Cost of Goods} & ''' + format_currency(fin_data['cost_of_goods'][4]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][3]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][2]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][1]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][0]) + r''' \\
# \rowcolor{tableodd}
# \textbf{Gross Profit} & ''' + format_currency(fin_data['gross_profit'][4]) + r''' & ''' + format_currency(fin_data['gross_profit'][3]) + r''' & ''' + format_currency(fin_data['gross_profit'][2]) + r''' & ''' + format_currency(fin_data['gross_profit'][1]) + r''' & ''' + format_currency(fin_data['gross_profit'][0]) + r''' \\
# \rowcolor{white}
# \textbf{Gross Profit \%} & ''' + format_percent(gp_pcts[4]) + r''' & ''' + format_percent(gp_pcts[3]) + r''' & ''' + format_percent(gp_pcts[2]) + r''' & ''' + format_percent(gp_pcts[1]) + r''' & ''' + format_percent(gp_pcts[0]) + r''' \\
# \multicolumn{6}{l}{\textbf{Expenses}} \\
# \rowcolor{tableodd}
# General Expense & ''' + format_currency(fin_data['total_expenses'][4]) + r''' & ''' + format_currency(fin_data['total_expenses'][3]) + r''' & ''' + format_currency(fin_data['total_expenses'][2]) + r''' & ''' + format_currency(fin_data['total_expenses'][1]) + r''' & ''' + format_currency(fin_data['total_expenses'][0]) + r''' \\
# \rowcolor{white}
# \textbf{Total Expenses} & ''' + format_currency(fin_data['total_expenses'][4]) + r''' & ''' + format_currency(fin_data['total_expenses'][3]) + r''' & ''' + format_currency(fin_data['total_expenses'][2]) + r''' & ''' + format_currency(fin_data['total_expenses'][1]) + r''' & ''' + format_currency(fin_data['total_expenses'][0]) + r''' \\
# \multicolumn{6}{l}{\textbf{Other Income}} \\
# \rowcolor{tableodd}
# - & \$- & \$- & ''' + format_currency(fin_data['other_income'][2]) + r''' & \$- & \$- \\
# \rowcolor{white}
# \textbf{Net Income} & ''' + format_currency(fin_data['net_income'][4]) + r''' & ''' + format_currency(fin_data['net_income'][3]) + r''' & ''' + format_currency(fin_data['net_income'][2]) + r''' & ''' + format_currency(fin_data['net_income'][1]) + r''' & ''' + format_currency(fin_data['net_income'][0]) + r''' \\
# \rowcolor{tableodd}
# \textbf{Net Income \%} & ''' + format_percent(ni_pcts[4]) + r''' & ''' + format_percent(ni_pcts[3]) + r''' & ''' + format_percent(ni_pcts[2]) + r''' & ''' + format_percent(ni_pcts[1]) + r''' & ''' + format_percent(ni_pcts[0]) + r''' \\
# \end{tabular}
# \end{center}

# \vspace{0.3cm}

# \textit{\small Note: Projected year is calculated from the year to date statement from January 1 to September 30.}

# \clearpage
# '''

#     # Normalization Summary
#     latex += r'''\section*{Normalization Summary}
# \addcontentsline{toc}{section}{Normalization Summary}

# \begin{center}
# \small
# \begin{tabular}{lrrrrrl}
# \rowcolor{tableheader}
# \textcolor{white}{} & \textcolor{white}{\textbf{''' + years[4] + r'''}} & \textcolor{white}{\textbf{''' + years[3] + r'''}} & \textcolor{white}{\textbf{''' + years[2] + r'''}} & \textcolor{white}{\textbf{''' + years[1] + r'''}} & \textcolor{white}{\textbf{''' + years[0] + r'''}} & \textcolor{white}{\textbf{Notes}} \\
# \rowcolor{tableodd}
# Net Income & ''' + format_currency(fin_data['net_income'][4]) + r''' & ''' + format_currency(fin_data['net_income'][3]) + r''' & ''' + format_currency(fin_data['net_income'][2]) + r''' & ''' + format_currency(fin_data['net_income'][1]) + r''' & ''' + format_currency(fin_data['net_income'][0]) + r''' & \\
# \rowcolor{white}
# Discretionary Expense & \$- & \$- & \$- & \$- & \$- & \\
# \rowcolor{tableodd}
# Amortization & ''' + format_currency(norm['amortization'][4]) + r''' & ''' + format_currency(norm['amortization'][3]) + r''' & ''' + format_currency(norm['amortization'][2]) + r''' & ''' + format_currency(norm['amortization'][1]) + r''' & ''' + format_currency(norm['amortization'][0]) + r''' & \\
# \rowcolor{white}
# Interest on Equipment under Capital Lease & ''' + format_currency(norm['interest_capital_lease'][4]) + r''' & ''' + format_currency(norm['interest_capital_lease'][3]) + r''' & ''' + format_currency(norm['interest_capital_lease'][2]) + r''' & ''' + format_currency(norm['interest_capital_lease'][1]) + r''' & ''' + format_currency(norm['interest_capital_lease'][0]) + r''' & \\
# \rowcolor{tableodd}
# Management Salary & ''' + format_currency(norm['management_salary'][4]) + r''' & ''' + format_currency(norm['management_salary'][3]) + r''' & ''' + format_currency(norm['management_salary'][2]) + r''' & ''' + format_currency(norm['management_salary'][1]) + r''' & ''' + format_currency(norm['management_salary'][0]) + r''' & \\
# \rowcolor{white}
# \textbf{Total Adjustments} & ''' + format_currency(norm['total_adjustments'][4]) + r''' & ''' + format_currency(norm['total_adjustments'][3]) + r''' & ''' + format_currency(norm['total_adjustments'][2]) + r''' & ''' + format_currency(norm['total_adjustments'][1]) + r''' & ''' + format_currency(norm['total_adjustments'][0]) + r''' & \\
# \rowcolor{tableodd}
# \textbf{SDE} & ''' + format_currency(norm['sde'][4]) + r''' & ''' + format_currency(norm['sde'][3]) + r''' & ''' + format_currency(norm['sde'][2]) + r''' & ''' + format_currency(norm['sde'][1]) + r''' & ''' + format_currency(norm['sde'][0]) + r''' & \\
# \rowcolor{white}
# Replace owner with manager & ''' + format_currency(norm['manager_salary'][4]) + r''' & ''' + format_currency(norm['manager_salary'][3]) + r''' & ''' + format_currency(norm['manager_salary'][2]) + r''' & ''' + format_currency(norm['manager_salary'][1]) + r''' & ''' + format_currency(norm['manager_salary'][0]) + r''' & \\
# \rowcolor{tableodd}
# \textbf{Adjusted EBITDA} & ''' + format_currency(norm['adj_ebitda'][4]) + r''' & ''' + format_currency(norm['adj_ebitda'][3]) + r''' & ''' + format_currency(norm['adj_ebitda'][2]) + r''' & ''' + format_currency(norm['adj_ebitda'][1]) + r''' & ''' + format_currency(norm['adj_ebitda'][0]) + r''' & \\
# \rowcolor{white}
# \textbf{Year Weighting} & ''' + str(norm['year_weighting'][4]) + r'''\% & ''' + str(norm['year_weighting'][3]) + r'''\% & ''' + str(norm['year_weighting'][2]) + r'''\% & ''' + str(norm['year_weighting'][1]) + r'''\% & ''' + str(norm['year_weighting'][0]) + r'''\% & \\
# \end{tabular}
# \end{center}

# \vspace{0.3cm}

# \textit{\small Note: Projected year is calculated from the year to date statement from January 1 to September 30.}

# \vspace{0.5cm}

# \subsection*{Adjusted EBITDA}

# In its simplest definition, adjusted EBITDA is a measure of a company's financial performance, acting as an alternative to other metrics like revenue, earnings or net income.

# Adjusted EBITDA is how many people determine business value as it places the focus on the financial outcome of operating decisions. It does this by removing the impacts of non-operating decisions made by the existing management, such as interest expenses, tax rates, or significant intangible assets. This leaves a figure that better reflects the operating profitability of a business, one that can effectively be compared between companies by owners, buyers and investors. It is for that reason many employ adjusted EBITDA over other metrics when deciding which organization is more attractive.

# \subsection*{What does EBITDA stand for?}

# \textbf{E - Earnings} - how much money a company makes.

# \textbf{B - Before}

# \textbf{I - Interest} - the expenses to a business caused by interest rates, such as loans provided by a bank or similar third-party.

# \textbf{T - Taxes} - the expenses to a business caused by tax rates imposed by their city, state, and country.

# \textbf{D - Depreciation} - a non-cash expense referring to the gradual reduction in value of a company's assets.

# \textbf{A - Amortization} - a non-cash expense referring to the cost of intangible (non-balance sheet) assets over time.

# \subsection*{SDE}

# Business owners often try to optimize the taxes they pay each year. As a result, it is not uncommon for a company to appear to make less money, `on paper.' For example, a company's profits are reduced if the owner takes a salary from their business, as that wage appears is an expense. However, this is money in the pocket of the business owner.

# Therefore, we use Seller's Discretionary Earnings (SDE) as a better way to show the profitability of an owner/operator business. To calculate SDE we add back all the benefits the owner receives from the business to Net Income (owner salaries, depreciation/amortization, etc.).

# \clearpage
# '''

#     # Industry Benchmarks
#     bench = data['industry_benchmarks']
#     latex += r'''\section*{Industry Benchmarks}
# \addcontentsline{toc}{section}{Industry Benchmarks}

# The table below compares your financial performance to ''' + f"{bench['sample_size']:,}" + r''' other businesses in your industry using data from Statistics Canada. Benchmarking data is created using a sample of Revenue Canada tax returns for incorporated businesses operating in Canada. To start increasing your valuation, focus on areas labelled `Improvement Opportunity' in the analysis column.

# \vspace{0.5cm}

# \begin{center}
# \begin{tabular}{lrrr}
# \rowcolor{tableheader}
# \textcolor{white}{} & \textcolor{white}{\textbf{Your Average}} & \textcolor{white}{\textbf{Industry Average}} & \textcolor{white}{\textbf{Analysis}} \\
# \rowcolor{tableodd}
# Cost of Goods & ''' + format_percent(bench['your_cost_of_goods']) + r''' & ''' + format_percent(bench['cost_of_goods_avg']) + r''' & Good \\
# \rowcolor{white}
# Total Expenses & ''' + format_percent(bench['your_total_expenses']) + r''' & ''' + format_percent(bench['total_expenses_avg']) + r''' & Good \\
# \end{tabular}
# \end{center}

# \vspace{0.5cm}

# \textit{\small * Note: Depending on how your accountant prepares your financial statements, your salaries \& wages and/or direct wages may appear high or low.}

# \vspace{0.3cm}

# On average, total employment costs in your industry are ''' + format_percent(bench['total_employment_costs_avg']) + r'''\% of revenue. In comparison, your total employment costs are ''' + format_percent(bench['your_employment_costs']) + r'''\%.

# \clearpage
# '''

#     # Scorecard Section
#     latex += r'''\section*{Scorecard}
# \addcontentsline{toc}{section}{Scorecard}

# \subsection*{Valuation Range}

# Sometimes the numbers don't represent the true value of a business. Scorecard values can change the valuation by +/- 25\% of the base valuation. The chart below show the valuation range for ''' + company_name + r''' based on the scorecard answers. A totally optimized scorecard would give a business valuation of ''' + format_currency(max_val) + r'''.

# \vspace{0.5cm}

# \begin{center}
# \begin{tikzpicture}
# \draw[fill=lightgray] (0,0) rectangle (12,0.5);
# \draw[fill=primaryblue] (''' + str(6 * (mpsp - min_val) / (max_val - min_val)) + r''',0) circle (0.3);
# \node[anchor=north] at (0,-0.1) {''' + format_currency(min_val) + r'''};
# \node[anchor=north] at (6,-0.1) {\textbf{''' + format_currency(mpsp) + r'''}};
# \node[anchor=north] at (12,-0.1) {''' + format_currency(max_val) + r'''};
# \end{tikzpicture}
# \end{center}

# \vspace{0.5cm}

# \subsection*{Section Breakdown}

# The following tables break down the qualitative analysis of ''' + company_name + r'''. Each section shows how your answers affect your overall valuation. Use the chart below each table as a guide to find areas of improvement in your business. Start with the sections where your score falls below the mid line as these are generally the areas where you will see the biggest impact in your valuation.

# \clearpage
# '''

#     # Finance and Operations Section
#     fin_ops = data['scorecard']['sections']['finance_operations']
#     fin_ops_range = sections_range['finance_operations']
    
#     latex += r'''\subsection*{Finance and General Operations +/- ''' + str(fin_ops['weight']) + r'''\% of valuation}

# \begin{center}
# \begin{tabular}{>{\raggedright}p{10cm}p{4cm}}
# \rowcolor{tableheader}
# \textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
# \rowcolor{tableodd}
# Businesses typically have higher valuations when processes are documented. Does your firm have documented systemized business processes? & ''' + fin_ops['questions']['documented_processes'] + r''' \\
# \rowcolor{white}
# Do you hire an accountant to prepare your year-end Financial Statements and/or tax returns? & ''' + fin_ops['questions']['accountant'] + r''' \\
# \rowcolor{tableodd}
# Do you prepare an annual operating budget? & ''' + fin_ops['questions']['annual_budget'] + r''' \\
# \rowcolor{white}
# Are your payables always paid in full and on-time? & ''' + fin_ops['questions']['payables_on_time'] + r''' \\
# \end{tabular}
# \end{center}

# \vspace{0.5cm}

# \begin{center}
# \begin{tikzpicture}
# \draw[<->] (0,0) -- (8,0);
# \node[anchor=north] at (0,-0.1) {''' + format_currency(-fin_ops_range) + r'''};
# \node[anchor=north] at (8,-0.1) {''' + format_currency(fin_ops_range) + r'''};
# \draw (4,0) -- (4,0.3);
# \end{tikzpicture}
# \end{center}

# It is very difficult for a potential buyer to assess, and ultimately purchase, a business without being able to review accurate financial statements. To increase your score in this area:

# \begin{itemize}
# \item Make sure you use a certified accountant to prepare your financial statements and file your tax returns.
# \item Make sure your accounts payable are up to date and you are meeting all the terms of your supplier contracts.
# \item Draft a budget. Creating, monitoring, and managing a budget is the key to business success. A detailed and realistic budget can be most important tool for guiding your business.
# \item Document processes and procedures in a way that someone that is not from the organization can come in and understand them. Ensure thorough procedures are detailed for all sales and operational processes.
# \end{itemize}

# \clearpage
# '''

#     # Owner Dependency
#     owner_dep = data['scorecard']['sections']['owner_dependency']
#     owner_dep_range = sections_range['owner_dependency']
    
#     latex += r'''\subsection*{Owner Dependency +/- ''' + str(owner_dep['weight']) + r'''\% of valuation}

# \begin{center}
# \begin{tabular}{>{\raggedright}p{10cm}p{4cm}}
# \rowcolor{tableheader}
# \textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
# \rowcolor{tableodd}
# Would your company thrive if you left for 2 months? & ''' + owner_dep['questions']['thrive_without_owner'] + r''' \\
# \rowcolor{white}
# Have you taken a vacation longer than 1 month in the past 2 years? & ''' + owner_dep['questions']['vacation_over_month'] + r''' \\
# \rowcolor{tableodd}
# On a normal day, what percentage of customers ask for you by name? & ''' + owner_dep['questions']['customers_ask_by_name_pct'] + r''' \\
# \end{tabular}
# \end{center}

# \vspace{0.5cm}

# \begin{center}
# \begin{tikzpicture}
# \draw[<->] (0,0) -- (8,0);
# \node[anchor=north] at (0,-0.1) {''' + format_currency(-owner_dep_range) + r'''};
# \node[anchor=north] at (8,-0.1) {''' + format_currency(owner_dep_range) + r'''};
# \draw (4,0) -- (4,0.3);
# \end{tikzpicture}
# \end{center}

# One of the single biggest concerns voiced by business acquirers is the fear that the business will collapse without the founder at the helm. To alleviate that concern, and to increase the value of your business, make every effort to reduce your importance in day-to-day business operations.

# \begin{itemize}
# \item Start with identifying your daily tasks, making an accurate list of day-to-day operations. Then, delegate.
# \item Delegate - create and mentor leaders by giving employees more responsibility. Take time to train new managers to take on your roles.
# \item Automate systems, many tech companies have created niche products designed to expedite quotes, sales, project management, invoicing, customer service management etc.
# \item Transition key clients to other managers or sales members. Though a delicate task, it will help position you in a less demanding role.
# \item Start being gradually absent. See how your company does once you've removed yourself, first for a long weekend, then a week, then longer. Ultimately, your end goal here is to get your staff used to the fact that you're no longer running things, and to solve day-to-day issues without you at the helm.
# \end{itemize}

# \clearpage
# '''

#     # Growth Potential
#     growth = data['scorecard']['sections']['growth_potential']
#     growth_range = sections_range['growth_potential']
    
#     latex += r'''\subsection*{Growth Potential +/- ''' + str(growth['weight']) + r'''\% of valuation}

# \begin{center}
# \begin{tabular}{>{\raggedright}p{10cm}p{4cm}}
# \rowcolor{tableheader}
# \textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
# \rowcolor{tableodd}
# Have you identified growth opportunities in your business? & ''' + growth['questions']['identified_opportunities'] + r''' \\
# \rowcolor{white}
# In your current space and with your current equipment, by how much could you increase revenues? & ''' + growth['questions']['revenue_increase_capacity'] + r''' \\
# \end{tabular}
# \end{center}

# \vspace{0.5cm}

# \begin{center}
# \begin{tikzpicture}
# \draw[<->] (0,0) -- (8,0);
# \node[anchor=north] at (0,-0.1) {''' + format_currency(-growth_range) + r'''};
# \node[anchor=north] at (8,-0.1) {''' + format_currency(growth_range) + r'''};
# \draw (4,0) -- (4,0.3);
# \end{tikzpicture}
# \end{center}

# Growth potential is an organization's future ability to generate larger profits, expand its workforce and increase production. If you have not identified areas of growth in your business, consider:

# \begin{itemize}
# \item Selling products/services online, or moving into new or adjacent markets.
# \item Increasing participation in local associations or community events.
# \item Automating existing systems and procedures.
# \item Developing new products and/or services.
# \item Improving customer experience and support.
# \item Training existing staff to improve operational efficiencies.
# \item Use different marketing techniques or increase marketing budget.
# \end{itemize}

# Document growth opportunities - even if you don't act on them, a buyer will appreciate knowing that there is a path to increased revenue.

# \clearpage
# '''

#     # Recurring Revenues
#     recurring = data['scorecard']['sections']['recurring_revenues']
#     recurring_range = sections_range['recurring_revenues']
    
#     latex += r'''\subsection*{Recurring Revenues +/- ''' + str(recurring['weight']) + r'''\% of valuation}

# \begin{center}
# \begin{tabular}{>{\raggedright}p{10cm}p{4cm}}
# \rowcolor{tableheader}
# \textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
# \rowcolor{tableodd}
# Which one of these best describes your revenue model? & ''' + recurring['questions']['revenue_model'] + r''' \\
# \end{tabular}
# \end{center}

# \vspace{0.5cm}

# \begin{center}
# \begin{tikzpicture}
# \draw[<->] (0,0) -- (8,0);
# \node[anchor=north] at (0,-0.1) {''' + format_currency(-recurring_range) + r'''};
# \node[anchor=north] at (8,-0.1) {''' + format_currency(recurring_range) + r'''};
# \draw (4,0) -- (4,0.3);
# \end{tikzpicture}
# \end{center}

# Buyers love recurring revenues. Recurring revenue is the portion of a company's revenue that is contracted to continue in the future. Unlike one-off sales, these revenues are predictable, stable and can be counted on to occur at regular intervals going forward with a high degree of certainty. Examples include cell phone contracts, magazine subscriptions, and service plans.

# Not all companies can transition their customers to a recurring revenue model, but if you have the ability to do one or more of the following, your business value will increase:

# \begin{itemize}
# \item Can you offer monthly service plans?
# \item Can you implement a membership program?
# \item Do you have additional service options available?
# \item Can you set up an affiliate program?
# \end{itemize}

# \clearpage
# '''

#     # Organizational Stability
#     org_stab = data['scorecard']['sections']['organizational_stability']
#     org_stab_range = sections_range['organizational_stability']
    
#     latex += r'''\subsection*{Organizational Stability +/- ''' + str(org_stab['weight']) + r'''\% of valuation}

# \begin{center}
# \begin{tabular}{>{\raggedright}p{10cm}p{4cm}}
# \rowcolor{tableheader}
# \textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
# \rowcolor{tableodd}
# How much revenue does your largest customer represent? & ''' + org_stab['questions']['largest_customer_pct'] + r''' \\
# \rowcolor{white}
# How much revenue does your 5 largest customers represent? & ''' + org_stab['questions']['top_5_customers_pct'] + r''' \\
# \rowcolor{tableodd}
# If this person isn't you, could you easily replace the person most responsible for sales and marketing in your business? & ''' + org_stab['questions']['replace_sales_person'] + r''' \\
# \rowcolor{white}
# If this person isn't you, could you easily replace the person most responsible for product/service design \& delivery in your business? & ''' + org_stab['questions']['replace_delivery_person'] + r''' \\
# \rowcolor{tableodd}
# Could you easily replace the most important outside supplier to your business? & ''' + org_stab['questions']['replace_supplier'] + r''' \\
# \end{tabular}
# \end{center}

# \vspace{0.5cm}

# \begin{center}
# \begin{tikzpicture}
# \draw[<->] (0,0) -- (8,0);
# \node[anchor=north] at (0,-0.1) {''' + format_currency(-org_stab_range) + r'''};
# \node[anchor=north] at (8,-0.1) {''' + format_currency(org_stab_range) + r'''};
# \draw (4,0) -- (4,0.3);
# \end{tikzpicture}
# \end{center}

# Business buyers are often concerned about how stable or resilient an organization is. An organization that is not heavily dependent on one or two key employees, one supplier or a small group of customers is more saleable and more valuable than a company that has all its eggs in one basket. The best way to create a strong foundation is to diversify:

# \begin{itemize}
# \item Developing a more diverse customer base mitigates risk and provides additional financial security and stability. Having one customer make up a significant amount of your revenues creates uncertainty and can cause major disruption if said customer were to leave.
# \item Crosstrain your employees as much as possible.
# \item Create relationships with multiple suppliers. If supplier A isn't available, ensure your relationship with supplier B is equally strong.
# \end{itemize}

# \clearpage
# '''

#     # Sales and Marketing
#     sales = data['scorecard']['sections']['sales_marketing']
#     sales_range = sections_range['sales_marketing']
    
#     latex += r'''\subsection*{Sales and Marketing +/- ''' + str(sales['weight']) + r'''\% of valuation}

# \begin{center}
# \begin{tabular}{>{\raggedright}p{10cm}p{4cm}}
# \rowcolor{tableheader}
# \textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
# \rowcolor{tableodd}
# Do you collect customer feedback with a documented process? & ''' + sales['questions']['customer_feedback'] + r''' \\
# \rowcolor{white}
# How much do you spend on marketing as a percentage of gross revenue? & ''' + sales['questions']['marketing_spend_pct'] + r''' \\
# \rowcolor{tableodd}
# Do you show up on the first page on a local Google search in your industry? & ''' + sales['questions']['google_first_page'] + r''' \\
# \rowcolor{white}
# Do you have a written customer acquisition strategy? & ''' + sales['questions']['written_acquisition_strategy'] + r''' \\
# \end{tabular}
# \end{center}

# \vspace{0.5cm}

# \begin{center}
# \begin{tikzpicture}
# \draw[<->] (0,0) -- (8,0);
# \node[anchor=north] at (0,-0.1) {''' + format_currency(-sales_range) + r'''};
# \node[anchor=north] at (8,-0.1) {''' + format_currency(sales_range) + r'''};
# \draw (4,0) -- (4,0.3);
# \end{tikzpicture}
# \end{center}

# Marketing and sales strategies are essential because they are designed to help you sell your products or services. Through proper communication, marketing helps your business become a market leader and trigger purchase decisions. In addition, it builds a reputation and it's fair to say that your reputation determines your brand equity.

# When businesses have an existing marketing plan and established brand, obtaining and retaining customers will be less work for a buyer, making the business more desirable. Here are some questions you can ask yourself:

# \begin{itemize}
# \item Do you have an annual budget allocated to marketing initiatives? If so, how much is it? Is it a percentage of your gross revenue?
# \item How strong is your branding? Do you show up first in a Google search?
# \item Do you have a web presence through a website or social media?
# \item Can you identify your ideal customer? (Demographic, psychographic, behavior)
# \item Do you have any customer feedback surveys or follow-up strategies/protocols?
# \item Are you tracking how people discover your business?
# \end{itemize}

# \clearpage
# '''

#     # Appendix - Comparable Transactions
#     latex += r'''\section*{Appendix A}
# \addcontentsline{toc}{section}{Appendix A}

# \subsection*{Comparable Transactions}

# \begin{center}
# \tiny
# \begin{longtable}{lrrrrrrr}
# \rowcolor{tableheader}
# \textcolor{white}{\textbf{NAICS Code}} & \textcolor{white}{\textbf{Revenue}} & \textcolor{white}{\textbf{SDE}} & \textcolor{white}{\textbf{Adj. EBITDA}} & \textcolor{white}{\textbf{Price}} & \textcolor{white}{\textbf{Revenue Multiple}} & \textcolor{white}{\textbf{SDE Multiple}} & \textcolor{white}{\textbf{Adj. EBITDA Multiple}} \\
# \endfirsthead
# \rowcolor{tableheader}
# \textcolor{white}{\textbf{NAICS Code}} & \textcolor{white}{\textbf{Revenue}} & \textcolor{white}{\textbf{SDE}} & \textcolor{white}{\textbf{Adj. EBITDA}} & \textcolor{white}{\textbf{Price}} & \textcolor{white}{\textbf{Revenue Multiple}} & \textcolor{white}{\textbf{SDE Multiple}} & \textcolor{white}{\textbf{Adj. EBITDA Multiple}} \\
# \endhead
# '''

#     # Add transaction rows
#     transactions = data['comparable_transactions']['transactions']
#     for i, trans in enumerate(transactions):
#         row_color = "tableodd" if i % 2 == 0 else "white"
#         latex += r'''\rowcolor{''' + row_color + r'''}
# ''' + trans['naics'] + r''' & ''' + format_currency(trans['revenue']) + r''' & ''' + format_currency(trans['sde']) + r''' & ''' + format_currency(trans['adj_ebitda']) + r''' & ''' + format_currency(trans['price']) + r''' & ''' + str(trans['rev_mult']) + r''' & ''' + str(trans['sde_mult']) + r''' & ''' + str(trans['ebitda_mult']) + r''' \\
# '''

#     latex += r'''\end{longtable}
# \end{center}

# \end{document}'''

#     return latex


# def main():
#     """Main function to generate the report"""
    
#     # Check command line arguments
#     if len(sys.argv) != 2:
#         print("Usage: python generate_report.py <data_file.json>")
#         print("\nExample: python generate_report.py report_data.json")
#         sys.exit(1)
    
#     data_file = sys.argv[1]
    
#     # Check if data file exists
#     if not os.path.exists(data_file):
#         print(f"Error: Data file '{data_file}' not found.")
#         sys.exit(1)
    
#     # Check if logo exists
#     if not os.path.exists('Chinook_logo.png'):
#         print("Warning: Chinook_logo.png not found. The report will fail to compile without it.")
#         print("Please place the logo file in the same directory as this script.")
    
#     # Load data
#     print(f"Loading data from {data_file}...")
#     try:
#         with open(data_file, 'r') as f:
#             data = json.load(f)
#     except json.JSONDecodeError as e:
#         print(f"Error parsing JSON file: {e}")
#         sys.exit(1)
#     except Exception as e:
#         print(f"Error reading file: {e}")
#         sys.exit(1)
    
#     # Generate LaTeX
#     print("Generating LaTeX document...")
#     latex_content = generate_latex(data)
    
#     # Write to file
#     output_file = 'valuation_report.tex'
#     print(f"Writing to {output_file}...")
#     with open(output_file, 'w') as f:
#         f.write(latex_content)
    
#     print(f"\nSuccess! LaTeX file generated: {output_file}")
#     print("\nTo compile the PDF, run:")
#     print(f"  pdflatex {output_file}")
#     print(f"  pdflatex {output_file}  (run twice for TOC)")
#     print("\nOr use:")
#     print(f"  latexmk -pdf {output_file}")
#     print("\nMake sure you have:")
#     print("  1. Chinook_logo.png in the same directory")
#     print("  2. A LaTeX distribution installed (e.g., TeX Live, MiKTeX)")


# if __name__ == "__main__":
#     main()







#!/usr/bin/env python3
"""
Valuation Report Generator
Creates a professional business valuation report from JSON data
"""

import json
import os
import sys
from pathlib import Path


def format_currency(value):
    """Format number as currency with $ and commas"""
    return f"\\${value:,.0f}"


def format_percent(value):
    """Format number as percentage"""
    return f"{value:.2f}\\%"


def calculate_gross_profit_percent(gross_profit, revenue):
    """Calculate gross profit percentage"""
    if revenue == 0:
        return 0
    return (gross_profit / revenue) * 100


def calculate_net_income_percent(net_income, revenue):
    """Calculate net income percentage"""
    if revenue == 0:
        return 0
    return (net_income / revenue) * 100


def generate_latex(data):
    """Generate complete LaTeX document from data"""
    
    # Extract commonly used values
    company_name = data['company']['name']
    report_date = data['company']['report_date']
    mpsp = data['valuation']['mpsp']
    naics = data['company']['naics_code']
    
    # Calculate scorecard ranges
    min_val = data['scorecard']['minimum_valuation']
    max_val = data['scorecard']['optimized_valuation']
    
    # Calculate section ranges
    sections_range = {}
    for section_name, section_data in data['scorecard']['sections'].items():
        weight = section_data['weight']
        range_amount = int(mpsp * weight / 100)
        sections_range[section_name] = range_amount
    
    # Start building LaTeX
    latex = r'''\documentclass[11pt,letterpaper]{article}
\usepackage[letterpaper,margin=1in,top=1in,bottom=1in]{geometry}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{array}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{colortbl}
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{tocloft}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{amsmath}
\usepackage{tikz}
\usepackage[hidelinks]{hyperref}

% Define colors
\definecolor{primarypurple}{RGB}{102,45,145}
\definecolor{lightgray}{RGB}{240,240,240}
\definecolor{darkgray}{RGB}{100,100,100}
\definecolor{tableheader}{RGB}{102,45,145}
\definecolor{tableodd}{RGB}{245,240,250}

% Header and footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small Most Probable Selling Price Report}
\fancyhead[R]{\small ''' + company_name + r'''}
\fancyfoot[L]{\small Chinook Business Advisory}
\fancyfoot[R]{\small \thepage\ of \pageref{LastPage}}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0.5pt}

% Title formatting
\titleformat{\section}
  {\normalfont\Large\bfseries\color{primarypurple}}
  {}{0em}{}[\titlerule]
\titleformat{\subsection}
  {\normalfont\large\bfseries\color{primarypurple}}
  {\thesubsection}{1em}{}

% TOC formatting
\renewcommand{\contentsname}{Table of Contents}
\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}
\setlength{\cftbeforesecskip}{8pt}

% List formatting
\setlist[itemize]{leftmargin=*,topsep=6pt,itemsep=3pt}

\begin{document}

% Title Page
\begin{titlepage}
\centering
\vspace*{1cm}

% Black rectangle with white text
\colorbox{black}{%
  \parbox{0.9\textwidth}{%
    \centering
    \vspace{0.5cm}
    {\Huge\bfseries\textcolor{white}{Most Probable Selling Price Report}\par}
    \vspace{0.5cm}
  }%
}

\vspace{1.5cm}

{\LARGE\bfseries ''' + company_name + r'''\par}
\vspace{1cm}

{\Large ''' + report_date + r'''\par}
\vspace{2cm}

\includegraphics[width=0.4\textwidth]{Chinook_logo.png}

\vfill

{\large Chinook Business Advisory\par}

\end{titlepage}

% Table of Contents
\tableofcontents
\clearpage

% Main Content
\section*{Purpose \& Scope}
\addcontentsline{toc}{section}{Purpose \& Scope}

This report will provide an opinion of the Most Probable Selling Price (`MPSP') to the User, where the User is the Client or the agent or representative of the Client (the `User').

This is the price for the enterprise (the `Business') and its assets if to be sold as a going concern. This price includes normal inventory but does not include any other components of working capital.

The purpose of this report is to provide an opinion of the Business's MPSP. It is not intended to be a formal valuation of the business, enterprise, or the assets thereof. It is a limited assessment of the MPSP, which is defined by the International Business Brokers Association (IBBA) as, `that price for the assets or shares intended for sale which represents the total consideration most likely to be established between a buyer and a seller considering compulsion on the part of either the buyer or the seller, and potential financial strategic or non-financial benefits to the seller and probable buyer'. This report is intended for the sole use of the User and specifically for the purpose cited herein; all others possessing this report are not intended users. The use of this report by anyone other than the intended person and for the intended purpose, is not authorized.

\subsection*{Valuation Assumptions}

The generation of this report relied upon:

\begin{enumerate}[itemsep=3pt]
\item A qualitative questionnaire completed by the user.
\item The Income Statements and/or Balance Sheets provided by the user.
\item Comparable transaction data.
\end{enumerate}

\subsection*{General Assumptions}

The following assumptions were made when preparing this report.

\begin{enumerate}[itemsep=3pt]
\item The Business is a sole proprietorship, legal partnership, or a corporation.
\item The Business has no contingent liabilities, unusual contractual obligations, or substantial commitments, other than in the ordinary course of business.
\item The Business has no litigation pending or threatened.
\item Chinook Business Advisory did not audit or otherwise verify the financial information submitted.
\end{enumerate}

\clearpage

\section*{Disclaimer}
\addcontentsline{toc}{section}{Disclaimer}

Chinook Business Advisory, does not warrant any information contained herein and is not responsible for any results whatsoever as a result of, or as a consequence of, using the information provided in this report. It is understood that market conditions are variable, business operations and the perceived risks associated with them are subject to change, and that the motivations of both Purchasers and Vendors may differ and result in an ultimate sale price either higher or lower than predicted in the report. The valuation of the business assets, goodwill and/or share value is not warranted in any way.

The User has supplied the information contained in this report. Chinook Business Advisory has not audited or otherwise confirmed this information and makes no representations, expressed or implied, as to its accuracy or completeness or the conclusions to be drawn and shall in no way be responsible for the content, accuracy and truthfulness of such information.

The information presented in this report is the result of the User's input, representations and calculations. Additional information, such as market data from reliable sources, will also be considered. The Report will contain information and conclusions deemed to be relevant to the User but is offered without any guarantees or warranties relating to specific statements or implied statements contained herein.

An essential step in the review of a company is an analysis of its financial performance over time. Analyzing a company's financial statements provides an indication of historical growth, liquidity, leverage, and profitability, all of which influence the value of a company's assets or equity. The following section of this report examines the trend of the company's financial performance in the previous fiscal years.

The subject company's historical income statements have been adjusted by the User to present the business as if it had been managed to maximize profitability. Since private companies tend to keep reported profits and resulting taxes as low as possible, adjusting the financial statements is an important element to understanding the true earning capacity of the business.

Adjustments include any fringe benefits the owner may have had, unusual circumstances, liens that will be paid off, as well as the standard adjustments used to determine Adjusted EBITDA (Earnings before Interest, Taxes, Depreciation, and Amortization). This will reflect a more realistic income for a new owner and allow a prospective purchaser to compare ``apples to apples''.

This adjusted profit is known as SDE (Seller's Discretionary Earnings). SDE could be defined as the total financial benefit available to a single person who owns and is fully employed in the operation of the business. Put another way, Adj. EBITDA = SDE minus a manager's salary. Analysis of the subject Company is based on the adjusted totals. A summary of the adjusted historical financial statements is contained in the following section.

Chinook Business Advisory does not audit or review the financial statements of the subject company nor any of the adjustments made by the User and bears no responsibility for the use of this report.

\clearpage

\section*{Valuation}
\addcontentsline{toc}{section}{Valuation}

\vspace{1cm}

\noindent
Based on the information provided, the report has determined the Most Probable Selling Price (MPSP) for ''' + company_name + r''' to be:

\begin{center}
{\Huge\bfseries\color{primarypurple} ''' + format_currency(mpsp) + r'''}
\end{center}

\vspace{1cm}

\subsection*{Valuation Multiples}

This price was determined using a market-based approach which examined ''' + str(data['comparable_transactions']['count']) + r''' comparable transactions. These transactions included businesses with revenues between ''' + format_currency(data['comparable_transactions']['revenue_range'][0]) + r''' and ''' + format_currency(data['comparable_transactions']['revenue_range'][1]) + r'''. An asking price of ''' + format_currency(mpsp) + r''' represents the following valuation multiples:

\vspace{0.5cm}

\begin{minipage}[t]{0.55\textwidth}
\vspace{0pt}
\end{minipage}%
\hfill
\begin{minipage}[t]{0.4\textwidth}
\vspace{0pt}
\begin{tabular}{|>{\raggedright}p{3cm}|r|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Valuation Metric}} & \textcolor{white}{\textbf{Multiple}} \\
\hline
\rowcolor{tableodd}
Revenue & ''' + str(data['valuation']['revenue_multiple']) + r''' \\
\hline
\rowcolor{white}
SDE & ''' + str(data['valuation']['sde_multiple']) + r''' \\
\hline
\rowcolor{tableodd}
Adj. EBITDA & ''' + str(data['valuation']['adj_ebitda_multiple']) + r''' \\
\hline
\end{tabular}
\end{minipage}

\vspace{0.5cm}

See Appendix A for comparable transactions.

\clearpage
'''

    # Company Overview Section
    fin_data = data['financial_data']
    years = fin_data['years']
    
    # Calculate gross profit percentages
    gp_pcts = []
    for i in range(len(years)):
        gp_pct = calculate_gross_profit_percent(fin_data['gross_profit'][i], fin_data['revenue'][i])
        gp_pcts.append(gp_pct)
    
    # Calculate net income percentages
    ni_pcts = []
    for i in range(len(years)):
        ni_pct = calculate_net_income_percent(fin_data['net_income'][i], fin_data['revenue'][i])
        ni_pcts.append(ni_pct)
    
    norm = data['normalizations']
    
    latex += r'''\section*{Company Overview}
\addcontentsline{toc}{section}{Company Overview}

\begin{tabular}{ll}
\textbf{Name of Business:} & ''' + company_name + r''' \\
\textbf{NAICS Industry Code:} & ''' + naics + r''' \\
\textbf{MPSP:} & ''' + format_currency(mpsp) + r''' \\
\end{tabular}

\vspace{0.5cm}

\begin{center}
\small
\begin{tabular}{|l|r|r|r|r|r|}
\hline
\rowcolor{tableheader}
\textcolor{white}{} & \textcolor{white}{\textbf{''' + years[4] + r'''}} & \textcolor{white}{\textbf{''' + years[3] + r'''}} & \textcolor{white}{\textbf{''' + years[2] + r'''}} & \textcolor{white}{\textbf{''' + years[1] + r'''}} & \textcolor{white}{\textbf{''' + years[0] + r'''}} \\
\hline
\rowcolor{tableodd}
\textbf{Total Revenue} & ''' + format_currency(fin_data['revenue'][4]) + r''' & ''' + format_currency(fin_data['revenue'][3]) + r''' & ''' + format_currency(fin_data['revenue'][2]) + r''' & ''' + format_currency(fin_data['revenue'][1]) + r''' & ''' + format_currency(fin_data['revenue'][0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Total Cost of Goods} & ''' + format_currency(fin_data['cost_of_goods'][4]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][3]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][2]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][1]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][0]) + r''' \\
\hline
\rowcolor{tableodd}
\textbf{Gross Profit} & ''' + format_currency(fin_data['gross_profit'][4]) + r''' & ''' + format_currency(fin_data['gross_profit'][3]) + r''' & ''' + format_currency(fin_data['gross_profit'][2]) + r''' & ''' + format_currency(fin_data['gross_profit'][1]) + r''' & ''' + format_currency(fin_data['gross_profit'][0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Total Expenses} & ''' + format_currency(fin_data['total_expenses'][4]) + r''' & ''' + format_currency(fin_data['total_expenses'][3]) + r''' & ''' + format_currency(fin_data['total_expenses'][2]) + r''' & ''' + format_currency(fin_data['total_expenses'][1]) + r''' & ''' + format_currency(fin_data['total_expenses'][0]) + r''' \\
\hline
\rowcolor{tableodd}
\textbf{Net Income} & ''' + format_currency(fin_data['net_income'][4]) + r''' & ''' + format_currency(fin_data['net_income'][3]) + r''' & ''' + format_currency(fin_data['net_income'][2]) + r''' & ''' + format_currency(fin_data['net_income'][1]) + r''' & ''' + format_currency(fin_data['net_income'][0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Total Normalizations} & ''' + format_currency(norm['total_adjustments'][4]) + r''' & ''' + format_currency(norm['total_adjustments'][3]) + r''' & ''' + format_currency(norm['total_adjustments'][2]) + r''' & ''' + format_currency(norm['total_adjustments'][1]) + r''' & ''' + format_currency(norm['total_adjustments'][0]) + r''' \\
\hline
\rowcolor{tableodd}
\textbf{SDE} & ''' + format_currency(norm['sde'][4]) + r''' & ''' + format_currency(norm['sde'][3]) + r''' & ''' + format_currency(norm['sde'][2]) + r''' & ''' + format_currency(norm['sde'][1]) + r''' & ''' + format_currency(norm['sde'][0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Adj. EBITDA} & ''' + format_currency(norm['adj_ebitda'][4]) + r''' & ''' + format_currency(norm['adj_ebitda'][3]) + r''' & ''' + format_currency(norm['adj_ebitda'][2]) + r''' & ''' + format_currency(norm['adj_ebitda'][1]) + r''' & ''' + format_currency(norm['adj_ebitda'][0]) + r''' \\
\hline
\rowcolor{tableodd}
\textbf{Year Weighting} & ''' + str(norm['year_weighting'][4]) + r'''\% & ''' + str(norm['year_weighting'][3]) + r'''\% & ''' + str(norm['year_weighting'][2]) + r'''\% & ''' + str(norm['year_weighting'][1]) + r'''\% & ''' + str(norm['year_weighting'][0]) + r'''\% \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{tabular}{ll}
\textbf{Weighted Average of Revenue} & ''' + format_currency(data['valuation']['weighted_avg_revenue']) + r''' \\
\textbf{MPSP Multiple of Revenue} & ''' + str(data['valuation']['revenue_multiple']) + r''' \\
\textbf{Weighted Average of SDE} & ''' + format_currency(data['valuation']['weighted_avg_sde']) + r''' \\
\textbf{MPSP Multiple of SDE} & ''' + str(data['valuation']['sde_multiple']) + r''' \\
\end{tabular}

\vspace{0.3cm}

\textit{\small Note: Projected year is calculated from the year to date statement from January 1 to September 30.}

\clearpage
'''

    # Valuation Methodologies
    latex += r'''\section*{Valuation Methodologies}
\addcontentsline{toc}{section}{Valuation Methodologies}

\subsection*{1. Earnings Based Approaches:}

This method assesses the ability of the Company to produce earnings in the future. With this approach, a valuator uses the Company's operating history to determine its expected level of earnings and the likelihood of the earnings to continue in the future.

These earnings are normalized for unusual revenue or non-operational expenses. A capitalization factor, often called a multiple, is then applied that reflects a reasonable rate of return based on the perceived risk associated with the continued profitability of the company.

Within Earning Based Approaches there are several other methodologies used such as Discounted Cash Flow (DCF) where an average of the trend of predicted future earnings is used and divided by the capitalization factor.

\subsection*{2. Asset Based Approaches:}

Includes the book value of tangible assets on the balance sheet (inventory/supplies, fixed assets, and all intangible assets) minus liabilities. Simply, the money left over if the company was liquidated.

The Asset Based Approach are often appropriate in the following situations:

\begin{enumerate}[itemsep=3pt]
\item The company is considering liquidating or going out of business
\item The company has no earnings history
\item The company's earnings cannot be reliably estimated
\item The company depends heavily on competitive contracts and there is not a consistent, predictable customer base (e.g., construction companies)
\item The company derives little or no value from labor or intangible assets (e.g., real estate or holding companies)
\item A significant portion of the company's assets are composed of liquid assets or other investments (e.g., marketable securities, real estate, mineral rights)
\end{enumerate}

As such, the asset approach is for businesses where a large amount of the value is in its tangible assets. Or the business is not generating a high enough return on its assets to warrant ``excess earnings'' or ``goodwill''.

\subsection*{3. Market Based Approaches:}

The market-based approach studies recent sales of similar assets, making adjustments for the differences between them. This is similar to how the real estate industry uses ``market comps'' to determine a listing price.

To find a Company's Most Probable Selling Price (MPSP), the report examines transaction data of businesses of a similar size and industry. The report then makes adjustments to the Company's value based on on the qualitative inputs of the the report User. These are factors such as client concentration, growth opportunities, management structure, etc.

A market-based valuation represents a reasonable expectation of what the business might sell for in a free and open market based on similar business purchase and sale transactions.

\clearpage

\subsection*{Methodology}

\textbf{Our transaction algorithm} examines a database of 40,000+ transactions to find comparable businesses that have been sold.

The algorithm selects businesses that are similar in terms of NAICS code and annual revenues. The more businesses that have sold that are similar to yours, the more accurate the MPSP will be.

\subsection*{The Science}

Based on information you provide in the financial tables, the report then assigns your business a median business value. That means that if the report finds 15 businesses that were similar it would assign your business the middle value.

\begin{center}
\includegraphics[width=0.6\textwidth]{science.png}
\end{center}

\subsection*{The Art}

The next part of the process involves taking the answers to the questions we ask and trying to determine if your business is more or less attractive than average.

This report uses your answers to more accurately position your business on the chart. If your answers suggest that your business is a little better than the average in the dataset, the report will assign a higher Most Probable Selling Price to your business. Conversely, if there are opportunities to improve your business that haven't yet been acted on, the report will assign a lower MPSP.

\begin{center}
\includegraphics[width=0.6\textwidth]{art.png}
\end{center}

\clearpage
'''

    # Unadjusted Historical Income Statements
    latex += r'''\section*{Unadjusted Historical Income Statements}
\addcontentsline{toc}{section}{Unadjusted Historical Income Statements}

\textit{Derived from accountant prepared financial statements}

\vspace{0.5cm}

\begin{center}
\small
\begin{tabular}{|l|r|r|r|r|r|}
\hline
\rowcolor{tableheader}
\textcolor{white}{} & \textcolor{white}{\textbf{''' + years[4] + r'''}} & \textcolor{white}{\textbf{''' + years[3] + r'''}} & \textcolor{white}{\textbf{''' + years[2] + r'''}} & \textcolor{white}{\textbf{''' + years[1] + r'''}} & \textcolor{white}{\textbf{''' + years[0] + r'''}} \\
\hline
\multicolumn{6}{|l|}{\textbf{Revenue}} \\
\hline
\rowcolor{tableodd}
Revenue & ''' + format_currency(fin_data['revenue'][4]) + r''' & ''' + format_currency(fin_data['revenue'][3]) + r''' & ''' + format_currency(fin_data['revenue'][2]) + r''' & ''' + format_currency(fin_data['revenue'][1]) + r''' & ''' + format_currency(fin_data['revenue'][0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Total Revenue} & ''' + format_currency(fin_data['revenue'][4]) + r''' & ''' + format_currency(fin_data['revenue'][3]) + r''' & ''' + format_currency(fin_data['revenue'][2]) + r''' & ''' + format_currency(fin_data['revenue'][1]) + r''' & ''' + format_currency(fin_data['revenue'][0]) + r''' \\
\hline
\multicolumn{6}{|l|}{\textbf{Cost of Goods}} \\
\hline
\rowcolor{tableodd}
Cost of Sales & ''' + format_currency(fin_data['cost_of_goods'][4]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][3]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][2]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][1]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Total Cost of Goods} & ''' + format_currency(fin_data['cost_of_goods'][4]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][3]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][2]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][1]) + r''' & ''' + format_currency(fin_data['cost_of_goods'][0]) + r''' \\
\hline
\rowcolor{tableodd}
\textbf{Gross Profit} & ''' + format_currency(fin_data['gross_profit'][4]) + r''' & ''' + format_currency(fin_data['gross_profit'][3]) + r''' & ''' + format_currency(fin_data['gross_profit'][2]) + r''' & ''' + format_currency(fin_data['gross_profit'][1]) + r''' & ''' + format_currency(fin_data['gross_profit'][0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Gross Profit \%} & ''' + format_percent(gp_pcts[4]) + r''' & ''' + format_percent(gp_pcts[3]) + r''' & ''' + format_percent(gp_pcts[2]) + r''' & ''' + format_percent(gp_pcts[1]) + r''' & ''' + format_percent(gp_pcts[0]) + r''' \\
\hline
\multicolumn{6}{|l|}{\textbf{Expenses}} \\
\hline
\rowcolor{tableodd}
General Expense & ''' + format_currency(fin_data['total_expenses'][4]) + r''' & ''' + format_currency(fin_data['total_expenses'][3]) + r''' & ''' + format_currency(fin_data['total_expenses'][2]) + r''' & ''' + format_currency(fin_data['total_expenses'][1]) + r''' & ''' + format_currency(fin_data['total_expenses'][0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Total Expenses} & ''' + format_currency(fin_data['total_expenses'][4]) + r''' & ''' + format_currency(fin_data['total_expenses'][3]) + r''' & ''' + format_currency(fin_data['total_expenses'][2]) + r''' & ''' + format_currency(fin_data['total_expenses'][1]) + r''' & ''' + format_currency(fin_data['total_expenses'][0]) + r''' \\
\hline
\multicolumn{6}{|l|}{\textbf{Other Income}} \\
\hline
\rowcolor{tableodd}
- & \$- & \$- & ''' + format_currency(fin_data['other_income'][2]) + r''' & \$- & \$- \\
\hline
\rowcolor{white}
\textbf{Net Income} & ''' + format_currency(fin_data['net_income'][4]) + r''' & ''' + format_currency(fin_data['net_income'][3]) + r''' & ''' + format_currency(fin_data['net_income'][2]) + r''' & ''' + format_currency(fin_data['net_income'][1]) + r''' & ''' + format_currency(fin_data['net_income'][0]) + r''' \\
\hline
\rowcolor{tableodd}
\textbf{Net Income \%} & ''' + format_percent(ni_pcts[4]) + r''' & ''' + format_percent(ni_pcts[3]) + r''' & ''' + format_percent(ni_pcts[2]) + r''' & ''' + format_percent(ni_pcts[1]) + r''' & ''' + format_percent(ni_pcts[0]) + r''' \\
\hline
\end{tabular}
\end{center}

\vspace{0.3cm}

\textit{\small Note: Projected year is calculated from the year to date statement from January 1 to September 30.}

\clearpage
'''

    # Normalization Summary
    latex += r'''\section*{Normalization Summary}
\addcontentsline{toc}{section}{Normalization Summary}

\begin{center}
\small
\begin{tabular}{|l|r|r|r|r|r|l|}
\hline
\rowcolor{tableheader}
\textcolor{white}{} & \textcolor{white}{\textbf{''' + years[4] + r'''}} & \textcolor{white}{\textbf{''' + years[3] + r'''}} & \textcolor{white}{\textbf{''' + years[2] + r'''}} & \textcolor{white}{\textbf{''' + years[1] + r'''}} & \textcolor{white}{\textbf{''' + years[0] + r'''}} & \textcolor{white}{\textbf{Notes}} \\
\hline
\rowcolor{tableodd}
Net Income & ''' + format_currency(fin_data['net_income'][4]) + r''' & ''' + format_currency(fin_data['net_income'][3]) + r''' & ''' + format_currency(fin_data['net_income'][2]) + r''' & ''' + format_currency(fin_data['net_income'][1]) + r''' & ''' + format_currency(fin_data['net_income'][0]) + r''' & \\
\hline
\rowcolor{white}
Discretionary Expense & \$- & \$- & \$- & \$- & \$- & \\
\hline
\rowcolor{tableodd}
Amortization & ''' + format_currency(norm['amortization'][4]) + r''' & ''' + format_currency(norm['amortization'][3]) + r''' & ''' + format_currency(norm['amortization'][2]) + r''' & ''' + format_currency(norm['amortization'][1]) + r''' & ''' + format_currency(norm['amortization'][0]) + r''' & \\
\hline
\rowcolor{white}
Interest on Equipment under Capital Lease & ''' + format_currency(norm['interest_capital_lease'][4]) + r''' & ''' + format_currency(norm['interest_capital_lease'][3]) + r''' & ''' + format_currency(norm['interest_capital_lease'][2]) + r''' & ''' + format_currency(norm['interest_capital_lease'][1]) + r''' & ''' + format_currency(norm['interest_capital_lease'][0]) + r''' & \\
\hline
\rowcolor{tableodd}
Management Salary & ''' + format_currency(norm['management_salary'][4]) + r''' & ''' + format_currency(norm['management_salary'][3]) + r''' & ''' + format_currency(norm['management_salary'][2]) + r''' & ''' + format_currency(norm['management_salary'][1]) + r''' & ''' + format_currency(norm['management_salary'][0]) + r''' & \\
\hline
\rowcolor{white}
\textbf{Total Adjustments} & ''' + format_currency(norm['total_adjustments'][4]) + r''' & ''' + format_currency(norm['total_adjustments'][3]) + r''' & ''' + format_currency(norm['total_adjustments'][2]) + r''' & ''' + format_currency(norm['total_adjustments'][1]) + r''' & ''' + format_currency(norm['total_adjustments'][0]) + r''' & \\
\hline
\rowcolor{tableodd}
\textbf{SDE} & ''' + format_currency(norm['sde'][4]) + r''' & ''' + format_currency(norm['sde'][3]) + r''' & ''' + format_currency(norm['sde'][2]) + r''' & ''' + format_currency(norm['sde'][1]) + r''' & ''' + format_currency(norm['sde'][0]) + r''' & \\
\hline
\rowcolor{white}
Replace owner with manager & ''' + format_currency(norm['manager_salary'][4]) + r''' & ''' + format_currency(norm['manager_salary'][3]) + r''' & ''' + format_currency(norm['manager_salary'][2]) + r''' & ''' + format_currency(norm['manager_salary'][1]) + r''' & ''' + format_currency(norm['manager_salary'][0]) + r''' & \\
\hline
\rowcolor{tableodd}
\textbf{Adjusted EBITDA} & ''' + format_currency(norm['adj_ebitda'][4]) + r''' & ''' + format_currency(norm['adj_ebitda'][3]) + r''' & ''' + format_currency(norm['adj_ebitda'][2]) + r''' & ''' + format_currency(norm['adj_ebitda'][1]) + r''' & ''' + format_currency(norm['adj_ebitda'][0]) + r''' & \\
\hline
\rowcolor{white}
\textbf{Year Weighting} & ''' + str(norm['year_weighting'][4]) + r'''\% & ''' + str(norm['year_weighting'][3]) + r'''\% & ''' + str(norm['year_weighting'][2]) + r'''\% & ''' + str(norm['year_weighting'][1]) + r'''\% & ''' + str(norm['year_weighting'][0]) + r'''\% & \\
\hline
\end{tabular}
\end{center}

\vspace{0.3cm}

\textit{\small Note: Projected year is calculated from the year to date statement from January 1 to September 30.}

\vspace{0.5cm}

\subsection*{Adjusted EBITDA}

In its simplest definition, adjusted EBITDA is a measure of a company's financial performance, acting as an alternative to other metrics like revenue, earnings or net income.

Adjusted EBITDA is how many people determine business value as it places the focus on the financial outcome of operating decisions. It does this by removing the impacts of non-operating decisions made by the existing management, such as interest expenses, tax rates, or significant intangible assets. This leaves a figure that better reflects the operating profitability of a business, one that can effectively be compared between companies by owners, buyers and investors. It is for that reason many employ adjusted EBITDA over other metrics when deciding which organization is more attractive.

\subsection*{What does EBITDA stand for?}

\textbf{E - Earnings} - how much money a company makes.

\textbf{B - Before}

\textbf{I - Interest} - the expenses to a business caused by interest rates, such as loans provided by a bank or similar third-party.

\textbf{T - Taxes} - the expenses to a business caused by tax rates imposed by their city, state, and country.

\textbf{D - Depreciation} - a non-cash expense referring to the gradual reduction in value of a company's assets.

\textbf{A - Amortization} - a non-cash expense referring to the cost of intangible (non-balance sheet) assets over time.

\subsection*{SDE}

Business owners often try to optimize the taxes they pay each year. As a result, it is not uncommon for a company to appear to make less money, `on paper.' For example, a company's profits are reduced if the owner takes a salary from their business, as that wage appears is an expense. However, this is money in the pocket of the business owner.

Therefore, we use Seller's Discretionary Earnings (SDE) as a better way to show the profitability of an owner/operator business. To calculate SDE we add back all the benefits the owner receives from the business to Net Income (owner salaries, depreciation/amortization, etc.).

\clearpage
'''

    # Industry Benchmarks
    bench = data['industry_benchmarks']
    latex += r'''\section*{Industry Benchmarks}
\addcontentsline{toc}{section}{Industry Benchmarks}

The table below compares your financial performance to ''' + f"{bench['sample_size']:,}" + r''' other businesses in your industry using data from Statistics Canada. Benchmarking data is created using a sample of Revenue Canada tax returns for incorporated businesses operating in Canada. To start increasing your valuation, focus on areas labelled `Improvement Opportunity' in the analysis column.

\vspace{0.5cm}

\begin{center}
\begin{tabular}{|l|r|r|r|}
\hline
\rowcolor{tableheader}
\textcolor{white}{} & \textcolor{white}{\textbf{Your Average}} & \textcolor{white}{\textbf{Industry Average}} & \textcolor{white}{\textbf{Analysis}} \\
\hline
\rowcolor{tableodd}
Cost of Goods & ''' + format_percent(bench['your_cost_of_goods']) + r''' & ''' + format_percent(bench['cost_of_goods_avg']) + r''' & Good \\
\hline
\rowcolor{white}
Total Expenses & ''' + format_percent(bench['your_total_expenses']) + r''' & ''' + format_percent(bench['total_expenses_avg']) + r''' & Good \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\textit{\small * Note: Depending on how your accountant prepares your financial statements, your salaries \& wages and/or direct wages may appear high or low.}

\vspace{0.3cm}

On average, total employment costs in your industry are ''' + format_percent(bench['total_employment_costs_avg']) + r'''\% of revenue. In comparison, your total employment costs are ''' + format_percent(bench['your_employment_costs']) + r'''\%.

\clearpage
'''

    # Scorecard Section
    latex += r'''\section*{Scorecard}
\addcontentsline{toc}{section}{Scorecard}

\subsection*{Valuation Range}

Sometimes the numbers don't represent the true value of a business. Scorecard values can change the valuation by +/- 25\% of the base valuation. The chart below show the valuation range for ''' + company_name + r''' based on the scorecard answers. A totally optimized scorecard would give a business valuation of ''' + format_currency(max_val) + r'''.

\vspace{0.5cm}

\begin{center}
\begin{tikzpicture}
\draw[fill=lightgray] (0,0) rectangle (12,0.5);
\draw[fill=primarypurple] (''' + str(12 * (mpsp - min_val) / (max_val - min_val)) + r''',0.25) circle (0.3);
\node[anchor=north] at (0,-0.1) {''' + format_currency(min_val) + r'''};
\node[anchor=north] at (6,-0.1) {\textbf{''' + format_currency(mpsp) + r'''}};
\node[anchor=north] at (12,-0.1) {''' + format_currency(max_val) + r'''};
\end{tikzpicture}
\end{center}

\vspace{0.5cm}

\subsection*{Section Breakdown}

The following tables break down the qualitative analysis of ''' + company_name + r'''. Each section shows how your answers affect your overall valuation. Use the chart below each table as a guide to find areas of improvement in your business. Start with the sections where your score falls below the mid line as these are generally the areas where you will see the biggest impact in your valuation.

\clearpage
'''

    # Finance and Operations Section
    fin_ops = data['scorecard']['sections']['finance_operations']
    fin_ops_range = sections_range['finance_operations']
    
    latex += r'''\subsection*{Finance and General Operations +/- ''' + str(fin_ops['weight']) + r'''\% of valuation}

\begin{center}
\begin{tabular}{|>{\raggedright}p{10cm}|p{4cm}|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
\hline
\rowcolor{tableodd}
Businesses typically have higher valuations when processes are documented. Does your firm have documented systemized business processes? & ''' + fin_ops['questions']['documented_processes'] + r''' \\
\hline
\rowcolor{white}
Do you hire an accountant to prepare your year-end Financial Statements and/or tax returns? & ''' + fin_ops['questions']['accountant'] + r''' \\
\hline
\rowcolor{tableodd}
Do you prepare an annual operating budget? & ''' + fin_ops['questions']['annual_budget'] + r''' \\
\hline
\rowcolor{white}
Are your payables always paid in full and on-time? & ''' + fin_ops['questions']['payables_on_time'] + r''' \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{center}
\begin{tikzpicture}
\draw[<->] (0,0) -- (8,0);
\node[anchor=north] at (0,-0.1) {''' + format_currency(-fin_ops_range) + r'''};
\node[anchor=north] at (8,-0.1) {''' + format_currency(fin_ops_range) + r'''};
\draw (4,0) -- (4,0.3);
\end{tikzpicture}
\end{center}

It is very difficult for a potential buyer to assess, and ultimately purchase, a business without being able to review accurate financial statements. To increase your score in this area:

\begin{itemize}
\item Make sure you use a certified accountant to prepare your financial statements and file your tax returns.
\item Make sure your accounts payable are up to date and you are meeting all the terms of your supplier contracts.
\item Draft a budget. Creating, monitoring, and managing a budget is the key to business success. A detailed and realistic budget can be most important tool for guiding your business.
\item Document processes and procedures in a way that someone that is not from the organization can come in and understand them. Ensure thorough procedures are detailed for all sales and operational processes.
\end{itemize}

\clearpage
'''

    # Owner Dependency
    owner_dep = data['scorecard']['sections']['owner_dependency']
    owner_dep_range = sections_range['owner_dependency']
    
    latex += r'''\subsection*{Owner Dependency +/- ''' + str(owner_dep['weight']) + r'''\% of valuation}

\begin{center}
\begin{tabular}{|>{\raggedright}p{10cm}|p{4cm}|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
\hline
\rowcolor{tableodd}
Would your company thrive if you left for 2 months? & ''' + owner_dep['questions']['thrive_without_owner'] + r''' \\
\hline
\rowcolor{white}
Have you taken a vacation longer than 1 month in the past 2 years? & ''' + owner_dep['questions']['vacation_over_month'] + r''' \\
\hline
\rowcolor{tableodd}
On a normal day, what percentage of customers ask for you by name? & ''' + owner_dep['questions']['customers_ask_by_name_pct'] + r''' \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{center}
\begin{tikzpicture}
\draw[<->] (0,0) -- (8,0);
\node[anchor=north] at (0,-0.1) {''' + format_currency(-owner_dep_range) + r'''};
\node[anchor=north] at (8,-0.1) {''' + format_currency(owner_dep_range) + r'''};
\draw (4,0) -- (4,0.3);
\end{tikzpicture}
\end{center}

One of the single biggest concerns voiced by business acquirers is the fear that the business will collapse without the founder at the helm. To alleviate that concern, and to increase the value of your business, make every effort to reduce your importance in day-to-day business operations.

\begin{itemize}
\item Start with identifying your daily tasks, making an accurate list of day-to-day operations. Then, delegate.
\item Delegate - create and mentor leaders by giving employees more responsibility. Take time to train new managers to take on your roles.
\item Automate systems, many tech companies have created niche products designed to expedite quotes, sales, project management, invoicing, customer service management etc.
\item Transition key clients to other managers or sales members. Though a delicate task, it will help position you in a less demanding role.
\item Start being gradually absent. See how your company does once you've removed yourself, first for a long weekend, then a week, then longer. Ultimately, your end goal here is to get your staff used to the fact that you're no longer running things, and to solve day-to-day issues without you at the helm.
\end{itemize}

\clearpage
'''

    # Growth Potential
    growth = data['scorecard']['sections']['growth_potential']
    growth_range = sections_range['growth_potential']
    
    latex += r'''\subsection*{Growth Potential +/- ''' + str(growth['weight']) + r'''\% of valuation}

\begin{center}
\begin{tabular}{|>{\raggedright}p{10cm}|p{4cm}|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
\hline
\rowcolor{tableodd}
Have you identified growth opportunities in your business? & ''' + growth['questions']['identified_opportunities'] + r''' \\
\hline
\rowcolor{white}
In your current space and with your current equipment, by how much could you increase revenues? & ''' + growth['questions']['revenue_increase_capacity'] + r''' \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{center}
\begin{tikzpicture}
\draw[<->] (0,0) -- (8,0);
\node[anchor=north] at (0,-0.1) {''' + format_currency(-growth_range) + r'''};
\node[anchor=north] at (8,-0.1) {''' + format_currency(growth_range) + r'''};
\draw (4,0) -- (4,0.3);
\end{tikzpicture}
\end{center}

Growth potential is an organization's future ability to generate larger profits, expand its workforce and increase production. If you have not identified areas of growth in your business, consider:

\begin{itemize}
\item Selling products/services online, or moving into new or adjacent markets.
\item Increasing participation in local associations or community events.
\item Automating existing systems and procedures.
\item Developing new products and/or services.
\item Improving customer experience and support.
\item Training existing staff to improve operational efficiencies.
\item Use different marketing techniques or increase marketing budget.
\end{itemize}

Document growth opportunities - even if you don't act on them, a buyer will appreciate knowing that there is a path to increased revenue.

\clearpage
'''

    # Recurring Revenues
    recurring = data['scorecard']['sections']['recurring_revenues']
    recurring_range = sections_range['recurring_revenues']
    
    latex += r'''\subsection*{Recurring Revenues +/- ''' + str(recurring['weight']) + r'''\% of valuation}

\begin{center}
\begin{tabular}{|>{\raggedright}p{10cm}|p{4cm}|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
\hline
\rowcolor{tableodd}
Which one of these best describes your revenue model? & ''' + recurring['questions']['revenue_model'] + r''' \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{center}
\begin{tikzpicture}
\draw[<->] (0,0) -- (8,0);
\node[anchor=north] at (0,-0.1) {''' + format_currency(-recurring_range) + r'''};
\node[anchor=north] at (8,-0.1) {''' + format_currency(recurring_range) + r'''};
\draw (4,0) -- (4,0.3);
\end{tikzpicture}
\end{center}

Buyers love recurring revenues. Recurring revenue is the portion of a company's revenue that is contracted to continue in the future. Unlike one-off sales, these revenues are predictable, stable and can be counted on to occur at regular intervals going forward with a high degree of certainty. Examples include cell phone contracts, magazine subscriptions, and service plans.

Not all companies can transition their customers to a recurring revenue model, but if you have the ability to do one or more of the following, your business value will increase:

\begin{itemize}
\item Can you offer monthly service plans?
\item Can you implement a membership program?
\item Do you have additional service options available?
\item Can you set up an affiliate program?
\end{itemize}

\clearpage
'''

    # Organizational Stability
    org_stab = data['scorecard']['sections']['organizational_stability']
    org_stab_range = sections_range['organizational_stability']
    
    latex += r'''\subsection*{Organizational Stability +/- ''' + str(org_stab['weight']) + r'''\% of valuation}

\begin{center}
\begin{tabular}{|>{\raggedright}p{10cm}|p{4cm}|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
\hline
\rowcolor{tableodd}
How much revenue does your largest customer represent? & ''' + org_stab['questions']['largest_customer_pct'] + r''' \\
\hline
\rowcolor{white}
How much revenue does your 5 largest customers represent? & ''' + org_stab['questions']['top_5_customers_pct'] + r''' \\
\hline
\rowcolor{tableodd}
If this person isn't you, could you easily replace the person most responsible for sales and marketing in your business? & ''' + org_stab['questions']['replace_sales_person'] + r''' \\
\hline
\rowcolor{white}
If this person isn't you, could you easily replace the person most responsible for product/service design \& delivery in your business? & ''' + org_stab['questions']['replace_delivery_person'] + r''' \\
\hline
\rowcolor{tableodd}
Could you easily replace the most important outside supplier to your business? & ''' + org_stab['questions']['replace_supplier'] + r''' \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{center}
\begin{tikzpicture}
\draw[<->] (0,0) -- (8,0);
\node[anchor=north] at (0,-0.1) {''' + format_currency(-org_stab_range) + r'''};
\node[anchor=north] at (8,-0.1) {''' + format_currency(org_stab_range) + r'''};
\draw (4,0) -- (4,0.3);
\end{tikzpicture}
\end{center}

Business buyers are often concerned about how stable or resilient an organization is. An organization that is not heavily dependent on one or two key employees, one supplier or a small group of customers is more saleable and more valuable than a company that has all its eggs in one basket. The best way to create a strong foundation is to diversify:

\begin{itemize}
\item Developing a more diverse customer base mitigates risk and provides additional financial security and stability. Having one customer make up a significant amount of your revenues creates uncertainty and can cause major disruption if said customer were to leave.
\item Crosstrain your employees as much as possible.
\item Create relationships with multiple suppliers. If supplier A isn't available, ensure your relationship with supplier B is equally strong.
\end{itemize}

\clearpage
'''

    # Sales and Marketing
    sales = data['scorecard']['sections']['sales_marketing']
    sales_range = sections_range['sales_marketing']
    
    latex += r'''\subsection*{Sales and Marketing +/- ''' + str(sales['weight']) + r'''\% of valuation}

\begin{center}
\begin{tabular}{|>{\raggedright}p{10cm}|p{4cm}|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
\hline
\rowcolor{tableodd}
Do you collect customer feedback with a documented process? & ''' + sales['questions']['customer_feedback'] + r''' \\
\hline
\rowcolor{white}
How much do you spend on marketing as a percentage of gross revenue? & ''' + sales['questions']['marketing_spend_pct'] + r''' \\
\hline
\rowcolor{tableodd}
Do you show up on the first page on a local Google search in your industry? & ''' + sales['questions']['google_first_page'] + r''' \\
\hline
\rowcolor{white}
Do you have a written customer acquisition strategy? & ''' + sales['questions']['written_acquisition_strategy'] + r''' \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{center}
\begin{tikzpicture}
\draw[<->] (0,0) -- (8,0);
\node[anchor=north] at (0,-0.1) {''' + format_currency(-sales_range) + r'''};
\node[anchor=north] at (8,-0.1) {''' + format_currency(sales_range) + r'''};
\draw (4,0) -- (4,0.3);
\end{tikzpicture}
\end{center}

Marketing and sales strategies are essential because they are designed to help you sell your products or services. Through proper communication, marketing helps your business become a market leader and trigger purchase decisions. In addition, it builds a reputation and it's fair to say that your reputation determines your brand equity.

When businesses have an existing marketing plan and established brand, obtaining and retaining customers will be less work for a buyer, making the business more desirable. Here are some questions you can ask yourself:

\begin{itemize}
\item Do you have an annual budget allocated to marketing initiatives? If so, how much is it? Is it a percentage of your gross revenue?
\item How strong is your branding? Do you show up first in a Google search?
\item Do you have a web presence through a website or social media?
\item Can you identify your ideal customer? (Demographic, psychographic, behavior)
\item Do you have any customer feedback surveys or follow-up strategies/protocols?
\item Are you tracking how people discover your business?
\end{itemize}

\clearpage
'''

    # Appendix - Comparable Transactions
    latex += r'''\section*{Appendix A}
\addcontentsline{toc}{section}{Appendix A}

\subsection*{Comparable Transactions}

\begin{center}
\tiny
\begin{longtable}{|l|r|r|r|r|r|r|r|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{NAICS Code}} & \textcolor{white}{\textbf{Revenue}} & \textcolor{white}{\textbf{SDE}} & \textcolor{white}{\textbf{Adj. EBITDA}} & \textcolor{white}{\textbf{Price}} & \textcolor{white}{\textbf{Revenue Multiple}} & \textcolor{white}{\textbf{SDE Multiple}} & \textcolor{white}{\textbf{Adj. EBITDA Multiple}} \\
\hline
\endfirsthead
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{NAICS Code}} & \textcolor{white}{\textbf{Revenue}} & \textcolor{white}{\textbf{SDE}} & \textcolor{white}{\textbf{Adj. EBITDA}} & \textcolor{white}{\textbf{Price}} & \textcolor{white}{\textbf{Revenue Multiple}} & \textcolor{white}{\textbf{SDE Multiple}} & \textcolor{white}{\textbf{Adj. EBITDA Multiple}} \\
\hline
\endhead
'''

    # Add transaction rows
    transactions = data['comparable_transactions']['transactions']
    for i, trans in enumerate(transactions):
        row_color = "tableodd" if i % 2 == 0 else "white"
        latex += r'''\rowcolor{''' + row_color + r'''}
''' + trans['naics'] + r''' & ''' + format_currency(trans['revenue']) + r''' & ''' + format_currency(trans['sde']) + r''' & ''' + format_currency(trans['adj_ebitda']) + r''' & ''' + format_currency(trans['price']) + r''' & ''' + str(trans['rev_mult']) + r''' & ''' + str(trans['sde_mult']) + r''' & ''' + str(trans['ebitda_mult']) + r''' \\
\hline
'''

    latex += r'''\end{longtable}
\end{center}

\end{document}'''

    return latex


def main():
    """Main function to generate the report"""
    
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python generate_report.py <data_file.json>")
        print("\nExample: python generate_report.py report_data.json")
        sys.exit(1)
    
    data_file = sys.argv[1]
    
    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"Error: Data file '{data_file}' not found.")
        sys.exit(1)
    
    # Check if logo exists
    if not os.path.exists('Chinook_logo.png'):
        print("Warning: Chinook_logo.png not found. The report will fail to compile without it.")
        print("Please place the logo file in the same directory as this script.")
    
    # Check if science and art images exist
    if not os.path.exists('science.png'):
        print("Warning: science.png not found. The report will fail to compile without it.")
    if not os.path.exists('art.png'):
        print("Warning: art.png not found. The report will fail to compile without it.")
    
    # Load data
    print(f"Loading data from {data_file}...")
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Generate LaTeX
    print("Generating LaTeX document...")
    latex_content = generate_latex(data)
    
    # Write to file
    output_file = 'valuation_report.tex'
    print(f"Writing to {output_file}...")
    with open(output_file, 'w') as f:
        f.write(latex_content)
    
    print(f"\nSuccess! LaTeX file generated: {output_file}")
    print("\nTo compile the PDF, run:")
    print(f"  pdflatex {output_file}")
    print(f"  pdflatex {output_file}  (run twice for TOC)")
    print("\nOr use:")
    print(f"  latexmk -pdf {output_file}")
    print("\nMake sure you have:")
    print("  1. Chinook_logo.png in the same directory")
    print("  2. science.png in the same directory")
    print("  3. art.png in the same directory")
    print("  4. A LaTeX distribution installed (e.g., TeX Live, MiKTeX)")


if __name__ == "__main__":
    main()


