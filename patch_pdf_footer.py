import pathlib

p = pathlib.Path(r'x:/UNI/Main project/code/smart_parking/app.py')
src = p.read_text(encoding='utf-8')

anchor_start = 'story.append(tbl)\n    story.append(Spacer(1, 6*mm))'
anchor_end   = '\n    doc.build(story)'

i = src.find(anchor_start)
j = src.find(anchor_end)

if i == -1 or j == -1:
    print('ERROR: anchors not found i=%d j=%d' % (i, j))
    exit(1)

new_footer = (
    "story.append(tbl)\n"
    "    story.append(Spacer(1, 5*mm))\n"
    "    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1')))\n"
    "    story.append(Spacer(1, 3*mm))\n"
    "    issued_str = datetime.now().strftime('%d %b %Y, %I:%M %p')\n"
    "    story.append(Paragraph(\n"
    "        'Issued: ' + issued_str + '  |  Status: ACTIVE',\n"
    "        ParagraphStyle('footer', fontSize=8, alignment=TA_CENTER,\n"
    "                       textColor=colors.HexColor('#94a3b8'), fontName='Helvetica')\n"
    "    ))\n"
    "    story.append(Spacer(1, 4*mm))\n"
    "    warn_style = ParagraphStyle('warn', fontSize=9, alignment=TA_CENTER, leading=13,\n"
    "                                textColor=colors.HexColor('#92400e'), fontName='Helvetica-Bold')\n"
    "    warn_sub   = ParagraphStyle('warn_sub', fontSize=8, alignment=TA_CENTER, leading=11,\n"
    "                                textColor=colors.HexColor('#92400e'), fontName='Helvetica')\n"
    "    col_w2 = A5[0] - 24*mm\n"
    "    warn_tbl = Table(\n"
    "        [[Paragraph('! This token is valid for 15 minutes from the time of issue.', warn_style)],\n"
    "         [Paragraph('Please arrive at the parking gate before your token expires.', warn_sub)]],\n"
    "        colWidths=[col_w2]\n"
    "    )\n"
    "    warn_tbl.setStyle(TableStyle([\n"
    "        ('BACKGROUND',    (0, 0), (-1, -1), colors.HexColor('#fef3c7')),\n"
    "        ('BOX',           (0, 0), (-1, -1), 1, colors.HexColor('#f59e0b')),\n"
    "        ('TOPPADDING',    (0, 0), (-1, -1), 6),\n"
    "        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),\n"
    "        ('LEFTPADDING',   (0, 0), (-1, -1), 8),\n"
    "        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),\n"
    "        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),\n"
    "    ]))\n"
    "    story.append(warn_tbl)\n"
    "    story.append(Spacer(1, 3*mm))\n"
    "    story.append(Paragraph(\n"
    "        'Present this token at the parking entry gate.',\n"
    "        ParagraphStyle('note', fontSize=8, alignment=TA_CENTER,\n"
    "                       textColor=colors.HexColor('#94a3b8'), fontName='Helvetica-Oblique')\n"
    "    ))\n"
)

new_src = src[:i] + new_footer + src[j:]
p.write_text(new_src, encoding='utf-8')
print("PDF footer patched OK!")
