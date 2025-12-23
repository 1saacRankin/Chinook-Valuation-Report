"""
Professional Valuation Report Generator - Complete Enhanced Version
Matches the exact PDF format with professional styling
"""

from pathlib import Path

OUTPUT_FOLDER = "valuation_report_output"

def create_professional_quarto_template():
    """Create a professional Quarto template matching the PDF exactly"""
    
    template = r'''---
title: ""
date: ""
format:
  pdf:
    documentclass: report
    papersize: letter
    number-sections: false
    toc: true
    toc-depth: 2
    toc-title: "Table of Contents"
    geometry:
      - top=0.75in
      - bottom=0.75in
      - left=0.75in
      - right=0.75in
    include-in-header:
      text: |
        \usepackage{fancyhdr}
        \usepackage{graphicx}
        \usepackage{xcolor}
        \usepackage{tcolorbox}
        \usepackage{booktabs}
        \usepackage{longtable}
        \usepackage{array}
        \usepackage{multirow}
        \usepackage{colortbl}
        \usepackage{fontspec}
        \usepackage{titling}
        \usepackage{lastpage}
        \setmainfont{Arial}
        
        % Define exact colors from the PDF
        \definecolor{darkblue}{RGB}{0,51,102}
        \definecolor{mediumblue}{RGB}{41,98,155}
        \definecolor{lightblue}{RGB}{230,240,250}
        \definecolor{tableheader}{RGB}{68,114,196}
        \definecolor{lightgray}{RGB}{242,242,242}
        \definecolor{tablegray}{RGB}{217,217,217}
        \definecolor{accentblue}{RGB}{100,150,220}
        
        % Better table column padding
        \setlength{\tabcolsep}{10pt}
        
        % Custom title page
        \renewcommand{\maketitle}{
          \begin{titlepage}
            \centering
            \vspace*{1.5cm}
            
            \includegraphics[width=4.5in]{Chinook_logo.png}
            
            \vspace{2.5cm}
            
            {\fontsize{36}{44}\selectfont\bfseries\color{darkblue} Most Probable Selling Price Report\par}
            
            \vspace{2cm}
            
            {\fontsize{26}{32}\selectfont\bfseries\color{mediumblue} {{< var company_name >}}\par}
            
            \vspace{1.5cm}
            
            {\fontsize{16}{20}\selectfont\color{darkblue} {{< var report_date >}}\par}
            
            \vfill
          \end{titlepage}
          \newpage
        }
        
        % Header and footer for content pages
        \pagestyle{fancy}
        \fancyhf{}
        \fancyhead[L]{\includegraphics[height=0.4in]{Chinook_logo.png}}
        \fancyhead[R]{\thepage}
        \renewcommand{\headrulewidth}{0.4pt}
        \fancyfoot[C]{}
        
        % Style for first page (no header)
        \fancypagestyle{plain}{
          \fancyhf{}
          \fancyfoot[C]{\thepage}
          \renewcommand{\headrulewidth}{0pt}
        }
        
        % MPSP Box - prominent and professional
        \newtcolorbox{mpspbox}{
          enhanced,
          colback=lightblue,
          colframe=mediumblue,
          boxrule=3pt,
          arc=2pt,
          boxsep=20pt,
          left=25pt,
          right=25pt,
          top=25pt,
          bottom=25pt,
          shadow={2mm}{-2mm}{0mm}{black!20}
        }
        
        % Valuation range box - clean and clear
        \newtcolorbox{rangebox}{
          enhanced,
          colback=lightblue!30,
          colframe=mediumblue,
          boxrule=2.5pt,
          arc=2pt,
          boxsep=15pt,
          left=20pt,
          right=20pt,
          top=20pt,
          bottom=20pt,
          shadow={1.5mm}{-1.5mm}{0mm}{black!15}
        }
        
        % Info box for company details - subtle and professional
        \newtcolorbox{infobox}{
          enhanced,
          colback=lightgray,
          colframe=mediumblue,
          boxrule=2pt,
          arc=2pt,
          boxsep=12pt,
          left=15pt,
          right=15pt,
          top=15pt,
          bottom=15pt
        }
        
        % Table styling
        \renewcommand{\arraystretch}{1.4}
        
        % Custom section formatting - modern and clean
        \usepackage{titlesec}
        \titleformat{\section}
          {\normalfont\fontsize{18}{22}\bfseries\color{darkblue}}
          {}{0em}{}[\titlerule]
        \titlespacing*{\section}{0pt}{24pt}{12pt}
        
        \titleformat{\subsection}
          {\normalfont\fontsize{15}{18}\bfseries\color{mediumblue}}
          {}{0em}{}
        \titlespacing*{\subsection}{0pt}{18pt}{8pt}
        
        \titleformat{\subsubsection}
          {\normalfont\fontsize{13}{16}\bfseries\color{mediumblue}}
          {}{0em}{}
        \titlespacing*{\subsubsection}{0pt}{12pt}{6pt}
          
execute:
  echo: false
  warning: false
  message: false
---

\maketitle

\newpage

\tableofcontents

\newpage

# Purpose & Scope {.unnumbered}

This report will provide an opinion of the Most Probable Selling Price ('MPSP') to the User, where the User is the Client or the agent or representative of the Client (the 'User').

This is the price for the enterprise (the 'Business') and its assets if to be sold as a going concern. This price includes normal inventory but does not include any other components of working capital.

The purpose of this report is to provide an opinion of the Business's MPSP. **It is not intended to be a formal valuation of the business, enterprise, or the assets thereof.** It is a limited assessment of the MPSP, which is defined by the International Business Brokers Association (IBBA) as:

\begin{quote}
\textit{"That price for the assets or shares intended for sale which represents the total consideration most likely to be established between a buyer and a seller considering compulsion on the part of either the buyer or the seller, and potential financial strategic or non-financial benefits to the seller and probable buyer"}
\end{quote}

This report is intended for the sole use of the User and specifically for the purpose cited herein; all others possessing this report are not intended users. The use of this report by anyone other than the intended person and for the intended purpose, is not authorized.

## Valuation Assumptions

The generation of this report relied upon:

1. A qualitative questionnaire completed by the user.
2. The Income Statements and/or Balance Sheets provided by the user.
3. Comparable transaction data.

## General Assumptions

The following assumptions were made when preparing this report:

1. The Business is a sole proprietorship, legal partnership, or a corporation.
2. The Business has no contingent liabilities, unusual contractual obligations, or substantial commitments, other than in the ordinary course of business.
3. The Business has no litigation pending or threatened.
4. Chinook Business Advisory did not audit or otherwise verify the financial information submitted.

\newpage

# Disclaimer {.unnumbered}

Chinook Business Advisory does not warrant any information contained herein and is not responsible for any results whatsoever as a result of, or as a consequence of, using the information provided in this report. It is understood that market conditions are variable, business operations and the perceived risks associated with them are subject to change, and that the motivations of both Purchasers and Vendors may differ and result in an ultimate sale price either higher or lower than predicted in the report. The valuation of the business assets, goodwill and/or share value is not warranted in any way.

The User has supplied the information contained in this report. Chinook Business Advisory has not audited or otherwise confirmed this information and makes no representations, expressed or implied, as to its accuracy or completeness or the conclusions to be drawn and shall in no way be responsible for the content, accuracy and truthfulness of such information.

The information presented in this report is the result of the User's input, representations and calculations. Additional information, such as market data from reliable sources, will also be considered. The Report will contain information and conclusions deemed to be relevant to the User but is offered without any guarantees or warranties relating to specific statements or implied statements contained herein.

An essential step in the review of a company is an analysis of its financial performance over time. Analyzing a company's financial statements provides an indication of historical growth, liquidity, leverage, and profitability, all of which influence the value of a company's assets or equity. The following section of this report examines the trend of the company's financial performance in the previous fiscal years.

The subject company's historical income statements have been adjusted by the User to present the business as if it had been managed to maximize profitability. Since private companies tend to keep reported profits and resulting taxes as low as possible, adjusting the financial statements is an important element to understanding the true earning capacity of the business.

Adjustments include any fringe benefits the owner may have had, unusual circumstances, liens that will be paid off, as well as the standard adjustments used to determine Adjusted EBITDA (Earnings before Interest, Taxes, Depreciation, and Amortization). This will reflect a more realistic income for a new owner and allow a prospective purchaser to compare "apples to apples".

This adjusted profit is known as SDE (Seller's Discretionary Earnings). SDE could be defined as the total financial benefit available to a single person who owns and is fully employed in the operation of the business. Put another way, Adj. EBITDA = SDE minus a manager's salary. Analysis of the subject Company is based on the adjusted totals. A summary of the adjusted historical financial statements is contained in the following section.

**Chinook Business Advisory does not audit or review the financial statements of the subject company nor any of the adjustments made by the User and bears no responsibility for the use of this report.**

\newpage

# Valuation {.unnumbered}

Based on the information provided, the report has determined the Most Probable Selling Price (MPSP) for {{< var company_name >}} to be:

\begin{mpspbox}
\begin{center}
{\fontsize{60}{72}\selectfont\bfseries \${{< var mpsp >}}}
\end{center}
\end{mpspbox}

\vspace{1.5em}

## Valuation Multiples

This price was determined using a market-based approach which examined **{{< var num_comparables >}} comparable transactions**. These transactions included businesses with revenues between **\${{< var comp_revenue_min >}}** and **\${{< var comp_revenue_max >}}**. An asking price of **\${{< var mpsp >}}** represents the following valuation multiples:

\vspace{1em}

\begin{center}
\begin{tabular}{>{\raggedright\arraybackslash}p{3.5in}r}
\toprule
\rowcolor{tableheader}
\textcolor{white}{\textbf{Valuation Metric}} & \textcolor{white}{\textbf{Multiple}} \\
\midrule
Revenue & {{< var revenue_multiple >}} \\
\rowcolor{lightgray}
SDE & {{< var sde_multiple >}} \\
Adj. EBITDA & {{< var ebitda_multiple >}} \\
\bottomrule
\end{tabular}
\end{center}

\vspace{1em}
\textit{See Appendix A for comparable transactions.}

\newpage

# Company Overview {.unnumbered}

\begin{infobox}
\textbf{Name of Business:} {{< var company_name >}}

\textbf{NAICS Industry Code:} {{< var naics_description >}} ({{< var naics_code >}})

\textbf{MPSP:} \${{< var mpsp >}}
\end{infobox}

\vspace{1.5em}

```{python}
import pandas as pd
import numpy as np

df = pd.read_csv('financial_data.csv')
norm_df = pd.read_csv('normalization_data.csv')

print("\\begin{center}")
print("\\begin{longtable}{lrrrrr}")
print("\\toprule")
print("\\rowcolor{tableheader}")
print("\\textcolor{white}{} & \\textcolor{white}{\\textbf{2025 proj.}} & \\textcolor{white}{\\textbf{2024}} & \\textcolor{white}{\\textbf{2023}} & \\textcolor{white}{\\textbf{2022}} & \\textcolor{white}{\\textbf{2021}} \\\\")
print("\\midrule")
print("\\endfirsthead")
print("\\toprule")
print("\\rowcolor{tableheader}")
print("\\textcolor{white}{} & \\textcolor{white}{\\textbf{2025 proj.}} & \\textcolor{white}{\\textbf{2024}} & \\textcolor{white}{\\textbf{2023}} & \\textcolor{white}{\\textbf{2022}} & \\textcolor{white}{\\textbf{2021}} \\\\")
print("\\midrule")
print("\\endhead")

# Define rows with proper data sources
rows_data = [
    ('Total Revenue', 'Revenue', False),
    ('Total Cost of Goods', 'Cost_of_Goods', True),
    ('Gross Profit', 'Gross_Profit', False),
    ('Total Expenses', 'Total_Expenses', True),
    ('Net Income', 'Net_Income', False),
    ('Total Normalizations', 'Total Adjustments', True),
    ('SDE', 'SDE', False),
    ('Adj. EBITDA', 'Adjusted EBITDA', True)
]

for idx, (label, source, shade) in enumerate(rows_data):
    if shade:
        print("\\rowcolor{lightgray}")
    
    values = []
    
    # Check if data comes from financial_data or normalization_data
    if source in df.columns:
        for val in df[source]:
            if pd.notna(val):
                values.append(f"\\${val:,.0f}")
            else:
                values.append("\\$-")
    else:
        # Get from normalization_data
        for col in ['2025_proj', '2024', '2023', '2022', '2021']:
            row_data = norm_df[norm_df['Item'] == source]
            if len(row_data) > 0:
                val = row_data[col].values[0]
                # Convert to numeric if it's a string number
                if isinstance(val, str):
                    try:
                        val = float(val.replace(',', ''))
                    except:
                        values.append("\\$-")
                        continue
                
                if pd.notna(val) and val != 0:
                    values.append(f"\\${val:,.0f}")
                else:
                    values.append("\\$-")
            else:
                values.append("\\$-")
    
    print(f"\\textbf{{{label}}} & {' & '.join(values)} \\\\")

print("\\midrule")
print("\\rowcolor{tableheader}")
print("\\textcolor{white}{\\textbf{Year Weighting}} & \\textcolor{white}{\\textbf{50\\%}} & \\textcolor{white}{\\textbf{50\\%}} & \\textcolor{white}{\\textbf{0\\%}} & \\textcolor{white}{\\textbf{0\\%}} & \\textcolor{white}{\\textbf{0\\%}} \\\\")
print("\\bottomrule")
print("\\end{longtable}")
print("\\end{center}")
```

\vspace{1em}

\begin{itemize}
\item \textbf{Weighted Average of Revenue:} \${{< var weighted_avg_revenue >}} \hfill \textbf{MPSP Multiple of Revenue:} {{< var revenue_multiple >}}
\item \textbf{Weighted Average of SDE:} \${{< var weighted_avg_sde >}} \hfill \textbf{MPSP Multiple of SDE:} {{< var sde_multiple >}}
\end{itemize}

\vspace{0.5em}
\textit{Note: Projected year is calculated from the year to date statement from January 1 to September 30.}

\newpage

# Valuation Methodologies {.unnumbered}

## 1. Earnings Based Approaches {.unnumbered}

This method assesses the ability of the Company to produce earnings in the future. With this approach, a valuator uses the Company's operating history to determine its expected level of earnings and the likelihood of the earnings to continue in the future.

These earnings are normalized for unusual revenue or non-operational expenses. A capitalization factor, often called a multiple, is then applied that reflects a reasonable rate of return based on the perceived risk associated with the continued profitability of the company.

Within Earning Based Approaches there are several other methodologies used such as Discounted Cash Flow (DCF) where an average of the trend of predicted future earnings is used and divided by the capitalization factor.

## 2. Asset Based Approaches {.unnumbered}

Includes the book value of tangible assets on the balance sheet (inventory/supplies, fixed assets, and all intangible assets) minus liabilities. Simply, the money left over if the company was liquidated.

The Asset Based Approach are often appropriate in the following situations:

1. The company is considering liquidating or going out of business
2. The company has no earnings history
3. The company's earnings cannot be reliably estimated
4. The company depends heavily on competitive contracts and there is not a consistent, predictable customer base (e.g., construction companies)
5. The company derives little or no value from labor or intangible assets (e.g., real estate or holding companies)
6. A significant portion of the company's assets are composed of liquid assets or other investments (e.g., marketable securities, real estate, mineral rights)

As such, the asset approach is for businesses where a large amount of the value is in its tangible assets. Or the business is not generating a high enough return on its assets to warrant "excess earnings" or "goodwill".

\newpage

## 3. Market Based Approaches {.unnumbered}

The market-based approach studies recent sales of similar assets, making adjustments for the differences between them. This is similar to how the real estate industry uses "market comps" to determine a listing price.

To find a Company's Most Probable Selling Price (MPSP), the report examines transaction data of businesses of a similar size and industry. The report then makes adjustments to the Company's value based on the qualitative inputs of the report User. These are factors such as client concentration, growth opportunities, management structure, etc.

A market-based valuation represents a reasonable expectation of what the business might sell for in a free and open market based on similar business purchase and sale transactions.

\newpage

# Valuation Methodologies (continued) {.unnumbered}

## Methodology {.unnumbered}

Our transaction algorithm examines a database of **40,000+ transactions** to find comparable businesses that have been sold.

The algorithm selects businesses that are similar in terms of NAICS code and annual revenues. The more businesses that have sold that are similar to yours, the more accurate the MPSP will be.

## The Science {.unnumbered}

Based on information you provide in the financial tables, the report then assigns your business a median business value. That means that if the report finds 15 businesses that were similar it would assign your business the middle value.

## The Art {.unnumbered}

The next part of the process involves taking the answers to the questions we ask and trying to determine if your business is more or less attractive than average.

This report uses your answers to more accurately position your business on the chart. If your answers suggest that your business is a little better than the average in the dataset, the report will assign a higher Most Probable Selling Price to your business. Conversely, if there are opportunities to improve your business that haven't yet been acted on, the report will assign a lower MPSP.

\newpage

# Unadjusted Historical Income Statements {.unnumbered}

\textit{Derived from accountant prepared financial statements}

\vspace{1em}

```{python}
import pandas as pd

df = pd.read_csv('financial_data.csv')

print("\\begin{center}")
print("\\begin{longtable}{lrrrrr}")
print("\\toprule")
print("\\rowcolor{tableheader}")
print("\\textcolor{white}{} & \\textcolor{white}{\\textbf{2025 proj.}} & \\textcolor{white}{\\textbf{2024}} & \\textcolor{white}{\\textbf{2023}} & \\textcolor{white}{\\textbf{2022}} & \\textcolor{white}{\\textbf{2021}} \\\\")
print("\\midrule")
print("\\endfirsthead")
print("\\toprule")
print("\\rowcolor{tableheader}")
print("\\textcolor{white}{} & \\textcolor{white}{\\textbf{2025 proj.}} & \\textcolor{white}{\\textbf{2024}} & \\textcolor{white}{\\textbf{2023}} & \\textcolor{white}{\\textbf{2022}} & \\textcolor{white}{\\textbf{2021}} \\\\")
print("\\midrule")
print("\\endhead")

# Revenue section
print("\\rowcolor{lightgray}")
print("\\textbf{Revenue} & & & & & \\\\")
print("Revenue & ", end='')
for val in df['Revenue']:
    print(f"\\${val:,.0f} & ", end='')
print("\\\\")
print("\\rowcolor{lightgray}")
print("\\textbf{Total Revenue} & ", end='')
for val in df['Revenue']:
    print(f"\\${val:,.0f} & ", end='')
print("\\\\")
print("\\midrule")

# Cost of Goods
print("\\textbf{Cost of Goods} & & & & & \\\\")
print("\\rowcolor{lightgray}")
print("Cost of Sales & ", end='')
for val in df['Cost_of_Goods']:
    print(f"\\${val:,.0f} & ", end='')
print("\\\\")
print("\\textbf{Total Cost of Goods} & ", end='')
for val in df['Cost_of_Goods']:
    print(f"\\${val:,.0f} & ", end='')
print("\\\\")
print("\\midrule")

# Gross Profit
print("\\rowcolor{lightgray}")
print("\\textbf{Gross Profit} & ", end='')
for val in df['Gross_Profit']:
    print(f"\\${val:,.0f} & ", end='')
print("\\\\")
print("Gross Profit \\% & ", end='')
for val in df['Gross_Profit_Pct']:
    print(f"{val:.2f}\\% & ", end='')
print("\\\\")
print("\\midrule")

# Expenses
print("\\rowcolor{lightgray}")
print("\\textbf{Expenses} & & & & & \\\\")
print("General Expense & ", end='')
for val in df['Total_Expenses']:
    print(f"\\${val:,.0f} & ", end='')
print("\\\\")
print("\\rowcolor{lightgray}")
print("\\textbf{Total Expenses} & ", end='')
for val in df['Total_Expenses']:
    print(f"\\${val:,.0f} & ", end='')
print("\\\\")
print("\\midrule")

# Other Income
print("\\textbf{Other Income} & ", end='')
for val in df['Other_Income']:
    if val == 0:
        print("\\$- & ", end='')
    else:
        print(f"\\${val:,.0f} & ", end='')
print("\\\\")
print("\\midrule")

# Net Income
print("\\rowcolor{lightgray}")
print("\\textbf{Net Income} & ", end='')
for val in df['Net_Income']:
    print(f"\\${val:,.0f} & ", end='')
print("\\\\")
print("Net Income \\% & ", end='')
for val in df['Net_Income_Pct']:
    print(f"{val:.2f}\\% & ", end='')
print("\\\\")

print("\\bottomrule")
print("\\end{longtable}")
print("\\end{center}")
```

\vspace{0.5em}
\textit{Note: Projected year is calculated from the year to date statement from January 1 to September 30.}

\newpage

# Normalization Summary {.unnumbered}

```{python}
import pandas as pd

df = pd.read_csv('normalization_data.csv')

print("\\begin{center}")
print("\\begin{longtable}{lrrrrr}")
print("\\toprule")
print("\\rowcolor{tableheader}")
print("\\textcolor{white}{} & \\textcolor{white}{\\textbf{2025 proj.}} & \\textcolor{white}{\\textbf{2024}} & \\textcolor{white}{\\textbf{2023}} & \\textcolor{white}{\\textbf{2022}} & \\textcolor{white}{\\textbf{2021}} \\\\")
print("\\midrule")
print("\\endfirsthead")
print("\\toprule")
print("\\rowcolor{tableheader}")
print("\\textcolor{white}{} & \\textcolor{white}{\\textbf{2025 proj.}} & \\textcolor{white}{\\textbf{2024}} & \\textcolor{white}{\\textbf{2023}} & \\textcolor{white}{\\textbf{2022}} & \\textcolor{white}{\\textbf{2021}} \\\\")
print("\\midrule")
print("\\endhead")

shade_rows = [0, 2, 4, 6, 8, 9]  # Alternating pattern

for idx, item in enumerate(df['Item']):
    if idx in shade_rows:
        print("\\rowcolor{lightgray}")
    
    if item == 'Year Weighting':
        print(f"\\textbf{{{item}}} & ", end='')
        for col in ['2025_proj', '2024', '2023', '2022', '2021']:
            print(f"\\textbf{{{df[col].iloc[idx]}}} & ", end='')
        print(" \\\\")
    else:
        print(f"\\textbf{{{item}}} & ", end='')
        for col in ['2025_proj', '2024', '2023', '2022', '2021']:
            val = df[col].iloc[idx]
            
            # Handle string values
            if isinstance(val, str):
                try:
                    val = float(val.replace(',', ''))
                except:
                    print("\\$- & ", end='')
                    continue
            
            if pd.notna(val) and val != 0:
                print(f"\\${val:,.0f} & ", end='')
            else:
                print("\\$- & ", end='')
        print(" \\\\")
    
    # Add separators after key rows
    if item in ['Total Adjustments', 'Adjusted EBITDA']:
        print("\\midrule")

print("\\bottomrule")
print("\\end{longtable}")
print("\\end{center}")
```

\vspace{0.5em}
\textit{Note: Projected year is calculated from the year to date statement from January 1 to September 30.}

\newpage

## Adjusted EBITDA {.unnumbered}

In its simplest definition, adjusted EBITDA is a measure of a company's financial performance, acting as an alternative to other metrics like revenue, earnings or net income.

Adjusted EBITDA is how many people determine business value as it places the focus on the financial outcome of operating decisions. It does this by removing the impacts of non-operating decisions made by the existing management, such as interest expenses, tax rates, or significant intangible assets.

This leaves a figure that better reflects the operating profitability of a business, one that can effectively be compared between companies by owners, buyers and investors. It is for that reason many employ adjusted EBITDA over other metrics when deciding which organization is more attractive.

### What does EBITDA stand for? {.unnumbered}

- **E - Earnings** - how much money a company makes.
- **B - Before**
- **I - Interest** - the expenses to a business caused by interest rates, such as loans provided by a bank or similar third-party.
- **T - Taxes** - the expenses to a business caused by tax rates imposed by their city, state, and country.
- **D - Depreciation** - a non-cash expense referring to the gradual reduction in value of a company's assets.
- **A - Amortization** - a non-cash expense referring to the cost of intangible (non-balance sheet) assets over time.

## SDE {.unnumbered}

Business owners often try to optimize the taxes they pay each year. As a result, it is not uncommon for a company to appear to make less money, 'on paper.' For example, a company's profits are reduced if the owner takes a salary from their business, as that wage appears as an expense. However, this is money in the pocket of the business owner.

Therefore, we use Seller's Discretionary Earnings (SDE) as a better way to show the profitability of an owner/operator business. To calculate SDE we add back all the benefits the owner receives from the business to Net Income (owner salaries, depreciation/amortization, etc.).

\newpage

# Industry Benchmarks {.unnumbered}

The table below compares your financial performance to **{{< var benchmark_sample >}}** other businesses in your industry using data from Statistics Canada. Benchmarking data is created using a sample of Revenue Canada tax returns for incorporated businesses operating in Canada. To start increasing your valuation, focus on areas labelled 'Improvement Opportunity' in the analysis column.

\vspace{1em}

\begin{center}
\begin{tabular}{lccc}
\toprule
\rowcolor{tableheader}
\textcolor{white}{\textbf{Metric}} & \textcolor{white}{\textbf{Your Company}} & \textcolor{white}{\textbf{Industry Average}} & \textcolor{white}{\textbf{Analysis}} \\
\midrule
\rowcolor{lightgray}
Cost of Goods & {{< var company_cogs >}}\% & {{< var industry_cogs >}}\% & Good \\
Total Expenses & {{< var company_expenses >}}\% & {{< var industry_expenses >}}\% & Good \\
\bottomrule
\end{tabular}
\end{center}

\vspace{1em}

\textit{* Note: Depending on how your accountant prepares your financial statements, your salaries \& wages and/or direct wages may appear high or low.}

\vspace{0.5em}

On average, total employment costs in your industry are **{{< var industry_employment >}}\%** of revenue. In comparison, your total employment costs are **{{< var company_employment >}}\%**.

\newpage

# Scorecard {.unnumbered}

## Valuation Range {.unnumbered}

Sometimes the numbers don't represent the true value of a business. Scorecard values can change the valuation by +/- 25% of the base valuation. The chart below shows the valuation range for {{< var company_name >}} based on the scorecard answers. A totally optimized scorecard would give a business valuation of \${{< var valuation_range_max >}}.

\vspace{1em}

\begin{rangebox}
\begin{center}
\textbf{Range:} \${{< var valuation_range_min >}} \hspace{3cm} \${{< var valuation_range_max >}}

\vspace{1em}

{\LARGE \${{< var mpsp >}}}
\end{center}
\end{rangebox}

\vspace{1em}

## Section Breakdown {.unnumbered}

The following sections break down the qualitative analysis of {{< var company_name >}}. Each section shows how answers affect the overall valuation.

\newpage

### Finance and General Operations (+/- 6.25\% of valuation) {.unnumbered}

**Questions:**

\begin{itemize}
\item \textbf{Documented processes:} We have some things written down
\item \textbf{Professional accounting:} Yes
\item \textbf{Annual budget:} No
\item \textbf{Payables management:} Yes
\end{itemize}

**Impact range:** -\$168,571 to +\$168,571

It is very difficult for a potential buyer to assess, and ultimately purchase, a business without being able to review accurate financial statements. To increase your score in this area:

\begin{itemize}
\item Make sure you use a certified accountant to prepare your financial statements and file your tax returns.
\item Make sure your accounts payable are up to date and you are meeting all the terms of your supplier contracts.
\item Draft a budget. Creating, monitoring, and managing a budget is the key to business success. A detailed and realistic budget can be most important tool for guiding your business.
\item Document processes and procedures in a way that someone that is not from the organization can come in and understand them. Ensure thorough procedures are detailed for all sales and operational processes.
\end{itemize}

\vspace{1em}

### Owner Dependency (+/- 6.25\% of valuation) {.unnumbered}

**Questions:**

\begin{itemize}
\item \textbf{Would your company thrive if you left for 2 months:} No
\item \textbf{Recent extended vacation:} No
\item \textbf{Customer name recognition:} 0\%
\end{itemize}

**Impact range:** -\$168,571 to +\$168,571

One of the single biggest concerns voiced by business acquirers is the fear that the business will collapse without the founder at the helm. To alleviate that concern, and to increase the value of your business, make every effort to reduce your importance in day-to-day business operations.

\begin{itemize}
\item Start with identifying your daily tasks, making an accurate list of day-to-day operations. Then, delegate.
\item Delegate - create and mentor leaders by giving employees more responsibility. Take time to train new managers to take on your roles.
\item Automate systems, many tech companies have created niche products designed to expedite quotes, sales, project management, invoicing, customer service management etc.
\item Transition key clients to other managers or sales members. Though a delicate task, it will help position you in a less demanding role.
\item Start being gradually absent. See how your company does once you've removed yourself, first for a long weekend, then a week, then longer.
\end{itemize}

\newpage

### Growth Potential (+/- 3.75\% of valuation) {.unnumbered}

**Questions:**

\begin{itemize}
\item \textbf{Identified growth opportunities:} Yes
\item \textbf{Revenue capacity increase:} 25\%
\end{itemize}

**Impact range:** -\$101,143 to +\$101,143

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

\vspace{1em}

### Recurring Revenues (+/- 2.5\% of valuation) {.unnumbered}

**Revenue model:** Your revenue is dependent on customers walking in/calling in to order/ordering online. (eg. retail store, restaurant, construction services)

**Impact range:** -\$67,429 to +\$67,429

Buyers love recurring revenues. Recurring revenue is the portion of a company's revenue that is contracted to continue in the future. Unlike one-off sales, these revenues are predictable, stable and can be counted on to occur at regular intervals going forward with a high degree of certainty. Examples include cell phone contracts, magazine subscriptions, and service plans.

Not all companies can transition their customers to a recurring revenue model, but if you have the ability to do one or more of the following, your business value will increase:

\begin{itemize}
\item Can you offer monthly service plans?
\item Can you implement a membership program?
\item Do you have additional service options available?
\item Can you set up an affiliate program?
\end{itemize}

\newpage

### Organizational Stability (+/- 3.75\% of valuation) {.unnumbered}

**Questions:**

\begin{itemize}
\item \textbf{Largest customer revenue:} Less than 5\%
\item \textbf{Top 5 customers revenue:} 10\%-24\%
\item \textbf{Sales leader replacement:} It is me
\item \textbf{Operations leader replacement:} It is me
\item \textbf{Supplier replacement:} Yes
\end{itemize}

**Impact range:** -\$101,143 to +\$101,143

Business buyers are often concerned about how stable or resilient an organization is. An organization that is not heavily dependent on one or two key employees, one supplier or a small group of customers is more saleable and more valuable than a company that has all its eggs in one basket. The best way to create a strong foundation is to diversify:

\begin{itemize}
\item Developing a more diverse customer base mitigates risk and provides additional financial security and stability.
\item Cross-train your employees as much as possible.
\item Create relationships with multiple suppliers.
\end{itemize}

\vspace{1em}

### Sales and Marketing (+/- 2.5\% of valuation) {.unnumbered}

**Questions:**

\begin{itemize}
\item \textbf{Customer feedback process:} No
\item \textbf{Marketing spend:} 1-5\% of revenue
\item \textbf{Google search ranking:} First page
\item \textbf{Written acquisition strategy:} No
\end{itemize}

**Impact range:** -\$67,428 to +\$67,428

Marketing and sales strategies are essential because they are designed to help you sell your products or services. Through proper communication, marketing helps your business become a market leader and trigger purchase decisions. In addition, it builds a reputation and it's fair to say that your reputation determines your brand equity.

When businesses have an existing marketing plan and established brand, obtaining and retaining customers will be less work for a buyer, making the business more desirable. Here are some questions you can ask yourself:

\begin{itemize}
\item Do you have an annual budget allocated to marketing initiatives?
\item How strong is your branding? Do you show up first in a Google search?
\item Do you have a web presence through a website or social media?
\item Can you identify your ideal customer?
\item Do you have any customer feedback surveys or follow-up strategies?
\item Are you tracking how people discover your business?
\end{itemize}

\newpage

# Appendix A: Comparable Transactions {.unnumbered}

```{python}
import pandas as pd

df = pd.read_csv('comparable_transactions.csv')

print("\\begin{center}")
print("\\begin{longtable}{rrrrrrr}")
print("\\toprule")
print("\\rowcolor{tableheader}")
print("\\textcolor{white}{\\textbf{NAICS}} & \\textcolor{white}{\\textbf{Revenue}} & \\textcolor{white}{\\textbf{SDE}} & \\textcolor{white}{\\textbf{Adj.}} & \\textcolor{white}{\\textbf{Price}} & \\textcolor{white}{\\textbf{Rev}} & \\textcolor{white}{\\textbf{SDE}} & \\textcolor{white}{\\textbf{EBITDA}} \\\\")
print("\\rowcolor{tableheader}")
print("\\textcolor{white}{\\textbf{Code}} & & & \\textcolor{white}{\\textbf{EBITDA}} & & \\textcolor{white}{\\textbf{Mult}} & \\textcolor{white}{\\textbf{Mult}} & \\textcolor{white}{\\textbf{Mult}} \\\\")
print("\\midrule")
print("\\endfirsthead")
print("\\toprule")
print("\\rowcolor{tableheader}")
print("\\textcolor{white}{\\textbf{NAICS}} & \\textcolor{white}{\\textbf{Revenue}} & \\textcolor{white}{\\textbf{SDE}} & \\textcolor{white}{\\textbf{Adj.}} & \\textcolor{white}{\\textbf{Price}} & \\textcolor{white}{\\textbf{Rev}} & \\textcolor{white}{\\textbf{SDE}} & \\textcolor{white}{\\textbf{EBITDA}} \\\\")
print("\\rowcolor{tableheader}")
print("\\textcolor{white}{\\textbf{Code}} & & & \\textcolor{white}{\\textbf{EBITDA}} & & \\textcolor{white}{\\textbf{Mult}} & \\textcolor{white}{\\textbf{Mult}} & \\textcolor{white}{\\textbf{Mult}} \\\\")
print("\\midrule")
print("\\endhead")

for idx in range(len(df)):
    if idx % 2 == 1:
        print("\\rowcolor{lightgray}")
    print(f"{df['NAICS_Code'].iloc[idx]} & ", end='')
    print(f"\\${df['Revenue'].iloc[idx]:,.0f} & ", end='')
    print(f"\\${df['SDE'].iloc[idx]:,.0f} & ", end='')
    print(f"\\${df['Adj_EBITDA'].iloc[idx]:,.0f} & ", end='')
    print(f"\\${df['Price'].iloc[idx]:,.0f} & ", end='')
    print(f"{df['Revenue_Multiple'].iloc[idx]:.2f} & ", end='')
    print(f"{df['SDE_Multiple'].iloc[idx]:.2f} & ", end='')
    print(f"{df['EBITDA_Multiple'].iloc[idx]:.2f} \\\\")

print("\\bottomrule")
print("\\end{longtable}")
print("\\end{center}")
```

'''
    
    output_path = Path(OUTPUT_FOLDER) / 'valuation_report.qmd'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"\n{'='*70}")
    print("✓ PROFESSIONAL VALUATION REPORT CREATED")
    print(f"{'='*70}")
    print(f"\nTemplate: {output_path}")
    print("\n🎨 THEME FEATURES:")
    print("  • No section numbering (.unnumbered)")
    print("  • Professional title page with logo")
    print("  • Enhanced color scheme (blues & grays)")
    print("  • Styled boxes with subtle shadows")
    print("  • Blue table headers with white text")
    print("  • Alternating row colors in tables")
    print("  • Clean section dividers")
    print("  • Professional typography (Arial)")
    print("  • Proper date formatting")
    
    print(f"\n{'='*70}")
    print("📋 NEXT STEPS:")
    print(f"{'='*70}")
    print(f"\n1. Ensure Chinook_logo.png is in: {OUTPUT_FOLDER}/")
    print(f"\n2. Navigate to folder:")
    print(f"   cd {OUTPUT_FOLDER}")
    print(f"\n3. Generate the PDF:")
    print(f"   quarto render valuation_report.qmd --to pdf")
    print(f"\n4. Your report will be:")
    print(f"   {OUTPUT_FOLDER}/valuation_report.pdf")
    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    create_professional_quarto_template()