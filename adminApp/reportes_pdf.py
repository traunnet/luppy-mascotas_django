from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO

PRIMARY_COLOR = colors.HexColor("#2C3E50")  
SECONDARY_COLOR = colors.HexColor("#16A085") 
TEXT_LIGHT = colors.whitesmoke

def dibujar_encabezado(p, titulo, width, height):
    p.setFillColor(PRIMARY_COLOR)
    p.rect(0, height - 80, width, 80, fill=1, stroke=0)
    
    p.setFillColor(TEXT_LIGHT)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 45, "Luppy & Sus Mascotas")
    
    p.setFont("Helvetica", 12)
    p.drawRightString(width - 50, height - 45, titulo.upper())
    
    p.setStrokeColor(SECONDARY_COLOR)
    p.setLineWidth(3)
    p.line(50, height - 60, width - 50, height - 60)

def generar_reporte_ventas_pdf(ventas):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    dibujar_encabezado(p, "Reporte Histórico de Ventas", width, height)
    
    data = [["ID", "Fecha", "Cliente", "Total"]]
    for v in ventas:
        cliente = f"{v.id_cliente.usuario.nombre}" if v.id_cliente else "General"
        data.append([str(v.pk), v.fecha_venta.strftime('%d/%m/%Y'), cliente, f"${float(v.total):,.0f}"])
    
    tabla = Table(data, colWidths=[50, 100, 250, 100])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), TEXT_LIGHT),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
    ]))
    
    tabla.wrapOn(p, width, height)
    pos_y = height - 150 - (len(data) * 20)
    tabla.drawOn(p, 50, max(pos_y, 50))
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def generar_reporte_clientes_pdf(clientes):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    dibujar_encabezado(p, "Listado de Clientes", width, height)
    
    data = [["Nombre Completo", "Documento", "Correo", "Teléfono"]]
    for c in clientes:
        data.append([
            f"{c.usuario.nombre} {c.usuario.apellido}", 
            c.usuario.numero_documento, 
            c.usuario.correo, 
            c.usuario.telefono
        ])
    
    tabla = Table(data, colWidths=[160, 90, 170, 80])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), TEXT_LIGHT),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#E8F6F3")]),
    ]))
    
    tabla.wrapOn(p, width, height)
    tabla.drawOn(p, 50, height - 200)
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def generar_reporte_veterinarios_pdf(veterinarios):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    dibujar_encabezado(p, "Listado de Veterinarios", width, height)
    
    data = [["Nombre", "Licencia", "Especialidad", "Teléfono"]]
    for v in veterinarios:
        data.append([
            f"{v.usuario.nombre} {v.usuario.apellido}", 
            v.numero_licencia, 
            v.especialidad, 
            v.usuario.telefono
        ])
    
    tabla = Table(data, colWidths=[150, 100, 150, 100])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), TEXT_LIGHT),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F4F4")]),
    ]))
    
    tabla.wrapOn(p, width, height)
    tabla.drawOn(p, 50, height - 200)
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer