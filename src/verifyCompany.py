import json
import csv
import boto3
import os

region ='us-east-1'
record_list = []
client = boto3.client("dynamodb")
company_table = os.environ['COMPANIES_TABLE']
s3 = boto3.client('s3')
table = client.Table(company_table)

# Main Event
def lambda_handler(event, context):
    path = event["path"]
    company_id = path.split("/")[-1]
    compa = get_companie(company_id)
    if compa: 
        print ('Get a company succesfully from Dynamo DB', compa)
        return None
    else:
        getS3 = export_s3_2_dynamo(event, context)
        compa = get_companie(company_id)
        if compa: 
            print ('Get a company succesfully from S3', compa)
            return None
        else: 
            put2dynamodb = put_company(7, "Factory", 1234567, "Fast Food")
            print ('The company was not verify, but now is in the dynamoDB',put2dynamodb)
            return None

def put_company(company_id):
    response = table.put_item(
        Item = {
            'company_id' : {
                'N' : '{}'.format(company_id),
            },
            'name' : {
                'S' : '{}'.format(name),
            },
            'nit' : {
                'N' : '{}'.format(nit),
            },
            'type' : {
                'S' : '{}'.format(type),
            }
        }
    )
    return{
            'statusCode': 200,
            'body': json.dumps('Company added completed!')
        }
def get_companie(company_id):
    response = table.get_item(
        Key = {
            'company_id' : company_id
            }
    )
    
    item = response['Item']
    print(item)
    return item

def export_s3_2_dynamo(event, context):
    try: 
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print('Bucket: ',bucket, ' key: ', key)

        csv_file = s3.get_object(Bucket = bucket, Key = key)
        record_list = csv_file['Body'].read().decode('utf-8').split('\n')
        csv_reader =csv.reader(record_list, delimiter=',', quotechar='"')

        for row in csv_reader:
            company_id=row[0]
            name=row[1]
            nit=row[2]
            type=row[3]

            print('Company_id: ', company_id, ' Name: ', name, ' NIT: ', nit, ' Type:', type)

            add_to_db = client.put_item(
                TableName = 'company_table', 
                Item = {
                    'company_id' : {'N' : str(company_id)},
                    'name' : {'S' : str(name)},
                    'nit' : {'N' : str(nit)},
                    'type' : {'S' : str(type)},
                })
            print('Succesfully added records to DynamoDB')

    except Exception as e: 
        print(str(e))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }