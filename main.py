from flask import Flask
import tabula
# Importar las librerías necesarias
from functools import wraps
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, String, Float, BigInteger, Boolean, JSON, func
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import string
from werkzeug.datastructures import FileStorage
import pandas as pd
from sqlalchemy import create_engine, text
import boto3
import datetime
import pytz
import calendar
import time
import numpy as np
import uuid
import os
import pandas as pd
from sqlalchemy import exists
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

# Configurar el cliente de S3 para utilizar el esquema de autenticación AWS4-HMAC-SHA256


# Crear la aplicación Flask
app = Flask(__name__)
CORS(app)


@app.route('/api/convert_pdf', methods=['POST'])
def convert_pdf():
    # pdf_file = "BRASÍLIA - CONSULTAS.pdf"
    file = request.files['file']
    pdf_file = secure_filename(file.filename)
    file.save(pdf_file)
    num_pag = get_pdf_page_count(pdf_file)
    print(num_pag)
    json_result = convert_pdf_to_json(pdf_file, num_pag)

    # Reemplazar NaN por null en el resultado JSON
    json_str = json.dumps(json_result)
    json_str = json_str.replace('NaN', 'null')
    json_result = json.loads(json_str)

    df = pd.DataFrame(json_result[0])

    # Imprimir las columnas del DataFrame
    columnas = df.columns.tolist()

    return jsonify({'table': json_result[0], 'header': columnas}), 200


def convert_pdf_to_json(pdf_file, num_page):
    dfs = tabula.read_pdf(pdf_file, pages='all')
    print(dfs)
    json_data = []
    for df in dfs:
        json_data.append(df.to_dict(orient='records'))
    return json_data

def get_pdf_page_count(pdf_file):
    reader = PdfReader(pdf_file)
    num_pages = len(reader.pages)
    return num_pages



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=4000))
