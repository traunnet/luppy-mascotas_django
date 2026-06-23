import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from django.http import HttpResponse


def generar_recibo_pdf(usuario, venta, items):
    buffer = io.BytesIO()
    
    # 1. Configuración del documento
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    story = [] 
    styles = getSampleStyleSheet()

    # 2. Encabezado
    titulo_estilo = ParagraphStyle('Titulo', parent=styles['Heading1'], alignment=TA_CENTER)
    story.append(Paragraph(f"RECIBO DE VENTA #00{venta.id}", titulo_estilo))
    story.append(Spacer(1, 12))

    # 3. Información General (Usando los nombres exactos de tu modelo Venta)
    # Usamos fecha_venta que es el DateTimeField de tu modelo
    fecha_str = venta.fecha_venta.strftime('%d/%m/%Y %H:%M')
    
    info = [
        [f"Fecha: {fecha_str}", f"Cliente ID: {venta.id_cliente_id}"],
        [f"Total: ${venta.total}", f"Estado: {venta.estado}"]
    ]
    tabla_info = Table(info, colWidths=[10*cm, 8*cm])
    story.append(tabla_info)
    story.append(Spacer(1, 20))

    # 4. Tabla de Productos (Navegando por las relaciones de DetalleVenta)
    data = [['Producto', 'Cantidad', 'Precio Unit.', 'Subtotal']]
    
    for item in items:
        # Accedemos: item -> id_inventario -> id_tipo_producto -> nombre_producto
        nombre_prod = item.id_inventario.id_tipo_producto.nombre_producto
        subtotal = item.cantidad * item.precio_unitario
        
        data.append([
            nombre_prod, 
            str(item.cantidad), 
            f"${item.precio_unitario}", 
            f"${subtotal}"
        ])

    # Estilo de la tabla de productos
    tabla_productos = Table(data, colWidths=[8*cm, 3*cm, 3*cm, 4*cm])
    tabla_productos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.cadetblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    story.append(tabla_productos)

    # 5. Finalización
    doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="recibo_{venta.id}.pdf"'
    
    return response