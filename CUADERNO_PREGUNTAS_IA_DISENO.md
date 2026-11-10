# EXPLORANDUM — Cuaderno de preguntas con inteligencia artificial

## Decisión editorial
- Los niños deben poder detener la expedición, escribir una pregunta espontánea sobre cualquier encuentro y obtener una respuesta real de IA vinculada al contexto de la especie, los hábitats de la península de Baja California y las fuentes científicas.
- Debe aparecer como una caja discreta de conversación en el **cuaderno de observación**, no encima de la grabación.
- El vídeo permanece real, libre de textos o rótulos invasivos. La conversación será una capa independiente de la película.
- Mantener las versiones favoritas intactas; implementar solo en una versión experimental con pruebas y autorización de configuración segura.

## Interfaz futura
1. Bloque «¿Qué te gustaría descubrir?» con campo de pregunta, envío, historial de respuesta y posibilidad de preguntar de nuevo.
2. El contexto incluye el nombre científico del encuentro activo, descripción, distribución regional y enlaces a las fuentes utilizadas; no inventar especies o geografía.
3. Redactar respuestas de español claro, adaptadas a lectores jóvenes, pero rigurosas. Aceptar preguntas encadenadas; no aplicar ejercicios obligatorios.
4. Si la pregunta es controvertida o sin datos, reconocer incertidumbre. Añadir enlace a fuente cuando sea posible.
5. No guardar por defecto conversaciones, ubicaciones ni datos personales de menores. Protección contra abuso y límites de consumo.
6. Un aviso claro cuando sea una respuesta de IA; no simular IA usando textos preprogramados.

## Arquitectura
- GitHub Pages es hospedaje estático: **no debe exponerse una API key en JavaScript/HTML**.
- Necesario un endpoint backend separado con credenciales en Secret Manager, CORS reducido al origen de EXPLORANDUM, controles de frecuencia y presupuesto, reglas y registro técnico mínimo no personal.
- No utilizar la infraestructura de Mi Aula/Prepdiplo para esta web sin autorización y aislamiento; son dos proyectos diferentes.
- No implementar un falso botón «Preguntar a la IA». No usar una URL de ChatGPT con query-string como sustituto de una integración fiable.
- Antes de publicar, probar mediante navegador la autenticación del endpoint, que no hay claves expuestas, la respuesta, los errores, límites y la política de datos.
- Referencia oficial: https://developers.openai.com/api/reference/overview
