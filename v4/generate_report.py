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
    try:
        return f"\\${value:,.0f}"
    except (ValueError, TypeError):
        return "\\$0"


def format_percent(value):
    """Format number as percentage"""
    try:
        return f"{value:.2f}\\%"
    except (ValueError, TypeError):
        return "0.00\\%"


def escape_latex(text):
    """Escape special LaTeX characters in text"""
    if not isinstance(text, str):
        text = str(text)
    
    replacements = {
        '&': '\\&',
        '%': '\\%',
        '$': '\\$',
        '#': '\\#',
        '_': '\\_',
        '{': '\\{',
        '}': '\\}',
        '~': '\\textasciitilde{}',
        '^': '\\textasciicircum{}',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


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


def score_to_position(score, scale_width=8):
    """
    Convert a score (1-5) to a position on the scale (0-scale_width)
    Score of 1 = left edge (0)
    Score of 3 = center (scale_width/2)
    Score of 5 = right edge (scale_width)
    """
    if score < 1:
        score = 1
    elif score > 5:
        score = 5
    
    # Map score 1-5 to position 0-scale_width
    position = ((score - 1) / 4) * scale_width
    return position


def generate_scorecard_scale(score, min_val, max_val, scale_width=8):
    """
    Generate TikZ code for a scorecard scale with a positioned circle
    """
    position = score_to_position(score, scale_width)
    
    tikz_code = r'''\begin{tikzpicture}[scale=0.9]
% Draw the gray bar
\fill[lightgray] (0,0) rectangle (''' + str(scale_width) + r''',0.6);
% Draw scale endpoints
\draw[thick] (0,0) -- (0,0.6);
\draw[thick] (''' + str(scale_width) + r''',0) -- (''' + str(scale_width) + r''',0.6);
% Draw center mark
\draw[thick] (''' + str(scale_width/2) + r''',0) -- (''' + str(scale_width/2) + r''',0.6);
% Draw the circle at the score position
\fill[primarypurple] (''' + str(position) + r''',0.3) circle (0.25);
% Labels
\node[anchor=north,font=\small] at (0,-0.2) {''' + format_currency(min_val) + r'''};
\node[anchor=north,font=\small] at (''' + str(scale_width/2) + r''',-0.2) {0};
\node[anchor=north,font=\small] at (''' + str(scale_width) + r''',-0.2) {''' + format_currency(max_val) + r'''};
\end{tikzpicture}'''
    
    return tikz_code


def validate_json_structure(data):
    """Validate the JSON structure has all required fields"""
    required_fields = {
        'company': ['name', 'naics_code', 'report_date'],
        'valuation': ['mpsp', 'revenue_multiple', 'sde_multiple', 'adj_ebitda_multiple', 
                     'weighted_avg_revenue', 'weighted_avg_sde'],
        'financial_data': ['years', 'revenue', 'cost_of_goods', 'gross_profit', 
                          'total_expenses', 'net_income', 'other_income'],
        'normalizations': ['years', 'amortization', 'interest_capital_lease', 
                          'management_salary', 'total_adjustments', 'sde', 
                          'manager_salary', 'adj_ebitda', 'year_weighting'],
        'industry_benchmarks': ['sample_size', 'cost_of_goods_avg', 'total_expenses_avg',
                               'total_employment_costs_avg', 'your_cost_of_goods',
                               'your_total_expenses', 'your_employment_costs'],
        'scorecard': ['minimum_valuation', 'optimized_valuation', 'sections'],
        'comparable_transactions': ['count', 'revenue_range', 'transactions']
    }
    
    errors = []
    
    for section, fields in required_fields.items():
        if section not in data:
            errors.append(f"Missing required section: {section}")
            continue
        
        for field in fields:
            if field not in data[section]:
                errors.append(f"Missing required field: {section}.{field}")
    
    # Validate scorecard sections
    required_sections = ['finance_operations', 'owner_dependency', 'growth_potential',
                        'recurring_revenues', 'organizational_stability', 'sales_marketing']
    
    if 'scorecard' in data and 'sections' in data['scorecard']:
        for section in required_sections:
            if section not in data['scorecard']['sections']:
                errors.append(f"Missing scorecard section: {section}")
            else:
                section_data = data['scorecard']['sections'][section]
                if 'weight' not in section_data:
                    errors.append(f"Missing weight in scorecard section: {section}")
                if 'questions' not in section_data:
                    errors.append(f"Missing questions in scorecard section: {section}")
                if 'scores' not in section_data:
                    errors.append(f"Missing scores in scorecard section: {section}")
    
    return errors


def generate_latex(data):
    """Generate complete LaTeX document from data"""
    
    # Validate data structure
    errors = validate_json_structure(data)
    if errors:
        print("WARNING: JSON structure validation failed:")
        for error in errors:
            print(f"  - {error}")
        print("\nContinuing with available data, but report may be incomplete...\n")
    
    # Extract commonly used values with safe defaults
    company_name = escape_latex(data.get('company', {}).get('name', 'Unknown Company'))
    report_date = data.get('company', {}).get('report_date', 'Unknown Date')
    mpsp = data.get('valuation', {}).get('mpsp', 0)
    naics = data.get('company', {}).get('naics_code', 'Unknown')
    
    # Calculate scorecard ranges
    min_val = data.get('scorecard', {}).get('minimum_valuation', int(mpsp * 0.75))
    max_val = data.get('scorecard', {}).get('optimized_valuation', int(mpsp * 1.25))
    
    # Calculate section ranges
    sections_range = {}
    for section_name, section_data in data.get('scorecard', {}).get('sections', {}).items():
        weight = section_data.get('weight', 0)
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

% Title Page (no page number)
\thispagestyle{empty}
\pagenumbering{gobble}

\begin{center}
\vspace*{2cm}
\includegraphics[width=0.5\textwidth]{Chinook_logo.png}
\vspace{2cm}
\end{center}

% Full-width black rectangle
\noindent\colorbox{black}{%
  \parbox{\dimexpr\textwidth-2\fboxsep\relax}{%
    \vspace{1.2cm}
    {\Huge\bfseries\textcolor{white}{Most Probable Selling Price}\par}
    \vspace{0.3cm}
    {\Huge\bfseries\textcolor{white}{Report}\par}
    \vspace{1.2cm}
    {\LARGE\bfseries\textcolor{white}{''' + company_name + r'''}\par}
    \vspace{0.4cm}
    {\Large\textcolor{white}{''' + report_date + r'''}\par}
    \vspace{1.2cm}
  }%
}



\clearpage

% Table of Contents (start page numbering at 2)
\pagenumbering{arabic}
\setcounter{page}{2}
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

Adjustments include any fringe benefits the owner may have had, unusual circumstances, liens that will be paid off, as well as the standard adjustments used to determine \textbf{Adjusted EBITDA} (Earnings before Interest, Taxes, Depreciation, and Amortization). This will reflect a more realistic income for a new owner and allow a prospective purchaser to compare ``apples to apples''.

This adjusted profit is known as SDE (Seller's Discretionary Earnings). SDE could be defined as the total financial benefit available to a single person who owns and is fully employed in the operation of the business. Put another way, Adj. EBITDA = SDE minus a manager's salary. Analysis of the subject Company is based on the adjusted totals. A summary of the adjusted historical financial statements is contained in the following section.

\textbf{Chinook Business Advisory does not audit or review the financial statements of the subject company nor any of the adjustments made by the User and bears no responsibility for the use of this report.}

\clearpage

\section*{Valuation}
\addcontentsline{toc}{section}{Valuation}

\vspace{1cm}

\begin{minipage}[t]{0.55\textwidth}
\vspace{0pt}
\noindent
Based on the information provided, the report has determined the Most Probable Selling Price (MPSP) for ''' + company_name + r''' to be:

\vspace{0.5cm}

{\Huge\bfseries\color{primarypurple} ''' + format_currency(mpsp) + r'''}

\vspace{1cm}

\subsection*{Valuation Multiples}

This price was determined using a market-based approach which examined ''' + str(data.get('comparable_transactions', {}).get('count', 0)) + r''' comparable transactions. These transactions included businesses with revenues between ''' + format_currency(data.get('comparable_transactions', {}).get('revenue_range', [0, 0])[0]) + r''' and ''' + format_currency(data.get('comparable_transactions', {}).get('revenue_range', [0, 0])[1]) + r'''. An asking price of ''' + format_currency(mpsp) + r''' represents the following valuation multiples:
\end{minipage}%
\hfill
\begin{minipage}[t]{0.4\textwidth}
\vspace{0pt}
\vspace{2.5cm}
\begin{tabular}{|>{\raggedright}p{3cm}|r|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Valuation Metric}} & \textcolor{white}{\textbf{Multiple}} \\
\hline
\rowcolor{tableodd}
Revenue & ''' + str(data.get('valuation', {}).get('revenue_multiple', 0)) + r''' \\
\hline
\rowcolor{white}
SDE & ''' + str(data.get('valuation', {}).get('sde_multiple', 0)) + r''' \\
\hline
\rowcolor{tableodd}
Adj. EBITDA & ''' + str(data.get('valuation', {}).get('adj_ebitda_multiple', 0)) + r''' \\
\hline
\end{tabular}
\end{minipage}

\vspace{0.5cm}

See Appendix A for comparable transactions.

\clearpage
'''

    # Company Overview Section
    fin_data = data.get('financial_data', {})
    years = fin_data.get('years', [''] * 5)
    
    # Calculate gross profit percentages
    gp_pcts = []
    for i in range(len(years)):
        try:
            gp_pct = calculate_gross_profit_percent(
                fin_data.get('gross_profit', [0]*5)[i],
                fin_data.get('revenue', [0]*5)[i]
            )
            gp_pcts.append(gp_pct)
        except (IndexError, TypeError):
            gp_pcts.append(0)
    
    # Calculate net income percentages
    ni_pcts = []
    for i in range(len(years)):
        try:
            ni_pct = calculate_net_income_percent(
                fin_data.get('net_income', [0]*5)[i],
                fin_data.get('revenue', [0]*5)[i]
            )
            ni_pcts.append(ni_pct)
        except (IndexError, TypeError):
            ni_pcts.append(0)
    
    norm = data.get('normalizations', {})
    
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
\textbf{Total Revenue} & ''' + format_currency(fin_data.get('revenue', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('revenue', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('revenue', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('revenue', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('revenue', [0]*5)[0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Total Cost of Goods} & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[0]) + r''' \\
\hline
\rowcolor{tableodd}
\textbf{Gross Profit} & ''' + format_currency(fin_data.get('gross_profit', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('gross_profit', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('gross_profit', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('gross_profit', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('gross_profit', [0]*5)[0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Total Expenses} & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[0]) + r''' \\
\hline
\rowcolor{tableodd}
\textbf{Net Income} & ''' + format_currency(fin_data.get('net_income', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('net_income', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('net_income', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('net_income', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('net_income', [0]*5)[0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Total Normalizations} & ''' + format_currency(norm.get('total_adjustments', [0]*5)[4]) + r''' & ''' + format_currency(norm.get('total_adjustments', [0]*5)[3]) + r''' & ''' + format_currency(norm.get('total_adjustments', [0]*5)[2]) + r''' & ''' + format_currency(norm.get('total_adjustments', [0]*5)[1]) + r''' & ''' + format_currency(norm.get('total_adjustments', [0]*5)[0]) + r''' \\
\hline
\rowcolor{tableodd}
\textbf{SDE} & ''' + format_currency(norm.get('sde', [0]*5)[4]) + r''' & ''' + format_currency(norm.get('sde', [0]*5)[3]) + r''' & ''' + format_currency(norm.get('sde', [0]*5)[2]) + r''' & ''' + format_currency(norm.get('sde', [0]*5)[1]) + r''' & ''' + format_currency(norm.get('sde', [0]*5)[0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Adj. EBITDA} & ''' + format_currency(norm.get('adj_ebitda', [0]*5)[4]) + r''' & ''' + format_currency(norm.get('adj_ebitda', [0]*5)[3]) + r''' & ''' + format_currency(norm.get('adj_ebitda', [0]*5)[2]) + r''' & ''' + format_currency(norm.get('adj_ebitda', [0]*5)[1]) + r''' & ''' + format_currency(norm.get('adj_ebitda', [0]*5)[0]) + r''' \\
\hline
\rowcolor{tableodd}
\textbf{Year Weighting} & ''' + str(norm.get('year_weighting', [0]*5)[4]) + r'''\% & ''' + str(norm.get('year_weighting', [0]*5)[3]) + r'''\% & ''' + str(norm.get('year_weighting', [0]*5)[2]) + r'''\% & ''' + str(norm.get('year_weighting', [0]*5)[1]) + r'''\% & ''' + str(norm.get('year_weighting', [0]*5)[0]) + r'''\% \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{tabular}{ll}
\textbf{Weighted Average of Revenue} & ''' + format_currency(data.get('valuation', {}).get('weighted_avg_revenue', 0)) + r''' \\
\textbf{MPSP Multiple of Revenue} & ''' + str(data.get('valuation', {}).get('revenue_multiple', 0)) + r''' \\
\textbf{Weighted Average of SDE} & ''' + format_currency(data.get('valuation', {}).get('weighted_avg_sde', 0)) + r''' \\
\textbf{MPSP Multiple of SDE} & ''' + str(data.get('valuation', {}).get('sde_multiple', 0)) + r''' \\
\end{tabular}

\vspace{0.3cm}

\textit{\small Note: Projected year is calculated average growth rate of each item.}

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

\begin{minipage}[t]{0.48\textwidth}
\vspace{0pt}
\includegraphics[width=\textwidth]{science.png}
\end{minipage}%
\hfill
\begin{minipage}[t]{0.48\textwidth}
\vspace{0pt}
Based on information you provide in the financial tables, the report then assigns your business a median business value. That means that if the report finds 15 businesses that were similar it would assign your business the middle value.
\end{minipage}

\vspace{0.5cm}

\subsection*{The Art}

\begin{minipage}[t]{0.48\textwidth}
\vspace{0pt}
The next part of the process involves taking the answers to the questions we ask and trying to determine if your business is more or less attractive than average.
\end{minipage}%
\hfill
\begin{minipage}[t]{0.48\textwidth}
\vspace{0pt}
\includegraphics[width=\textwidth]{art.png}
\end{minipage}

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
Revenue & ''' + format_currency(fin_data.get('revenue', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('revenue', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('revenue', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('revenue', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('revenue', [0]*5)[0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Total Revenue} & ''' + format_currency(fin_data.get('revenue', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('revenue', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('revenue', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('revenue', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('revenue', [0]*5)[0]) + r''' \\
\hline
\multicolumn{6}{|l|}{\textbf{Cost of Goods}} \\
\hline
\rowcolor{tableodd}
Cost of Sales & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Total Cost of Goods} & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('cost_of_goods', [0]*5)[0]) + r''' \\
\hline
\rowcolor{tableodd}
\textbf{Gross Profit} & ''' + format_currency(fin_data.get('gross_profit', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('gross_profit', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('gross_profit', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('gross_profit', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('gross_profit', [0]*5)[0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Gross Profit \%} & ''' + format_percent(gp_pcts[4]) + r''' & ''' + format_percent(gp_pcts[3]) + r''' & ''' + format_percent(gp_pcts[2]) + r''' & ''' + format_percent(gp_pcts[1]) + r''' & ''' + format_percent(gp_pcts[0]) + r''' \\
\hline
\multicolumn{6}{|l|}{\textbf{Expenses}} \\
\hline
\rowcolor{tableodd}
General Expense & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[0]) + r''' \\
\hline
\rowcolor{white}
\textbf{Total Expenses} & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('total_expenses', [0]*5)[0]) + r''' \\
\hline
\multicolumn{6}{|l|}{\textbf{Other Income}} \\
\hline
\rowcolor{tableodd}
- & ''' + (format_currency(fin_data.get('other_income', [0]*5)[4]) if fin_data.get('other_income', [0]*5)[4] > 0 else '\\$-') + r''' & ''' + (format_currency(fin_data.get('other_income', [0]*5)[3]) if fin_data.get('other_income', [0]*5)[3] > 0 else '\\$-') + r''' & ''' + (format_currency(fin_data.get('other_income', [0]*5)[2]) if fin_data.get('other_income', [0]*5)[2] > 0 else '\\$-') + r''' & ''' + (format_currency(fin_data.get('other_income', [0]*5)[1]) if fin_data.get('other_income', [0]*5)[1] > 0 else '\\$-') + r''' & ''' + (format_currency(fin_data.get('other_income', [0]*5)[0]) if fin_data.get('other_income', [0]*5)[0] > 0 else '\\$-') + r''' \\
\hline
\rowcolor{white}
\textbf{Net Income} & ''' + format_currency(fin_data.get('net_income', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('net_income', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('net_income', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('net_income', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('net_income', [0]*5)[0]) + r''' \\
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
Net Income & ''' + format_currency(fin_data.get('net_income', [0]*5)[4]) + r''' & ''' + format_currency(fin_data.get('net_income', [0]*5)[3]) + r''' & ''' + format_currency(fin_data.get('net_income', [0]*5)[2]) + r''' & ''' + format_currency(fin_data.get('net_income', [0]*5)[1]) + r''' & ''' + format_currency(fin_data.get('net_income', [0]*5)[0]) + r''' & \\
\hline
\rowcolor{white}
Discretionary Expense & ''' + format_currency(norm.get('discretionary_expense', [0]*5)[4]) + r''' & ''' + format_currency(norm.get('discretionary_expense', [0]*5)[3]) + r''' & ''' + format_currency(norm.get('discretionary_expense', [0]*5)[2]) + r''' & ''' + format_currency(norm.get('discretionary_expense', [0]*5)[1]) + r''' & ''' + format_currency(norm.get('discretionary_expense', [0]*5)[0]) + r''' & \\
\hline
\rowcolor{tableodd}
Amortization & ''' + format_currency(norm.get('amortization', [0]*5)[4]) + r''' & ''' + format_currency(norm.get('amortization', [0]*5)[3]) + r''' & ''' + format_currency(norm.get('amortization', [0]*5)[2]) + r''' & ''' + format_currency(norm.get('amortization', [0]*5)[1]) + r''' & ''' + format_currency(norm.get('amortization', [0]*5)[0]) + r''' & \\
\hline
\rowcolor{white}
Interest on Equipment & ''' + format_currency(norm.get('interest_capital_lease', [0]*5)[4]) + r''' & ''' + format_currency(norm.get('interest_capital_lease', [0]*5)[3]) + r''' & ''' + format_currency(norm.get('interest_capital_lease', [0]*5)[2]) + r''' & ''' + format_currency(norm.get('interest_capital_lease', [0]*5)[1]) + r''' & ''' + format_currency(norm.get('interest_capital_lease', [0]*5)[0]) + r''' & \\
\hline
\rowcolor{tableodd}
Management Salary & ''' + format_currency(norm.get('management_salary', [0]*5)[4]) + r''' & ''' + format_currency(norm.get('management_salary', [0]*5)[3]) + r''' & ''' + format_currency(norm.get('management_salary', [0]*5)[2]) + r''' & ''' + format_currency(norm.get('management_salary', [0]*5)[1]) + r''' & ''' + format_currency(norm.get('management_salary', [0]*5)[0]) + r''' & \\
\hline
\rowcolor{white}
\textbf{Total Adjustments} & ''' + format_currency(norm.get('total_adjustments', [0]*5)[4]) + r''' & ''' + format_currency(norm.get('total_adjustments', [0]*5)[3]) + r''' & ''' + format_currency(norm.get('total_adjustments', [0]*5)[2]) + r''' & ''' + format_currency(norm.get('total_adjustments', [0]*5)[1]) + r''' & ''' + format_currency(norm.get('total_adjustments', [0]*5)[0]) + r''' & \\
\hline
\rowcolor{tableodd}
\textbf{SDE} & ''' + format_currency(norm.get('sde', [0]*5)[4]) + r''' & ''' + format_currency(norm.get('sde', [0]*5)[3]) + r''' & ''' + format_currency(norm.get('sde', [0]*5)[2]) + r''' & ''' + format_currency(norm.get('sde', [0]*5)[1]) + r''' & ''' + format_currency(norm.get('sde', [0]*5)[0]) + r''' & \\
\hline
\rowcolor{white}
Replace owner & ''' + format_currency(norm.get('manager_salary', [0]*5)[4]) + r''' & ''' + format_currency(norm.get('manager_salary', [0]*5)[3]) + r''' & ''' + format_currency(norm.get('manager_salary', [0]*5)[2]) + r''' & ''' + format_currency(norm.get('manager_salary', [0]*5)[1]) + r''' & ''' + format_currency(norm.get('manager_salary', [0]*5)[0]) + r''' & \\
\hline
\rowcolor{tableodd}
\textbf{Adjusted EBITDA} & ''' + format_currency(norm.get('adj_ebitda', [0]*5)[4]) + r''' & ''' + format_currency(norm.get('adj_ebitda', [0]*5)[3]) + r''' & ''' + format_currency(norm.get('adj_ebitda', [0]*5)[2]) + r''' & ''' + format_currency(norm.get('adj_ebitda', [0]*5)[1]) + r''' & ''' + format_currency(norm.get('adj_ebitda', [0]*5)[0]) + r''' & \\
\hline
\rowcolor{white}
\textbf{Year Weighting} & ''' + str(norm.get('year_weighting', [0]*5)[4]) + r'''\% & ''' + str(norm.get('year_weighting', [0]*5)[3]) + r'''\% & ''' + str(norm.get('year_weighting', [0]*5)[2]) + r'''\% & ''' + str(norm.get('year_weighting', [0]*5)[1]) + r'''\% & ''' + str(norm.get('year_weighting', [0]*5)[0]) + r'''\% & \\
\hline
\end{tabular}
\end{center}

\vspace{0.3cm}

\textit{\small Note: Projected year is calculated from the year to date statement from January 1 to September 30.}

\vspace{0.5cm}

\subsection*{Adjusted EBITDA}

In its simplest definition, adjusted EBITDA is a measure of a company's financial performance, acting as an alternative to other metrics like revenue, earnings or net income.

Adjusted EBITDA is how many people determine business value as it places the focus on the financial outcome of operating decisions. It does this by removing the impacts of non-operating decisions made by the existing management, such as interest expenses, tax rates, or significant intangible assets. This leaves a figure that better reflects the operating profitability of a business, one that can effectively be compared between companies by owners, buyers and investors. It is for that reason many employ adjusted EBITDA over other metrics when deciding which organization is more attractive.

\clearpage

\subsection*{What does EBITDA stand for?}

\begin{description}[style=nextline,leftmargin=0cm,itemsep=8pt]
\item[\textbf{E --- Earnings}] How much money a company makes.
\item[\textbf{B --- Before}] 
\item[\textbf{I --- Interest}] The expenses to a business caused by interest rates, such as loans provided by a bank or similar third-party.
\item[\textbf{T --- Taxes}] The expenses to a business caused by tax rates imposed by their city, state, and country.
\item[\textbf{D --- Depreciation}] A non-cash expense referring to the gradual reduction in value of a company's assets.
\item[\textbf{A --- Amortization}] A non-cash expense referring to the cost of intangible (non-balance sheet) assets over time.
\end{description}

\subsection*{SDE}

Business owners often try to optimize the taxes they pay each year. As a result, it is not uncommon for a company to appear to make less money, `on paper.' For example, a company's profits are reduced if the owner takes a salary from their business, as that wage appears is an expense. However, this is money in the pocket of the business owner.

Therefore, we use Seller's Discretionary Earnings (SDE) as a better way to show the profitability of an owner/operator business. To calculate SDE we add back all the benefits the owner receives from the business to Net Income (owner salaries, depreciation/amortization, etc.).

\clearpage
'''

    # Industry Benchmarks
    bench = data.get('industry_benchmarks', {})
    latex += r'''\section*{Industry Benchmarks}
\addcontentsline{toc}{section}{Industry Benchmarks}

The table below compares your financial performance to ''' + f"{bench.get('sample_size', 0):,}" + r''' other businesses in your industry using data from Statistics Canada. Benchmarking data is created using a sample of Revenue Canada tax returns for incorporated businesses operating in Canada. To start increasing your valuation, focus on areas labelled `Improvement Opportunity' in the analysis column.

\vspace{0.5cm}

\begin{center}
\begin{tabular}{|l|r|r|r|}
\hline
\rowcolor{tableheader}
\textcolor{white}{} & \textcolor{white}{\textbf{Your Average}} & \textcolor{white}{\textbf{Industry Average}} & \textcolor{white}{\textbf{Analysis}} \\
\hline
\rowcolor{tableodd}
Cost of Goods & ''' + format_percent(bench.get('your_cost_of_goods', 0)) + r''' & ''' + format_percent(bench.get('cost_of_goods_avg', 0)) + r''' & Good \\
\hline
\rowcolor{white}
Total Expenses & ''' + format_percent(bench.get('your_total_expenses', 0)) + r''' & ''' + format_percent(bench.get('total_expenses_avg', 0)) + r''' & Good \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\textit{\small * Note: Depending on how your accountant prepares your financial statements, your salaries \& wages and/or direct wages may appear high or low.}

\vspace{0.3cm}

On average, total employment costs in your industry are ''' + format_percent(bench.get('total_employment_costs_avg', 0)) + r''' of revenue. In comparison, your total employment costs are ''' + format_percent(bench.get('your_employment_costs', 0)) + r'''.

\clearpage
'''

    # Scorecard Section
    latex += r'''\section*{Scorecard}
\addcontentsline{toc}{section}{Scorecard}

\subsection*{Valuation Range}

Sometimes the numbers don't represent the true value of a business. Scorecard values can change the valuation by +/- 25\% of the base valuation. The chart below show the valuation range for ''' + company_name + r''' based on the scorecard answers. A totally optimized scorecard would give a business valuation of ''' + format_currency(max_val) + r'''.

\vspace{0.5cm}

\begin{center}
\begin{tikzpicture}[scale=0.9]
% Draw the gray bar
\fill[lightgray] (0,0) rectangle (12,0.6);
% Draw the scale lines
\draw[thick] (0,0) -- (0,0.6);
\draw[thick] (12,0) -- (12,0.6);
% Draw the purple circle
\fill[primarypurple] (''' + str(12 * (mpsp - min_val) / (max_val - min_val)) + r''',0.3) circle (0.35);
% Add labels below
\node[anchor=north,font=\small] at (0,-0.2) {''' + format_currency(min_val) + r'''};
\node[anchor=north,font=\bfseries\large] at (6,-0.2) {''' + format_currency(mpsp) + r'''};
\node[anchor=north,font=\small] at (12,-0.2) {''' + format_currency(max_val) + r'''};
\end{tikzpicture}
\end{center}

\vspace{0.5cm}

\subsection*{Section Breakdown}

The following tables break down the qualitative analysis of ''' + company_name + r'''. Each section shows how your answers affect your overall valuation. Use the chart below each table as a guide to find areas of improvement in your business. Start with the sections where your score falls below the mid line as these are generally the areas where you will see the biggest impact in your valuation.

\clearpage
'''

    # Finance and Operations Section
    sections = data.get('scorecard', {}).get('sections', {})
    fin_ops = sections.get('finance_operations', {})
    fin_ops_range = sections_range.get('finance_operations', 0)
    fin_ops_score = fin_ops.get('scores', {}).get('average', 3)
    
    # Escape answers for LaTeX
    fin_ops_questions = fin_ops.get('questions', {})
    fin_ops_answers = {
        'documented_processes': escape_latex(fin_ops_questions.get('documented_processes', '')),
        'accountant': escape_latex(fin_ops_questions.get('accountant', '')),
        'annual_budget': escape_latex(fin_ops_questions.get('annual_budget', '')),
        'payables_on_time': escape_latex(fin_ops_questions.get('payables_on_time', ''))
    }
    
    latex += r'''\subsection*{Finance and General Operations +/- ''' + str(fin_ops.get('weight', 0)) + r'''\% of valuation}

\begin{center}
\small
\begin{tabular}{|>{\raggedright\arraybackslash}p{9.5cm}|>{\raggedright\arraybackslash}p{4cm}|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
\hline
\rowcolor{tableodd}
Businesses typically have higher valuations when processes are documented. Does your firm have documented systemized business processes? & ''' + fin_ops_answers['documented_processes'] + r''' \\
\hline
\rowcolor{white}
Do you hire an accountant to prepare your year-end Financial Statements and/or tax returns? & ''' + fin_ops_answers['accountant'] + r''' \\
\hline
\rowcolor{tableodd}
Do you prepare an annual operating budget? & ''' + fin_ops_answers['annual_budget'] + r''' \\
\hline
\rowcolor{white}
Are your payables always paid in full and on-time? & ''' + fin_ops_answers['payables_on_time'] + r''' \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{center}
''' + generate_scorecard_scale(fin_ops_score, -fin_ops_range, fin_ops_range) + r'''
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
    owner_dep = sections.get('owner_dependency', {})
    owner_dep_range = sections_range.get('owner_dependency', 0)
    owner_dep_score = owner_dep.get('scores', {}).get('average', 3)
    
    owner_dep_questions = owner_dep.get('questions', {})
    owner_dep_answers = {
        'thrive_without_owner': escape_latex(owner_dep_questions.get('thrive_without_owner', '')),
        'vacation_over_month': escape_latex(owner_dep_questions.get('vacation_over_month', '')),
        'customers_ask_by_name_pct': escape_latex(str(owner_dep_questions.get('customers_ask_by_name_pct', '')))
    }
    
    latex += r'''\subsection*{Owner Dependency +/- ''' + str(owner_dep.get('weight', 0)) + r'''\% of valuation}

\begin{center}
\small
\begin{tabular}{|>{\raggedright\arraybackslash}p{9.5cm}|>{\raggedright\arraybackslash}p{4cm}|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
\hline
\rowcolor{tableodd}
Would your company thrive if you left for 2 months? & ''' + owner_dep_answers['thrive_without_owner'] + r''' \\
\hline
\rowcolor{white}
Have you taken a vacation longer than 1 month in the past 2 years? & ''' + owner_dep_answers['vacation_over_month'] + r''' \\
\hline
\rowcolor{tableodd}
On a normal day, what percentage of customers ask for you by name? & ''' + owner_dep_answers['customers_ask_by_name_pct'] + r''' \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{center}
''' + generate_scorecard_scale(owner_dep_score, -owner_dep_range, owner_dep_range) + r'''
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
    growth = sections.get('growth_potential', {})
    growth_range = sections_range.get('growth_potential', 0)
    growth_score = growth.get('scores', {}).get('average', 3)
    
    growth_questions = growth.get('questions', {})
    growth_answers = {
        'identified_opportunities': escape_latex(growth_questions.get('identified_opportunities', '')),
        'revenue_increase_capacity': escape_latex(str(growth_questions.get('revenue_increase_capacity', '')))
    }
    
    latex += r'''\subsection*{Growth Potential +/- ''' + str(growth.get('weight', 0)) + r'''\% of valuation}

\begin{center}
\small
\begin{tabular}{|>{\raggedright\arraybackslash}p{9.5cm}|>{\raggedright\arraybackslash}p{4cm}|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
\hline
\rowcolor{tableodd}
Have you identified growth opportunities in your business? & ''' + growth_answers['identified_opportunities'] + r''' \\
\hline
\rowcolor{white}
In your current space and with your current equipment, by how much could you increase revenues? & ''' + growth_answers['revenue_increase_capacity'] + r''' \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{center}
''' + generate_scorecard_scale(growth_score, -growth_range, growth_range) + r'''
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
    recurring = sections.get('recurring_revenues', {})
    recurring_range = sections_range.get('recurring_revenues', 0)
    recurring_score = recurring.get('scores', {}).get('average', 3)
    
    recurring_questions = recurring.get('questions', {})
    recurring_answer = escape_latex(recurring_questions.get('revenue_model', ''))
    
    latex += r'''\subsection*{Recurring Revenues +/- ''' + str(recurring.get('weight', 0)) + r'''\% of valuation}

\begin{center}
\small
\begin{tabular}{|>{\raggedright\arraybackslash}p{9.5cm}|>{\raggedright\arraybackslash}p{4cm}|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
\hline
\rowcolor{tableodd}
Which one of these best describes your revenue model? & ''' + recurring_answer + r''' \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{center}
''' + generate_scorecard_scale(recurring_score, -recurring_range, recurring_range) + r'''
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
    org_stab = sections.get('organizational_stability', {})
    org_stab_range = sections_range.get('organizational_stability', 0)
    org_stab_score = org_stab.get('scores', {}).get('average', 3)
    
    org_stab_questions = org_stab.get('questions', {})
    org_stab_answers = {
        'largest_customer_pct': escape_latex(org_stab_questions.get('largest_customer_pct', '')),
        'top_5_customers_pct': escape_latex(str(org_stab_questions.get('top_5_customers_pct', ''))),
        'replace_sales_person': escape_latex(org_stab_questions.get('replace_sales_person', '')),
        'replace_delivery_person': escape_latex(org_stab_questions.get('replace_delivery_person', '')),
        'replace_supplier': escape_latex(org_stab_questions.get('replace_supplier', ''))
    }
    
    latex += r'''\subsection*{Organizational Stability +/- ''' + str(org_stab.get('weight', 0)) + r'''\% of valuation}

\begin{center}
\small
\begin{tabular}{|>{\raggedright\arraybackslash}p{9.5cm}|>{\raggedright\arraybackslash}p{4cm}|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
\hline
\rowcolor{tableodd}
How much revenue does your largest customer represent? & ''' + org_stab_answers['largest_customer_pct'] + r''' \\
\hline
\rowcolor{white}
How much revenue does your 5 largest customers represent? & ''' + org_stab_answers['top_5_customers_pct'] + r''' \\
\hline
\rowcolor{tableodd}
If this person isn't you, could you easily replace the person most responsible for sales and marketing in your business? & ''' + org_stab_answers['replace_sales_person'] + r''' \\
\hline
\rowcolor{white}
If this person isn't you, could you easily replace the person most responsible for product/service design and delivery in your business? & ''' + org_stab_answers['replace_delivery_person'] + r''' \\
\hline
\rowcolor{tableodd}
Could you easily replace the most important outside supplier to your business? & ''' + org_stab_answers['replace_supplier'] + r''' \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{center}
''' + generate_scorecard_scale(org_stab_score, -org_stab_range, org_stab_range) + r'''
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
    sales = sections.get('sales_marketing', {})
    sales_range = sections_range.get('sales_marketing', 0)
    sales_score = sales.get('scores', {}).get('average', 3)
    
    sales_questions = sales.get('questions', {})
    sales_answers = {
        'customer_feedback': escape_latex(sales_questions.get('customer_feedback', '')),
        'marketing_spend_pct': escape_latex(sales_questions.get('marketing_spend_pct', '')),
        'google_first_page': escape_latex(sales_questions.get('google_first_page', '')),
        'written_acquisition_strategy': escape_latex(sales_questions.get('written_acquisition_strategy', ''))
    }
    
    latex += r'''\subsection*{Sales and Marketing +/- ''' + str(sales.get('weight', 0)) + r'''\% of valuation}

\begin{center}
\small
\begin{tabular}{|>{\raggedright\arraybackslash}p{9.5cm}|>{\raggedright\arraybackslash}p{4cm}|}
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{Question}} & \textcolor{white}{\textbf{Answer}} \\
\hline
\rowcolor{tableodd}
Do you collect customer feedback with a documented process? & ''' + sales_answers['customer_feedback'] + r''' \\
\hline
\rowcolor{white}
How much do you spend on marketing as a percentage of gross revenue? & ''' + sales_answers['marketing_spend_pct'] + r''' \\
\hline
\rowcolor{tableodd}
Do you show up on the first page on a local Google search in your industry? & ''' + sales_answers['google_first_page'] + r''' \\
\hline
\rowcolor{white}
Do you have a written customer acquisition strategy? & ''' + sales_answers['written_acquisition_strategy'] + r''' \\
\hline
\end{tabular}
\end{center}

\vspace{0.5cm}

\begin{center}
''' + generate_scorecard_scale(sales_score, -sales_range, sales_range) + r'''
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
\textcolor{white}{\textbf{NAICS}} & \textcolor{white}{\textbf{Revenue}} & \textcolor{white}{\textbf{SDE}} & \textcolor{white}{\textbf{Adj. EBITDA}} & \textcolor{white}{\textbf{Price}} & \textcolor{white}{\textbf{Rev Mult}} & \textcolor{white}{\textbf{SDE Mult}} & \textcolor{white}{\textbf{EBITDA Mult}} \\
\hline
\endfirsthead
\hline
\rowcolor{tableheader}
\textcolor{white}{\textbf{NAICS}} & \textcolor{white}{\textbf{Revenue}} & \textcolor{white}{\textbf{SDE}} & \textcolor{white}{\textbf{Adj. EBITDA}} & \textcolor{white}{\textbf{Price}} & \textcolor{white}{\textbf{Rev Mult}} & \textcolor{white}{\textbf{SDE Mult}} & \textcolor{white}{\textbf{EBITDA Mult}} \\
\hline
\endhead
'''

    # Add transaction rows
    transactions = data.get('comparable_transactions', {}).get('transactions', [])
    for i, trans in enumerate(transactions):
        row_color = "tableodd" if i % 2 == 0 else "white"
        latex += r'''\rowcolor{''' + row_color + r'''}
''' + str(trans.get('naics', '')) + r''' & ''' + format_currency(trans.get('revenue', 0)) + r''' & ''' + format_currency(trans.get('sde', 0)) + r''' & ''' + format_currency(trans.get('adj_ebitda', 0)) + r''' & ''' + format_currency(trans.get('price', 0)) + r''' & ''' + str(trans.get('rev_mult', 0)) + r''' & ''' + str(trans.get('sde_mult', 0)) + r''' & ''' + str(trans.get('ebitda_mult', 0)) + r''' \\
\hline
'''

    latex += r'''\end{longtable}
\end{center}

\end{document}'''

    return latex


def main():
    """Main function to generate the report"""
    
    print("=" * 70)
    print("BUSINESS VALUATION REPORT GENERATOR")
    print("=" * 70)
    print()
    
    # Check command line arguments
    if len(sys.argv) != 2:
        print("ERROR: Incorrect usage.")
        print()
        print("Usage: python generate_report.py <data_file.json>")
        print()
        print("Example: python generate_report.py report_data.json")
        sys.exit(1)
    
    data_file = sys.argv[1]
    
    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"ERROR: Data file '{data_file}' not found.")
        print()
        print("Please ensure the JSON file exists in the current directory.")
        sys.exit(1)
    
    # Check if required images exist
    required_images = ['Chinook_logo.png', 'science.png', 'art.png']
    missing_images = [img for img in required_images if not os.path.exists(img)]
    
    if missing_images:
        print("WARNING: Missing required image files:")
        for img in missing_images:
            print(f"  - {img}")
        print()
        print("The report will fail to compile without these images.")
        print("Please place the image files in the same directory as this script.")
        print()
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Load data
    print(f"Loading data from {data_file}...")
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        print("✓ Data loaded successfully")
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON format in file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to read file: {e}")
        sys.exit(1)
    
    print()
    
    # Generate LaTeX
    print("Generating LaTeX document...")
    try:
        latex_content = generate_latex(data)
        print("✓ LaTeX content generated")
    except Exception as e:
        print(f"ERROR: Failed to generate LaTeX: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print()
    
    # Write to file
    output_file = 'valuation_report.tex'
    print(f"Writing to {output_file}...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        print("✓ LaTeX file written successfully")
    except Exception as e:
        print(f"ERROR: Failed to write file: {e}")
        sys.exit(1)
    
    print()
    print("=" * 70)
    print("SUCCESS! LaTeX file generated:", output_file)
    print("=" * 70)
    print()
    print("Next steps:")
    print()
    print("1. Compile the PDF:")
    print(f"   pdflatex {output_file}")
    print(f"   pdflatex {output_file}  (run twice for TOC)")
    print()
    print("   OR")
    print()
    print(f"   latexmk -pdf {output_file}")
    print()
    print("2. Make sure you have in the same directory:")
    print("   - Chinook_logo.png")
    print("   - science.png")
    print("   - art.png")
    print("   - A LaTeX distribution (TeX Live, MiKTeX, etc.)")
    print()


if __name__ == "__main__":
    main()