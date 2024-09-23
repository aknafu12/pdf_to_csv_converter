import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_converter import PDFConverter

class PDFToCSVApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF to CSV Bank Statement Converter")

        self.api_key = "YOUR_API_KEY"  # Replace with your OpenAI API key
        self.converter = PDFConverter(self.api_key)

        self.label = tk.Label(master, text="Select PDF Bank Statements:")
        self.label.pack(pady=10)

        self.upload_button = tk.Button(master, text="Upload PDF", command=self.upload_pdf)
        self.upload_button.pack(pady=10)

        self.convert_button = tk.Button(master, text="Convert to CSV", command=self.convert_pdf_to_csv, state=tk.DISABLED)
        self.convert_button.pack(pady=10)

        self.status_label = tk.Label(master, text="")
        self.status_label.pack(pady=10)

    def upload_pdf(self):
        self.pdf_files = filedialog.askopenfilenames(title="Select PDF Files", filetypes=[("PDF files", "*.pdf")])
        if self.pdf_files:
            self.status_label.config(text=f"{len(self.pdf_files)} PDF files selected.")
            self.convert_button.config(state=tk.NORMAL)

    def convert_pdf_to_csv(self):
        for pdf_file in self.pdf_files:
            csv_file = pdf_file.replace('.pdf', '.csv')
            try:
                self.converter.convert_pdf_to_csv(pdf_file, csv_file)
                self.status_label.config(text=f"Converted: {pdf_file} to {csv_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert {pdf_file}: {e}")

        messagebox.showinfo("Success", "Conversion complete!")

