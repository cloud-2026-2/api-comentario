import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    
    # Leer variables de entorno (DynamoDB y S3)
    nombre_tabla = os.environ["TABLE_NAME"]
    nombre_bucket = os.environ["BUCKET_NAME"]
    
    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    
    # 1. Guardar en DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response_dynamo = table.put_item(Item=comentario)
    
    # 2. Guardar en Amazon S3 (Estrategia Ingesta Push)
    s3 = boto3.client('s3')
    # Convertimos el diccionario "comentario" a un formato de texto JSON legible
    comentario_json_string = json.dumps(comentario)
    
    # Subimos el archivo a S3 usando el uuidv1 como nombre de archivo
    nombre_archivo = f"{uuidv1}.json"
    response_s3 = s3.put_object(
        Bucket=nombre_bucket,
        Key=nombre_archivo,
        Body=comentario_json_string,
        ContentType='application/json'
    )
    
    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response_dynamo': response_dynamo,
        'response_s3': response_s3
    }
