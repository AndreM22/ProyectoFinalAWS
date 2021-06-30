
import json
import boto3
import os

bank_table = os.environ['BANK_TABLE']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(bank_table)


def putNewAccount(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    path = event["path"]
    account_id = path.split("/")[-1] # ["account", "id"]
    
    body = json.loads(event["body"])
    print(body)
    print(account_id)
    item = {
        'pk': account_id,
        'sk': "info",
        'name': body["name"],
        'money_amount': body["money_amount"],
        'company_name': body["company_name"],
        'company_nit': body["company_nit"],
        'company_type': body["company_type"],
        'monthly_salary': body["monthly_salary"],
        "daily_transactions":body["daily_transactions"]
    }
    print(json.dumps(item))
    table.put_item(
       Item=item
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Account registered succesfully!')
    }