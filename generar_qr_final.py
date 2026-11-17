"""
Genera el avatar para Instagram (1080x1080) y los códigos QR estilizados de FOXHUNTED.
Cuando tengas tu usuario de GitHub y tu nuevo @ de Instagram, cambia las variables
GITHUB_PAGES_URL e INSTAGRAM_URL y vuelve a ejecutar este script.
"""

import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
QR_DIR = os.path.join(BASE_DIR, "qr")
os.makedirs(QR_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# EDITA ESTAS DOS LÍNEAS CUANDO TENGAS TU REPO DE GITHUB Y TU NUEVO INSTAGRAM:
# ---------------------------------------------------------------------------
GITHUB_PAGES_URL = "https://foxhuntedtech-lang.github.io/links.html"
INSTAGRAM_URL = "https://instagram.com/foxhunted.tech"
WHATSAPP_URL = "https://wa.me/524448656388?text=Hola%20FOXHUNTED,%20necesito%20cotizar%20un%20servicio."

INK = (21, 21, 23)
PAPER = (242, 236, 225)
YELLOW = (244, 208, 25)
MAGENTA = (230, 28, 122)
CYAN = (0, 184, 217)


def make_styled_qr(url, filename, label_text, accent_rgb=YELLOW):
    """Genera un QR nítido en tarjeta estilo FOXHUNTED listo para imprimir o poner en el flyer."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=18,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=INK, back_color=PAPER).convert("RGB")

    qw, qh = qr_img.size
    pad_x = 70
    pad_top = 70
    footer_h = 130
    card_w = qw + pad_x * 2
    card_h = qh + pad_top + footer_h

    card = Image.new("RGB", (card_w, card_h), PAPER)
    d = ImageDraw.Draw(card)

    # Marco exterior tinta + franja superior de acento
    d.rectangle((0, 0, card_w - 1, card_h - 1), outline=INK, width=14)
    d.rectangle((14, 14, card_w - 15, 34), fill=accent_rgb)

    card.paste(qr_img, (pad_x, pad_top))

    # Etiqueta inferior
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 34)
    except OSError:
        font = ImageFont.load_default()

    bbox = d.textbbox((0, 0), label_text, font=font)
    tw = bbox[2] - bbox[0]
    tx = (card_w - tw) // 2
    ty = pad_top + qh + 36
    d.rectangle((pad_x, ty - 14, card_w - pad_x, ty + 54), fill=INK)
    d.text((tx, ty), label_text, font=font, fill=accent_rgb)

    out = os.path.join(QR_DIR, filename)
    card.save(out, "PNG")
    return out


def make_ig_avatar():
    """Genera foto de perfil 1080x1080 para el nuevo Instagram exclusivo de FOXHUNTED."""
    S = 1080
    img = Image.new("RGB", (S, S), INK)
    d = ImageDraw.Draw(img)

    # Marco de mira sutil
    m = 130
    L = 130
    for pts in [
        [(m, m + L), (m, m), (m + L, m)],
        [(S - m - L, m), (S - m, m), (S - m, m + L)],
        [(m, S - m - L), (m, S - m), (m + L, S - m)],
        [(S - m - L, S - m), (S - m, S - m), (S - m, S - m - L)],
    ]:
        d.line(pts, fill=PAPER, width=22)

    # Líneas de mira magenta
    d.line([(S // 2, 145), (S // 2, 220)], fill=MAGENTA, width=16)
    d.line([(S // 2, S - 220), (S // 2, S - 145)], fill=MAGENTA, width=16)

    # Zorro geométrico centrado (escala ~2.6x sobre fondo papel claro dentro de la mira)
    cx, cy = S // 2, S // 2 + 10
    def pts(coords):
        return [(cx + x * 2.55, cy + y * 2.55) for x, y in coords]

    d.polygon(pts([(-95, -105), (-26, -52), (26, -52), (95, -105), (82, 0),
                   (44, 68), (0, 115), (-44, 68), (-82, 0)]), fill=PAPER)
    d.polygon(pts([(-66, -12), (-16, 4), (-26, 22), (-70, 6)]), fill=MAGENTA)
    d.polygon(pts([(66, -12), (16, 4), (26, 22), (70, 6)]), fill=CYAN)
    d.polygon(pts([(-22, 64), (22, 64), (0, 94)]), fill=YELLOW)

    out = os.path.join(ASSETS_DIR, "FOXHUNTED_IG_Avatar.png")
    img.save(out, "PNG")
    return out


if __name__ == "__main__":
    wa_qr = make_styled_qr(WHATSAPP_URL, "QR_WhatsApp_FOXHUNTED.png", "WHATSAPP // 444-865-6388", YELLOW)
    hub_qr = make_styled_qr(GITHUB_PAGES_URL, "QR_Hub_Web_IG_WA.png", "WEB • WHATSAPP • IG", CYAN)
    ig_qr = make_styled_qr(INSTAGRAM_URL, "QR_Instagram_FOXHUNTED.png", "IG // @foxhunted.tech", MAGENTA)
    avatar = make_ig_avatar()
    print("Generado:", wa_qr)
    print("Generado:", hub_qr)
    print("Generado:", ig_qr)
    print("Generado:", avatar)
