from weasyprint import HTML
import tempfile

def generate_plan_pdf(plan_data: dict) -> str:
    """
    Generates a PDF for the given plan data.
    Returns: file path to generated PDF.
    """
    html_content = f"""
    <html>
    <head>
      <style>
        body {{ font-family: sans-serif; }}
        h1 {{ color: #003366; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #999; padding: 8px; text-align: left; }}
      </style>
    </head>
    <body>
      <h1>Plan Illustration - {plan_data.get("plan_name")}</h1>
      <p><strong>Plan ID:</strong> {plan_data.get("plan_id")}</p>
      <p><strong>Min Age:</strong> {plan_data.get("min_age")}</p>
      <p><strong>Max Age:</strong> {plan_data.get("max_age")}</p>

      <h2>Available Payout Options</h2>
      <ul>
        {"".join(f"<li>{opt}</li>" for opt in plan_data.get("available_payout_options", []))}
      </ul>

      <h2>Payment Modes</h2>
      <ul>
        {"".join(f"<li>{mode}</li>" for mode in plan_data.get("available_payment_modes", []))}
      </ul>
    </body>
    </html>
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        HTML(string=html_content).write_pdf(pdf_file.name)
        return pdf_file.name
