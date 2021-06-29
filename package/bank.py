
import json
import boto3
import os

bank_table = os.environ['BANK_TABLE']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(bank_table)


def getBalanceOfAccount(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    path = event["path"]
    account_id = path.split("/")[-1]
    response = table.get_item(
        Key={
            'pk': account_id
        }
    )
    item = response['Item']
    return {
        'statusCode' : 200,
        'body' : json.dumps(item)
    }
    
def putAccountInfo(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    path = event["path"]
    # account_id = path.split("/")[-1] # ["user", "id"]
    
    body = json.loads(event["body"])
    print(body)
    # print(account_id)
    item = {
        # 'pk': account_id,
        'ID': body["ID"],
        'owner_name': body["owner_name"],
        'balance': body["balance"],
        'salary': body["salary"]
        
    }
    print(json.dumps(item))
    table.put_item(
      Item=item
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
def getIfCompanyIsVerified(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    path = event["path"]
    company_id = path.split("/")[-1]
    response = table.get_item(
        Key={
            'pk': company_id
        }
    )
    item = response['Item']
    return {
        'statusCode' : 200,
        'body' : json.dumps(item)
    }
    
def putVerifiedCompany(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    path = event["path"]
    company_id = path.split("/")[-1] # ["user", "id"]
    
    body = json.loads(event["body"])
    print(body)
    print(company_id)
    item = {
        'pk': company_id,
        'ID': body["ID"],
        'company_name': body["company_name"]
    
        
    }
    print(json.dumps(item))
    table.put_item(
      Item=item
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
def getSalary(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    path = event["path"]
    account_id = path.split("/")[-1]
    response = table.get_item(
        Key={
            'pk': account_id
        }
    )
    item = response['Item']
    return {
        'statusCode' : 200,
        'body' : json.dumps(item)
    }
    
def putSalary(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    path = event["path"]
    account_id = path.split("/")[-1] # ["user", "id"]
    
    body = json.loads(event["body"])
    print(body)
    print(putSalary)
    item = {
        'pk': account_id,
        'ID': body["ID"],
        'salary': body["salary"]
    }
    print(json.dumps(item))
    table.put_item(
      Item=item
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }