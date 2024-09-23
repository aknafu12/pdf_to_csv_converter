import pdfplumber
import openai
import pandas as pd


class PDFConverter:
    def __init__(self, api_key):
        openai.api_key = api_key

    def extract_text_from_pdf(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def gpt_extract_data(self, text):
        prompt = f"Extract and structure the following bank statement data into CSV format with columns Date, Description, Amount:\n\n{text}"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.5
        )
        return response.choices[0].message['content'].strip()

    def convert_pdf_to_csv(self, pdf_path, csv_path):
        text = self.extract_text_from_pdf(pdf_path)
        structured_data = self.gpt_extract_data(text)

        # Convert the structured data into a DataFrame and save it as CSV
        rows = [row.split(',') for row in structured_data.split('\n') if row]
        df = pd.DataFrame(rows[1:], columns=rows[0])
        df.to_csv(csv_path, index=False)
