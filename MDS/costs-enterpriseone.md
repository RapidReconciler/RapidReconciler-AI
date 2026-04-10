Actual Cost Setup for EnterpriseOne - Training Guide

# Purpose

This guide provides step-by-step instructions for configuring Actual Costing in JD Edwards EnterpriseOne, including key fields, setup decisions, and process flow.

# Who Should Use This Guide

\- CNC / System Administrators  
\- Finance / Cost Accounting  
\- Manufacturing Analysts  
\- Power Users

# Process Overview

Actual costing calculates costs based on actual transactions instead of predefined standards.  
<br/>High-Level Flow:  
1\. Configure Manufacturing Constants  
2\. Define Work Center Rates and Overhead  
3\. Set up AAIs  
4\. Configure Parent Item  
5\. Define Components and Costs  
6\. Execute Work Orders and Capture Actual Costs

# 1\. Manufacturing Constants Setup (F3009)

Navigation: EnterpriseOne Menu → Manufacturing Systems Setup → Manufacturing Constants  
<br/>Key Fields:  
\- Overhead Cost Types: Select included cost components  
\- Labor Rate Source: Work Center Rates or Employee Labor Rates (F00191)  
\- Machine Rate Source: Work Center Rates or Equipment Rates (F1301)  
<br/>\[Screenshot Placeholder\]

# 2\. Work Center & Overhead Setup

Work Center Rates (F30008)  
Navigation: Manufacturing Systems Setup → Product Costing → Work Center Rates  
\- Maintain cost methods 02 and 09  
\- Run Frozen Update (P30835)  
<br/>Overhead Rates (F30006)  
Navigation: Manufacturing Systems Setup → Product Costing → Overhead Rates  
<br/>\[Screenshot Placeholder\]

# 3\. AAI Setup (F4095)

Navigation: Financials → General Accounting → Automatic Accounting Instructions  
<br/>Required AAIs:  
\- 3110 Raw Materials  
\- 3120 Work in Process  
\- 3130 Finished Goods  
\- 3401 Accruals  
<br/>Variance Accounting (R31804)  
\- Uses AAI 3210 (COGS)  
\- Document Types: IS, IC, SO  
<br/>\[Screenshot Placeholder\]

# 4\. Parent Item Setup

Item Cost Revisions (P4105)  
Navigation: Inventory Management → Inventory Setup → Item Cost Revisions  
\- Use cost method 02 or 09  
<br/>Inventory Cost Level:  
\- Level 2 or Level 3 (Level 3 only for actual cost)  
<br/>Extra Costs (F30026)  
Navigation: Manufacturing Systems Setup → Product Costing → Extra Costs  
<br/>\[Screenshot Placeholder\]

# 5\. Component Setup

Bill of Material (P3002)  
Navigation: Manufacturing Systems Setup → Product Data Management → Bill of Material  
<br/>Rules:  
\- Components do not need same cost method as parent  
\- Cannot use cost method 09  
<br/>Costs come from P4105 and are calculated at material issue  
<br/>\[Screenshot Placeholder\]

# Common Pitfalls & Tips

\- Missing P4105 costs results in zero cost  
\- Incorrect cost method defaults to standard costing  
\- Validate with test work orders and review F4111
