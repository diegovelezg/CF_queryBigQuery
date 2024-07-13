import functions_framework
from google.cloud import bigquery
import os
from flask import jsonify, request

# Función para inicializar el cliente de BigQuery
def get_bigquery_client():
    # Establece la variable de entorno para las credenciales de Google Cloud
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'
    # Crea y devuelve un cliente de BigQuery
    return bigquery.Client()

# Define una Cloud Function que manejará solicitudes HTTP
@functions_framework.http
def query_bigquery(request):
    """Función de Cloud HTTP para consultar BigQuery.
    Args:
        request (flask.Request): El objeto de solicitud.
    Returns:
        Los resultados de la consulta en formato JSON.
    """
    try:
        # Extrae los parámetros de la solicitud JSON
        request_json = request.get_json(silent=True)
        dataset_table = request_json.get('your_dataset.your_table')
        fields = request_json.get('fields')
        filter_field = request_json.get('filter_field')
        filter_value = request_json.get('filter_value')
        filter_value_data_type = request_json.get('filter_value_data_type', 'STRING').upper()

        # Verifica que todos los parámetros requeridos estén presentes
        if not all([dataset_table, fields, filter_field, filter_value, filter_value_data_type]):
            return jsonify({
                "status": "error",
                "message": "Falta uno o más parámetros requeridos: your_dataset.your_table, fields, filter_field, filter_value, filter_value_data_type."
            }), 400

        # Inicializa el cliente de BigQuery
        client = get_bigquery_client()

        # Asegura que fields sea una lista, incluso si es un solo campo
        if isinstance(fields, str):
            fields = [fields]

        # Construye la consulta SQL utilizando los parámetros proporcionados
        fields_str = ", ".join(fields)  # Convierte la lista de campos en una cadena separada por comas
        query = f"""
            SELECT {fields_str}
            FROM `{dataset_table}`
            WHERE {filter_field} = @filter_value
            LIMIT 10
        """

        # Crea un parámetro de consulta con el tipo de dato adecuado
        query_parameter = bigquery.ScalarQueryParameter("filter_value", filter_value_data_type, filter_value)
        # Configura la consulta con el parámetro
        job_config = bigquery.QueryJobConfig(
            query_parameters=[query_parameter]
        )
        
        # Ejecuta la consulta en BigQuery
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()  # Obtiene los resultados de la consulta

        # Convierte los resultados en una lista de diccionarios
        rows = [dict(row) for row in results]
        
        # Devuelve los resultados en formato JSON
        return jsonify({
            "status": "success",
            "data": rows
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al realizar la consulta: {str(e)}"
        }), 500
