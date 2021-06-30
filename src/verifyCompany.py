import json
import csv
import boto3

region ='us-east-1'
record_list = []
client = boto3.client("dynamodb")
s3 = boto3.client('s3')

# Main Event
def lambda_handler(event, context):
    compa = get_companie(7, "Factory", 1234567, "Fast Food")
    if compa: 
        print ('Get a company succesfully from Dynamo DB', compa)
        return None
    else:
        getS3 = export_s3_2_dynamo(event, context)
        compa = get_companie(7, "Factory", 1234567, "Fast Food")
        if compa: 
            print ('Get a company succesfully from S3', compa)
            return None
        else: 
            put2dynamodb = put_company(7, "Factory", 1234567, "Fast Food")
            print ('The company was not verify, but now is in the dynamoDB',put2dynamodb)
            return None

def put_company(company_id, name, nit, type):
    response = client.put_item(
        TableName = 'company_table',
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
def get_companie(company_id, name, nit, type):
    response = client.get_item(
        TableName = 'company_table',
        Key = {
            'company_id' : {
                'N' : '{}'.format(company_id),
            }
        }
    )

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