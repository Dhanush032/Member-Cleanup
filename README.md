# Member Cleanup Script

## Overview

This project processes messy marketing signup data exported from multiple landing pages and generates a cleaned **"Golden Record"** CSV file for CRM import.

The script applies business rules such as date standardization, deduplication, multi-plan handling, and low-quality lead filtering.

---

## Problem Statement

The marketing team provided a `signup.xls` file containing inconsistent and duplicate member records.

The goal was to:

- Standardize signup dates
- Remove duplicate users
- Handle users who signed up for multiple plans
- Identify and quarantine low-quality leads
- Generate a clean final dataset for CRM usage

---

## Business Rules Implemented

### 1. Date Standardization
All signup dates are converted into the format:


If a date cannot be parsed or is invalid, the record is moved to `quarantine.csv`.

---

### 2. Deduplication

- Email is treated as the unique identifier.
- If multiple records exist for the same email:
  - The most recent signup (based on date) is kept.
  - Older entries are removed.

---

### 3. Multi-Plan Handling

If a user signed up for more than one plan:

- Only the most recent record is kept.
- A new column `is_multi_plan` is added.
- `is_multi_plan` is set to `True` for users appearing more than once.

---

### 4. Low-Quality Lead Filtering

Records are moved to `quarantine.csv` if:

- Name is missing
- Email is missing
- Email does not contain "@"
- Name contains the word "test"
- Email contains the word "test"
- Signup date is invalid

This improves CRM data quality and prevents marketing effort from being wasted on invalid or test entries.

---

## Project Structure

member-cleanup/  
│  
├── member_cleanup.py   
├── requirements.txt     
├── signup.xls  
├── members_final.csv  
├── quarantine.csv  
└── README.md  


---

## Requirements

Add the following to `requirements.txt`:

- pandas
- xlrd

pip install -r requirements.txt


---

## How to Run

1. Place `signup.xls` in the project directory.
2. Run the script:


---

## Output Files

### members_final.csv
Cleaned and deduplicated final dataset ready for CRM import.

### quarantine.csv
Low-quality, invalid, or test records separated for review and auditing.

---

## Summary

This script ensures:

- Consistent date formatting
- No duplicate member records
- Proper handling of multi-plan users
- Removal of invalid or test data
- Improved data reliability for business operations

---

## Design Decisions

- Used `pandas` for efficient data manipulation.
- Treated email as the primary unique identifier.
- Sorted records by date to retain the most recent signup.
- Preserved invalid records in quarantine instead of deleting them for traceability.

---

## Author

Developed as part of a data cleanup assignment simulating real-world marketing data processing.
