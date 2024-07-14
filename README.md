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
   ```
   
## Ejemplos
### Ejemplos de JSON de Solicitud
Para un campo de filtro de tipo STRING:
```
{
    "your_dataset.your_table": "my_dataset.my_table",
    "fields": ["field1", "field2", "field3"],
    "filter_field": "field1",
    "filter_value": "some_value",
    "filter_value_data_type": "STRING"
}
```
Para un campo de filtro de tipo INT64:
```
{
    "your_dataset.your_table": "my_dataset.my_table",
    "fields": ["field1", "field2", "field3"],
    "filter_field": "field1",
    "filter_value": 12345,
    "filter_value_data_type": "INT64"
}
```

### Respuesta
```
{
    "status": "success",
    "data": [
        {
            "field1": "value1",
            "field2": "value2",
            "field3": "value3"
        },
        ...
    ]
}
```

## Autenticación
### Crear una API Key en Google Cloud Console:
- Navega a API & Services > Credentials.
- Crea una nueva API Key y guárdala.

### Configurar y Desplegar el API Gateway
Crear el archivo api-config.yaml:

```
swagger: "2.0"
info:
  title: "Query BigQuery API"
  description: "API for querying BigQuery via Cloud Function"
  version: "1.0.0"
paths:
  /queryBigQuery:
    post:
      summary: "Invoke Cloud Function"
      operationId: queryBigQuery
      x-google-backend:
        address: https://.........   cloudfunctions.net/queryBigQuery
      responses:
        '200':
          description: "A successful response"
      security:
        - api_key: []
securityDefinitions:
  api_key:
    type: "apiKey"
    name: "Authorization"
    in: "header"
```

### Crear la Configuración del API:
```
gcloud api-gateway api-configs create querybigqueryapi-config \
    --api=querybigqueryapi \
    --openapi-spec=api-config.yaml \
    --project=xxx
```

### Crear el Gateway:
```
gcloud api-gateway gateways create querybigqueryapi-gateway \
    --api=querybigqueryapi \
    --api-config=querybigqueryapi-config \
    --location=us-central1 \
    --project=xxx
```

### Obtener la url 
```
gcloud api-gateway gateways describe querybigqueryapi-gateway \
    --location=us-central1 \
    --project=laboratoria-prologue
```

https://[defaultHostname]/queryBigQuery

Configurar la Solicitud en Postman:
Método HTTP: POST
URL: https://[defaultHostname]/queryBigQuery
Encabezados:
Content-Type: application/json
Authorization: YOUR_API_KEY
