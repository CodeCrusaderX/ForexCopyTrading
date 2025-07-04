from fpdf import FPDF
from datetime import datetime

def safe(txt):
    return txt.encode('latin-1', 'replace').decode('latin-1')

def generate_pdf_report(username, trades, balance, total_pnl, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=safe(f"Trade Summary for {username}"), ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"User: {username}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(200, 10, txt=f"Balance: ${balance:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total P&L: ${total_pnl:.2f}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Trade Log:", ln=True)
    pdf.ln(5)

    for t in trades:
        line = f"{t['Time']} | {t['Direction'].upper()} | Amount: ${t['Amount']} | Entry: {t['Entry Price']} | Current: {t['Current Price']} | P&L: ${t['P&L']}"
        pdf.multi_cell(0, 8, txt=line)

    pdf.output(filename)
    return filename