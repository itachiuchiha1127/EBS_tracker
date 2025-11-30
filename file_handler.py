import os
import csv
import json
import datetime
from fpdf import FPDF

LOG_FILE = "logs/app.log"

def log_error(error_message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists("logs"):
        os.makedirs("logs")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] ERROR: {error_message}\n")

def generate_csv(transactions):
    output = []
    headers = ["Date", "Type", "Category", "Amount", "Notes"]
    output.append(",".join(headers))
    
    for t in transactions:
        row = [
            t.get("date", ""),
            t.get("type", ""),
            t.get("category", ""),
            str(t.get("amount", 0)),
            t.get("notes", "").replace(",", " ")
        ]
        output.append(",".join(row))
    
    return "\n".join(output)

def generate_pdf(transactions, month_year):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=f"Monthly Report: {month_year}", ln=1, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(30, 10, "Date", 1)
    pdf.cell(20, 10, "Type", 1)
    pdf.cell(40, 10, "Category", 1)
    pdf.cell(30, 10, "Amount", 1)
    pdf.cell(70, 10, "Notes", 1)
    pdf.ln()
    
    pdf.set_font("Arial", size=10)
    total_expense = 0
    total_income = 0
    
    for t in transactions:
        pdf.cell(30, 10, str(t.get("date")), 1)
        pdf.cell(20, 10, t.get("type").capitalize(), 1)
        pdf.cell(40, 10, t.get("category"), 1)
        pdf.cell(30, 10, str(t.get("amount")), 1)
        pdf.cell(70, 10, t.get("notes", "")[:35], 1)
        pdf.ln()
        
        if t["type"] == "expense":
            total_expense += float(t["amount"])
        else:
            total_income += float(t["amount"])

    pdf.ln(5)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 10, f"Total Income: {total_income} | Total Expenses: {total_expense}", ln=1)
    pdf.cell(0, 10, f"Net Savings: {total_income - total_expense}", ln=1)

    return pdf.output(dest="S").encode("latin-1")

def backup_data(db):
    data = {
        "transactions": list(db.transactions.find()),
        "categories": list(db.categories.find()),
        "budgets": list(db.budgets.find()),
        "goals": list(db.goals.find())
    }
    from db_helper import json_encoder
    for key in data:
        data[key] = json_encoder(data[key])
        
    return json.dumps(data, indent=4)
