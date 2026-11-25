# PRISMA Inteligente · sitio web (V2.0, alineado con las presentaciones comerciales)

Página única y autónoma: `index.html` incluye estilos, código, fuentes (Montserrat e Inter, OFL) e imágenes.
No requiere build ni dependencias. Se abre con doble clic o se publica tal cual en Netlify.

## Archivos
- `index.html`: la página (7 secciones: Inicio, Retos, Soluciones, Cómo trabajamos, Tecnología, Experiencia, Contacto).
- `og-image.jpg`: imagen de vista previa para redes (1200×630).
- `netlify.toml`: cabeceras de seguridad.

## Pendientes
- Correo comercial: aún no existe; la página solo muestra WhatsApp.
- Dominio: canonical y Open Graph apuntan a https://prismainteligente.netlify.app. Cambiar si se usa prismainteligente.com.
- Fotos de los socios y de fincas: reemplazar por originales en alta resolución.

La versión anterior (v2.0 de 12 secciones) queda en el historial de git.

## Elementos permanentes
- `<meta name="google-site-verification" …>` en el `<head>` de `index.html`: verifica la propiedad en Google Search Console. **No eliminar** en futuras versiones.
