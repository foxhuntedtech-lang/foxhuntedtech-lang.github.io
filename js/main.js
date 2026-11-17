document.addEventListener("DOMContentLoaded", () => {
  const pageLoadedAt = Date.now();
  let lastSubmitAt = 0;

  const menuToggle = document.getElementById("menuToggle");
  const navLinks = document.getElementById("navLinks");
  const quoteForm = document.getElementById("quoteForm");
  const serviceSelect = document.getElementById("serviceSelect");
  const serviceButtons = document.querySelectorAll("[data-service]");

  const sanitizeText = (str, maxLen) =>
    String(str || "")
      .replace(/[\u0000-\u001F\u007F]/g, " ")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, maxLen);

  // Menú móvil
  if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", () => {
      navLinks.classList.toggle("open");
    });

    navLinks.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => navLinks.classList.remove("open"));
    });
  }

  // Botones de "Cotizar este servicio" preseleccionan el formulario
  serviceButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const chosen = btn.getAttribute("data-service");
      if (serviceSelect && chosen) {
        serviceSelect.value = chosen;
      }
      document.getElementById("cotizador")?.scrollIntoView({ behavior: "smooth" });
      document.getElementById("clientName")?.focus();
    });
  });

  // Envío directo a WhatsApp con protección anti-bot (honeypot + cooldown + sanitización)
  if (quoteForm) {
    quoteForm.addEventListener("submit", (e) => {
      e.preventDefault();

      // 1. Verificar honeypot: si un bot llenó el campo oculto, abortar silenciosamente
      const honeypot = document.getElementById("companyWebsite");
      if (honeypot && honeypot.value.trim() !== "") {
        return;
      }

      // 2. Verificar tiempo mínimo de interacción humana (1.5s) y cooldown (5s)
      const now = Date.now();
      if (now - pageLoadedAt < 1500 || now - lastSubmitAt < 5000) {
        return;
      }

      const name = sanitizeText(document.getElementById("clientName").value, 60);
      if (name.length < 2) {
        return;
      }

      const device = sanitizeText(document.getElementById("deviceType").value, 40);
      const service = sanitizeText(document.getElementById("serviceSelect").value, 80);
      const details =
        sanitizeText(document.getElementById("issueDetails").value, 350) ||
        "Sin detalles adicionales.";

      lastSubmitAt = now;

      const message =
        `Hola FOXHUNTED, soy *${name}*.\n` +
        `• *Equipo:* ${device}\n` +
        `• *Servicio:* ${service}\n` +
        `• *Detalle:* ${details}`;

      const whatsappUrl = `https://wa.me/524448656388?text=${encodeURIComponent(message)}`;
      window.open(whatsappUrl, "_blank", "noopener,noreferrer");
    });
  }
});
