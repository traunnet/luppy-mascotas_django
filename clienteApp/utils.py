import ssl
import smtplib
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def enviar_correo_compra(usuario, carrito, items):
    asunto = '🧾 Confirmación de compra - VetTech'

    detalles = []
    total = 0
    for item in items:
        subtotal = item.cantidad * item.precio_unitario
        total += subtotal
        detalles.append({
            "producto": item.id_inventario.id_tipo_producto.nombre_producto,
            "cantidad": item.cantidad,
            "subtotal": subtotal
        })

    mensaje_html = render_to_string("email/confirmacion_compra.html", {
        "usuario": usuario,
        "detalles": detalles,
        "total": total
    })

    mensaje_texto = (
        f"Hola {usuario.nombre} {usuario.apellido},\n\n"
        f"Gracias por tu compra 🐾\n\n"
        f"🛒 Detalle de tu pedido:\n"
        + "\n".join([f"- {d['producto']} x{d['cantidad']} = ${d['subtotal']}" for d in detalles])
        + f"\n\n💰 Total: ${total}\n\nGracias por confiar en nosotros ❤️"
    )

    # Conexión SMTP manual con SSL deshabilitado
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    smtp.ehlo()
    smtp.starttls(context=ctx)
    smtp.ehlo()
    smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    correo = EmailMultiAlternatives(
        asunto,
        mensaje_texto,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[usuario.correo],
    )
    correo.attach_alternative(mensaje_html, "text/html")

    msg = correo.message()
    smtp.sendmail(settings.EMAIL_HOST_USER, [usuario.correo], msg.as_bytes())
    smtp.quit()