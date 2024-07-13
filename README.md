# Cloud Function para Consultas en BigQuery

Esta Cloud Function en Python permite realizar consultas a BigQuery basadas en parámetros proporcionados a través de una solicitud HTTP. La función espera recibir los nombres de la tabla y los campos a consultar, así como un campo y un valor para filtrar los resultados.

## Contenido del Repositorio

- `main.py`: Contiene el código de la Cloud Function.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar la función.
- `service_account.json`: Archivo de credenciales de la cuenta de servicio (no incluido en el repositorio por razones de seguridad).

## Configuración y Despliegue

### Pre-requisitos

1. **Cuenta de Google Cloud**: Asegúrate de tener una cuenta de Google Cloud con permisos para acceder a BigQuery.
2. **Cuenta de Servicio**: Crea una cuenta de servicio en Google Cloud y descarga el archivo JSON de credenciales.
3. **BigQuery**: Asegúrate de que la tabla de BigQuery que deseas consultar exista y que la cuenta de servicio tenga los permisos adecuados para acceder a ella.

### Configuración del Entorno

1. **Archivo `requirements.txt`**:
   - Este archivo lista las dependencias necesarias para la función. Incluye `functions-framework`, `google-cloud-bigquery`, y `Flask`.

    ```txt
    functions-framework==3.*
    google-cloud-bigquery==3.*
    Flask==2.*
    ```

2. **Archivo `service_account.json`**:
   - Este archivo debe contener las credenciales de la cuenta de servicio y debe estar en el mismo directorio que `main.py`.

### Despliegue de la Cloud Function

1. **Despliega la función en Google Cloud**:
   - Puedes desplegar la función usando la consola de Google Cloud o la CLI de `gcloud`.

   ```sh
   gcloud functions deploy query_bigquery \
       --runtime python310 \
       --trigger-http \
       --allow-unauthenticated \
       --entry-point query_bigquery
