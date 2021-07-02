# From rest_framework
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import authentication, permissions
from django.http import HttpResponse

# Pdf Utilities
import os
import io
import datetime
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

# Models
from profiles.models import User


@api_view(['GET'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
def report_users(request):
    current_date = datetime.date.today().strftime('%d/%m/%Y')
    order = request.query_params.get('order')


    candidates = User.objects.filter(is_superuser=False)
    administrators = User.objects.filter(is_superuser=True)
    total_candidates = len(candidates)
    total_administrators = len(administrators)
    total_users = total_candidates + total_administrators



    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    p.setLineWidth(.2)
    p.setFont('Helvetica', 22)
    p.drawString(30, 750, 'PPM')

    p.setFont('Helvetica', 12)
    p.drawString(30, 735, 'Report')

    p.setFont('Helvetica-Bold', 12)
    p.drawString(480, 750, current_date)
    p.line(460, 747, 560, 747)

    # Candidates_table
    candidates = [
        {"Id": '1', 'first_name': 'Nombre', 'last_name': 'Apellido'}
    ]

    # Table header
    styles = getSampleStyleSheet()
    styleBH = styles['Normal']
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    number = Paragraph('''Id''', styleBH)
    first_name = Paragraph('''Nombre''', styleBH)
    last_name = Paragraph('''Apellido''', styleBH)

    data = []
    data.append([number, first_name, last_name])

    # table
    styleN = styles['BodyText']
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    high = 650

    for candidate in candidates:
        this_student = [candidate['Id'], candidate['first_name'], candidate['last_name']]
        data.append(this_student)
        high = high - 18

    # table size
    width, height = A4
    table = Table(data, colWidths=[1.9 * cm, 9.5 * cm, 1.9 * cm, 1.9 * cm, 1.9 * cm, 1.9 * cm])
    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    # pdf size

    table.wrapOn(p, width, height)
    table.drawOn(p, 30, high)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='users-report.pdf')
