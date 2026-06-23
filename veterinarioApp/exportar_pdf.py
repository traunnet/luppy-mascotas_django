from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.http import HttpResponse
from clienteApp.models import Venta

def exportar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Reporte_Ventas_Luppy.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        textColor=colors.HexColor("#10B981"), 
        fontSize=22,
        spaceAfter=20
    )
    elements.append(Paragraph("Reporte de Ventas - Luppy", title_style))
    elements.append(Paragraph("Sede: Bogotá, Colombia", styles['Normal']))
    elements.append(Spacer(1, 20))

    data = [['Fecha', 'Cliente', 'Estado', 'Total']]
    ventas = Venta.objects.all().order_by('-fecha_venta')

    for v in ventas:
        fecha = v.fecha_venta.strftime("%d/%m/%Y") if v.fecha_venta else "S/F"

        cliente = str(v.id_cliente) if v.id_cliente else "Anónimo"
        estado = str(v.estado)
        total = f"${float(v.total):,.2f}" if v.total else "$0.00"

        data.append([fecha, cliente, estado, total])

    t = Table(data, colWidths=[80, 220, 100, 80])
    
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#10B981")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'), 
    ]))

    elements.append(t)
    
    doc.build(elements)
    return response