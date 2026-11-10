# Explorandum — ensayo de independencia y publicación automática

Estado: **preparado técnicamente; NO desplegado a Cloudflare**. Este documento vive exclusivamente en una rama de pruebas. La web actual permanece en GitHub Pages y no debe interrumpirse.

## Condiciones de partida

- Proyecto de titularidad y administración exclusiva de Pat; ningún colaborador recibe acceso técnico.
- Explorandum engloba sus posibles líneas para adolescentes; Montessori y Prepdiplo son proyectos distintos, con cuentas, presupuestos y datos separados.
- Preparar un proyecto potencialmente comercial; no elegir alojamiento gratuito incompatible con uso comercial.
- Conservar la rama de recuperación `respaldo-versiones-favoritas-2026-11-09` y las páginas marcadas en `VERSIONES_FAVORITAS_NO_SOBRESCRIBIR.md`.
- La referencia pública actualmente operativa es `https://prepdiplo-web.github.io/Explorandum/`. No desactivar ni trasladar la fuente publicada antes de validar el nuevo alojamiento.
- No mezclar datos ni credenciales de Mi Aula / Prepdiplo con Explorandum.

## Arquitectura propuesta para la prueba

1. Crear un **espacio de propiedad independiente** de Explorandum en GitHub (organización gratuita), controlado exclusivamente por Pat. Crear allí **una copia independiente**, NO transferir/eliminar de golpe el repositorio actual: el traslado directo puede afectar la dirección GitHub Pages y los enlaces anteriores.
2. Crear cuenta/espacio Cloudflare **solo para Explorandum**, administrado por Pat y en plan gratuito.
3. Conectar Cloudflare Pages al nuevo repositorio de Explorandum por la integración oficial GitHub, dando acceso **solo al repositorio de Explorandum**, nunca a `mi-aula-prepdiplo`.
4. Configurar despliegue automático: producción en `main` **del repositorio NUEVO**, vista previa para ramas de desarrollo, sin tocar el `main` del repositorio original durante el ensayo. Sitio HTML estático: sin framework y sin comando de compilación; publicar desde la raíz del repositorio (si el panel exige comando, `exit 0`; directorio de salida `.`, a verificar en despliegue).
5. Hacer una prueba con un cambio inocuo y reversible en la **copia**: texto de una página de ensayo, sin alterar el diseño o páginas favoritas. Comprobar el nuevo URL `*.pages.dev` en Safari y ordenador, enlaces, imágenes, JavaScript, interacciones, navegación y recuperación de versión anterior.
6. El tráfico de vídeo del proyecto requiere análisis separado: según la política de Cloudflare, no se presume que servir vídeos MP4 mediante Pages/R2 gratuitos sea adecuado ni autorizado para distribución intensiva. **No activar el traslado completo del catálogo audiovisual** sin solución conforme a las condiciones comerciales. Evaluar vídeo externo incorporado o un servicio de vídeo permitido y su precio real antes de generar coste.
7. **Solo si todas las pruebas son satisfactorias** planificar dirección web propia, enlaces antiguos, información legal de una actividad económica y eventual desconexión de la web anterior. No realizar ninguna de estas operaciones automáticamente.

## Modelo de trabajo solicitado

- La titular pide cambios en lenguaje natural a ChatGPT.
- ChatGPT usa la conexión GitHub para editar el repositorio correcto y comprobar la versión.
- El alojamiento conectado a GitHub publica automáticamente las modificaciones aceptadas.
- ChatGPT comprueba la web y comunica resultado o incidencia.
- Solo el alta de cuentas, la concesión inicial de permisos o decisiones de pago necesitan intervención de la titular. **Actualmente no está conectada una herramienta que gestione directamente Cloudflare**, por lo que no se debe prometer configurar su panel desde este chat.

## Criterios de aceptación del ensayo

- Separación efectiva: propietario de GitHub y cuenta Cloudflare específicos de Explorandum; sin privilegios sobre Prepdiplo.
- Ninguna pérdida de versión favorita o medios existentes; alternativa de recuperación.
- Publicación sin operación manual por modificación ordinaria, sin generar cargos.
- Comprobación pública de al menos portada, navegación terrestre, cielo y cosmos, cabina submarina, vídeos de muestra y versión móvil.
- Reproducción audiovisual satisfactoria desde proveedor autorizado.
- Comprobación posterior de dominio y costes antes del cambio definitivo.

## Evidencia y límites documentales

- Cloudflare Pages integra repositorios GitHub y publica automáticamente: https://developers.cloudflare.com/pages/configuration/git-integration/github-integration/
- Cloudflare Pages Free: 500 compilaciones mensuales, 20.000 archivos por web y 25 MiB por archivo: https://developers.cloudflare.com/pages/platform/limits/
- Publicación estática sin framework: https://developers.cloudflare.com/pages/configuration/build-configuration/
- Políticas de distribución audiovisual: https://developers.cloudflare.com/fundamentals/reference/policies-compliances/delivering-videos-with-cloudflare/
- En el repositorio actual hay 112 archivos y unos 88 MiB de recursos, sin archivos individuales de más de 25 MiB. **Esto acredita tamaño, no compatibilidad legal con distribución de vídeo ni calidad de la migración.**
- Pendiente: creación y autorización de cuentas por Pat, conexión real Cloudflare, URL de prueba y pruebas reales de navegador.

## Seguridad

No solicitar contraseñas, tarjetas ni tokens en chat; no insertar claves permanentes ni credenciales de Cloudflare o Firebase en GitHub. Concesión mínima de permisos exclusivamente al nuevo repositorio Explorandum. No invocar despliegues de Mi Aula ni cambiar sus reglas.
