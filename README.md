# PRISMA Inteligente · sitio web

Sitio corporativo estático (HTML5 + CSS + JavaScript, sin dependencias ni build).

## 1. Estructura

```
prisma-web/
├── index.html          Página completa (una sola página con anclas)
├── styles.css          Estilos. Identidad visual en variables :root
├── script.js           PRISMA_CONFIG (datos editables) + interacción
├── assets/
│   ├── favicon.svg     Marca provisional (PLACEHOLDER)
│   └── img/
│       ├── hero-aerial.jpg      Hero (PLACEHOLDER generado)
│       ├── band-aerial.jpg      Franja metodología + insight destacado (PLACEHOLDER)
│       ├── cap-*.jpg            8 miniaturas de capacidades (gráficos)
│       └── og-image.jpg         Imagen para redes sociales 1200×630
├── netlify.toml        Cabeceras y caché para Netlify
└── tools/gen_images.py Script que generó las imágenes provisionales
```

Secciones y anclas: `#inicio` · `#que-hacemos` (Todo está conectado) · `#metodologia` · `#servicios` · `#intelligence` · `#capacidades` · `#programas` · `#valor` · `#nosotros` (`#fundadores`) · `#insights` · `#contacto`.

## 2. Ejecutar localmente

Cualquier servidor estático sirve. Desde la carpeta `prisma-web`:

```bash
python3 -m http.server 8080
# o
npx serve .
```

Abra http://localhost:8080. También funciona abriendo `index.html` con doble clic, aunque un servidor local es más fiel al comportamiento real.

## 3. Placeholders pendientes

| Elemento | Dónde | Estado actual |
| --- | --- | --- |
| Correo, teléfono, ubicación, LinkedIn | `script.js` → `PRISMA_CONFIG.contact` / `company.location` | Etiqueta amarilla PLACEHOLDER |
| Envío del formulario | `script.js` → `PRISMA_CONFIG.form` | Modo `demo`: valida pero no envía |
| Perfil de Francisco Barboza (cargo, formación, bio, foto, LinkedIn) | `script.js` → `PRISMA_CONFIG.founders[1]` | Recuadro PLACEHOLDER |
| Fotos de fundadores | `founders[0].photo`, `founders[1].photo` | Monogramas MA / FB |
| URL de PRISMA Intelligence | `PRISMA_CONFIG.links.intelligenceUrl` | El botón abre el formulario con el interés precargado |
| Página de equipo | `links.teamUrl` | El botón baja a los perfiles |
| Artículos de Insights | `PRISMA_CONFIG.insights` y `links.insightsUrl` | Tarjetas "En preparación"; el enlace invita a recibirlos |
| Fotografía hero y franjas | `assets/img/hero-aerial.jpg`, `band-aerial.jpg` | Vistas aéreas generadas por código |
| Logo y favicon | `index.html` (SVG del header/footer) y `assets/favicon.svg` | Prisma provisional |
| Dominio | `index.html`: `canonical`, `og:url`, `og:image`, JSON-LD `url`/`logo` | `DOMINIO-PENDIENTE.com` |

Con `showPlaceholders: false` en `PRISMA_CONFIG`, los datos vacíos se ocultan en lugar de mostrarse como etiqueta.

## 4. Cómo reemplazar contenido

**Datos de contacto.** Edite `PRISMA_CONFIG.contact` en `script.js`:

```js
contact: {
  email: 'contacto@su-dominio.com',
  phone: '+506 0000 0000',
  linkedin: 'https://www.linkedin.com/company/...'
}
```

Aparecen automáticamente en Contacto y en el footer (no hay datos repetidos en el HTML).

**Perfil de Francisco.** Complete `founders[1]`:

```js
{
  name: 'Francisco Barboza',
  role: 'Cofundador',
  photo: 'assets/img/founder-francisco.jpg',
  linkedin: 'https://www.linkedin.com/in/...',
  credentials: ['Grado 1', 'Grado 2'],
  bio: 'Dos o tres líneas de trayectoria.'
}
```

**Fotografías.** Reemplace los archivos manteniendo el nombre (o cambie la ruta en `styles.css`, busque `hero-aerial.jpg` y `band-aerial.jpg`):

- `hero-aerial.jpg`: 2400×1400 px, JPG calidad 75–80, menos de 400 KB. Operación agroindustrial moderna. El sujeto conviene a la derecha, porque el lado izquierdo lleva el texto bajo el degradado azul.
- `band-aerial.jpg`: 1600×1000 px. Cultivo o planta de proceso.
- `cap-*.jpg`: 640×360 px. Pueden seguir siendo gráficos o pasar a fotografía.
- Fotos de fundadores: cuadradas, 600×600 px, en `assets/img/`.

Actualice también el texto `aria-label`/`alt` si la nueva imagen muestra otra cosa.

**Formulario.**
- En Netlify: `provider: 'netlify'`. El formulario ya tiene `data-netlify="true"` y honeypot; las solicitudes aparecen en el panel de Netlify › Forms, donde se configuran avisos por correo.
- Formspree u otro servicio: `provider: 'endpoint'`, `endpoint: 'https://formspree.io/f/XXXX'`.

**Colores y tipografía.** Todo está en `:root` al inicio de `styles.css`.

## 5. Publicar en producción (recomendación)

**Netlify** es la opción más directa porque resuelve hosting, HTTPS y el formulario sin backend:

1. Suba la carpeta a un repositorio de GitHub (o arrástrela en app.netlify.com › Add new site › Deploy manually).
2. Build command: vacío. Publish directory: `.` (raíz).
3. En `script.js` ponga `form.provider: 'netlify'` y vuelva a publicar.
4. Conecte el dominio (Domain management) y active HTTPS (automático).
5. Reemplace `DOMINIO-PENDIENTE.com` en `index.html` por el dominio real.
6. En Forms › Form notifications, agregue el correo que recibirá las solicitudes.
7. Registre el sitio en Google Search Console y envíe la URL principal.

Alternativas: Vercel (igual de simple; use Formspree para el formulario), GitHub Pages (gratis; Formspree) o hosting tradicional (suba los archivos por FTP a `public_html`).
