"""
test_pdf_email.py -- tests PDF generation + email with attachment end-to-end.
Usage: python test_pdf_email.py your@email.com
"""
import sys, os, io, ssl, smtplib
from datetime import datetime, timedelta
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MAIL_USER     = os.getenv('MAIL_USER', 'spamlol439@gmail.com')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'hixpxubhbcqklind')
recipient     = sys.argv[1] if len(sys.argv) > 1 else MAIL_USER

print(f"[INFO] mail user : {MAIL_USER}")
print(f"[INFO] recipient : {recipient}")

# ── Step 1: generate PDF ─────────────────────────────────────────────────────
print("\n[1] Generating PDF...")
try:
    from reportlab.lib.pagesizes import A5
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, HRFlowable)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER

    now = datetime.now()
    info = {
        'reservation_id': 1,
        'user_name': 'Test User',
        'car_plate': 'KA-01-AB-1234',
        'user_email': recipient,
        'slot_label': 'A1',
        'start_time': now,
        'end_time': now + timedelta(hours=1),
    }

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A5,
                            leftMargin=12*mm, rightMargin=12*mm,
                            topMargin=12*mm, bottomMargin=12*mm)

    header_style = ParagraphStyle('header', fontSize=20, leading=24,
                                  textColor=colors.HexColor('#1e3a5f'),
                                  alignment=TA_CENTER, fontName='Helvetica-Bold')
    sub_style    = ParagraphStyle('sub', fontSize=10, leading=13,
                                  textColor=colors.HexColor('#475569'),
                                  alignment=TA_CENTER, fontName='Helvetica')
    token_style  = ParagraphStyle('token', fontSize=13, leading=16,
                                  textColor=colors.HexColor('#0f172a'),
                                  alignment=TA_CENTER, fontName='Helvetica-Bold')
    label_style  = ParagraphStyle('label', fontSize=9,
                                  textColor=colors.HexColor('#64748b'),
                                  fontName='Helvetica')
    value_style  = ParagraphStyle('value', fontSize=11,
                                  textColor=colors.HexColor('#0f172a'),
                                  fontName='Helvetica-Bold')

    duration_mins = 60
    duration_str  = "1h 0m"

    story = [
        Paragraph('P SmartPark', header_style),   # plain ASCII header
        Paragraph('Parking Reservation Token', sub_style),
        Spacer(1, 4*mm),
        HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1e3a5f')),
        Spacer(1, 4*mm),
        Paragraph(f"Token #{info['reservation_id']:06d}", token_style),
        Spacer(1, 6*mm),
    ]

    table_data = [
        [Paragraph('Name',       label_style), Paragraph(info['user_name'],  value_style)],
        [Paragraph('Car Plate',  label_style), Paragraph(info['car_plate'],  value_style)],
        [Paragraph('Email',      label_style), Paragraph(info['user_email'], value_style)],
        [Paragraph('Slot',       label_style), Paragraph(info['slot_label'], value_style)],
        [Paragraph('Date',       label_style), Paragraph(info['start_time'].strftime('%d %B %Y'), value_style)],
        [Paragraph('Start Time', label_style), Paragraph(info['start_time'].strftime('%I:%M %p'), value_style)],
        [Paragraph('End Time',   label_style), Paragraph(info['end_time'].strftime('%I:%M %p'),   value_style)],
        [Paragraph('Duration',   label_style), Paragraph(duration_str,       value_style)],
    ]

    col_w = (A5[0] - 24*mm)
    tbl = Table(table_data, colWidths=[col_w * 0.35, col_w * 0.65])
    tbl.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor('#f8fafc'), colors.white]),
        ('GRID',       (0,0), (-1,-1), 0.4, colors.HexColor('#cbd5e1')),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1')))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        f"Issued: {now.strftime('%d %b %Y, %I:%M %p')} | Status: ACTIVE",
        ParagraphStyle('footer', fontSize=8, alignment=TA_CENTER,
                       textColor=colors.HexColor('#94a3b8'), fontName='Helvetica')
    ))
    story.append(Paragraph(
        'WARNING: This token is valid for 15 minutes from the time of issue.\n'
        'Please arrive at the parking gate before your token expires.',
        ParagraphStyle('validity', fontSize=9, alignment=TA_CENTER, leading=13,
                       textColor=colors.HexColor('#b45309'), fontName='Helvetica')
    ))

    doc.build(story)
    pdf_bytes = buf.getvalue()
    print(f"    [OK] PDF generated successfully ({len(pdf_bytes):,} bytes)")
except Exception as e:
    print(f"    [FAIL] PDF generation error: {e}")
    sys.exit(1)

# ── Step 2: send email with attachment ───────────────────────────────────────
print("\n[2] Sending email with PDF attachment...")
try:
    msg = MIMEMultipart()
    msg['From']    = f'SmartPark <{MAIL_USER}>'
    msg['To']      = recipient
    msg['Subject'] = '[SmartPark] Parking Token #000001 - A1'

    body = (
        f"Hi {info['user_name']},\n\n"
        f"Your parking slot has been reserved.\n\n"
        f"  Slot       : {info['slot_label']}\n"
        f"  Car Plate  : {info['car_plate']}\n"
        f"  Start Time : {info['start_time'].strftime('%d %b %Y, %I:%M %p')}\n"
        f"  End Time   : {info['end_time'].strftime('%d %b %Y, %I:%M %p')}\n\n"
        f"Please find your parking token attached as a PDF.\n\n"
        f"-- SmartPark Team"
    )
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    pdf_part = MIMEApplication(pdf_bytes, _subtype='pdf')
    pdf_part.add_header('Content-Disposition', 'attachment',
                        filename='parking_token_000001.pdf')
    msg.attach(pdf_part)

    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=20) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.login(MAIL_USER, MAIL_PASSWORD)
        smtp.send_message(msg)

    print(f"    [OK] Email with PDF sent to {recipient}!")
except Exception as e:
    print(f"    [FAIL] Email error: {e}")
