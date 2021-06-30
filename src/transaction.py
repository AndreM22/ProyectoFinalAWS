import json
import boto3
import os
import csv
from boto3.dynamodb.conditions import Key, Attr

bank_table = os.environ['BANK_TABLE']
s3 = boto3.client('s3')
company_table = os.environ['COMPANIES_TABLE']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(bank_table)
table_company = dynamodb.Table(company_table)
records={}

def getTransactionInformation(event, context):
    path = event["path"]
    print(json.dumps(event))
    transaction_id = path.split("/")[-1]
    response = table.get_item(
    Key={
            'pk': transaction_id,
            'sk': 'info'
        }
    )
    item = response['Item']
    return {
        'statusCode': 200,
        'body': json.dumps(item)
        }
        
def putTransactionInformation(event, context):
    path = event["path"]
    transaction_id = path.split("/")[-1]
    body = json.loads(event['body'])
    s = body["sender"]
    r = body["receiver"]
    ammount = body["ammount"]
    sender = getUser(s)
    receiver = getUser(r)
    condition1 = True;
    condition3 = True;
    condition4 = getCompanyInfo(sender)
    if not condition4:
        export_s3_2_dynamo(event, context)
        compa = getCompanyInfo(sender)
        if compa: 
            print ('Get a company succesfully from S3')
        else: 
            put_company(sender)
            print ('The company was not verified, but now is in the dynamoDB table')
            return{
                'statusCode': 200,
                'body': json.dumps('Transaction rejected.\\n Motive: Company not verified')
            }
    else:
        company = getCompany(sender)
        if company['sk'] == 'unverified':
            return{
                'statusCode': 200,
                'body': json.dumps('Transaction rejected.\\n Motive: Company not verified')
            }
            
        
    if ammount > 20000 :
        condition1 = cond1(sender)
    condition2 = cond2(receiver)
    if ammount > 10000 :
        condition3 = cond3(sender, ammount)
    if condition1 and condition2 and condition3:
        if sender["money_amount"] < ammount:
            return{
            'statusCode': 200,
            'body': json.dumps("Transaction rejected.\\n Motive: Not enough money in sender account")
            }
        else:
            table.put_item(
                Item={
                    'pk': transaction_id,
                    'sk': 'info',
                    'sender': s,
                    'receiver': r,
                    'ammount': ammount
                }
            )
            updateUser(s, -ammount, sender)
            updateUser(r, ammount, receiver)
        return{
            'statusCode': 200,
            'body': json.dumps('Transaction completed!')
        }
    elif condition1 and condition2 and (not condition3): 
        return{
                'statusCode': 200,
                'body': json.dumps("Transaction rejected.\\n Motive: Less than 100$ in sender account if the transaction is made.")
            }
    elif condition1 and condition3 and (not condition2):
        return{
                'statusCode': 200,
                'body': json.dumps("Transaction rejected.\\n Motive: The receiver account can't receive more transactions for today")
            }
    elif condition2 and condition3 and (not condition1):
        return{
                'statusCode': 200,
                'body': json.dumps("Transaction rejected.\\n Motive: Suspicious transaction")
            }
    
def getUser(user_id):
    response = table.get_item(
    Key={
            'pk': user_id,
            'sk': 'info'
        }
    )
    item = response['Item']
    return item
    
def updateUser(user_id, ammount, user):
    print(user)
    table.update_item(
    Key={
        'pk': user_id,
        'sk': 'info'
    },
    UpdateExpression='SET money_amount = :val1, daily_transactions = :val2',
    ExpressionAttributeValues={
        ':val1': int(user["money_amount"] + ammount),
        ':val2': int(user["daily_transactions"] + 1)
    }
)

def cond1(user):
    return user["monthly_salary"] > 2000
def cond2(user):
    return not user["daily_transactions"] == 5
def cond3(user, ammount):
    return user["money_amount"]-ammount > 100
    
def getCompanyInfo(user):
    
    items = getCompany(user)
    if len(items):
        return True
    else:
        return False
        
def getCompany(user):
    company_name = user["company_name"]
    company_nit = user["company_nit"]
    company_type = user["company_type"]
    response = table_company.scan(
        FilterExpression=Attr('name').eq(company_name) & Attr("nit").eq(company_nit) & Attr("type").eq(company_type)
    )
    return (response['Items'][0])
    
        
        
def export_s3_2_dynamo(event, context):
    try: 
        bucket = "bucket-prueba-company-1"
        key = "TableEmpresas.csv"

        print('Bucket: ',bucket, ' key: ', key)

        csv_file = s3.get_object(Bucket = bucket, Key = key)
        record_list = csv_file['Body'].read().decode('utf-8').split('\n')
        csv_reader =csv.reader(record_list, delimiter=',', quotechar='"')
        for row in csv_reader:
            company_id=row[0]
            verified = row[1]
            name=row[2]
            nit=row[3]
            type=row[4]
            print('Company_id: ', company_id, ' Verified: ', verified, ' Name: ', name, ' NIT: ', nit, ' Type:', type)
            add_to_db = table_company.put_item(
                Item = {
                    'pk' : int(company_id),
                    'sk' : verified,
                    'name' : str(name),
                    'nit' : int(nit),
                    'type' : str(type),
                })
            print('Succesfully added records to DynamoDB')

    except Exception as e: 
        print(str(e))
    
def put_company(user):
    company_name = user["company_name"]
    company_nit = user["company_nit"]
    company_type = user["company_type"]
    if not company_name in records:
        records[company_name] = 1
    response = table_company.put_item(
            Item={
                    'pk': len(records),
                    'sk': 'unverified',
                    'name': company_name,
                    'nit': company_nit,
                    'type': company_type
                }
    )

    