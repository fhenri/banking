from datetime import datetime
from datetime import timedelta
import json
import pdfkit
from jinja2 import Environment, FileSystemLoader

def generate ():
    environment = Environment(loader=FileSystemLoader("resources/templates/"))
    invoice_zoho_template = environment.get_template("invoice.zoho.html")
    #invoice_template = environment.get_template("invoice.html")
    footer_template = environment.get_template("footer.html")

    invoice_generate_options = {
        #'footer-center': "EURL au capital de 2 000 euros\nRCS : 843 310 590 R.C.S. Cannes - NAF : 6202A",
        # stackoverflow
        'enable-local-file-access': None,
        'page-size': 'A4',
        'margin-top': '0in',
        'margin-right': '0in',
        'margin-bottom': '0.75in',
        'margin-left': '0in',
        'encoding': "UTF-8",
        'footer-html': footer_template.filename,
        'no-outline': None
    }

    data_payload = json.load(open("payload.json"))
    invoice_main_data = data_payload['main']
    invoice_date = invoice_main_data['invoice_date']
    invoice_due_date = (datetime.strptime(invoice_date, '%d-%m-%Y') + timedelta(days = 150)).strftime('%d-%m-%Y')
    invoice_list = data_payload['invoices']

    for invoice in invoice_list:
        invoice_filename = f"{invoice_main_data['id']}-{invoice['internal']}"
        html_filename = f"resources/out/{invoice_filename}.html"
        with open(html_filename, mode="w", encoding="utf-8") as results:
            # merge the json objects - dictionary unpacking operator
            invoice_data = { **invoice_main_data, **invoice, "invoice_due_date": invoice_due_date }
            #invoice_data = {
            #                **invoice_main_data, **invoice,
            #                'date': today.strftime('%Y-%m-%d'),
            #                'due_date': invoice_due_date.strftime('%Y-%m-%d')
            #                }
            results.write(invoice_zoho_template.render(invoice_data))
            #results.write(invoice_template.render(invoice_data))

        pdf_filename = f"resources/pdf/{invoice_filename}.pdf"
        pdfkit.from_file(html_filename, pdf_filename, options=invoice_generate_options)

def main():
    generate();

if __name__ == "__main__":
    print("running Invoice Generation");
    main();
