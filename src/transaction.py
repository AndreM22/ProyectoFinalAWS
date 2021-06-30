import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

bank_table = os.environ['BANK_TABLE']
company_table = os.environ['COMPANIES_TABLE']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(bank_table)
table_company = dynamodb.Table()
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
    
    getCompany(sender)
        
    if ammount > 20000 :
        condition1 = cond1(sender)
    condition2 = cond2(receiver)
    if ammount > 10000 :
        condition3 = cond3(sender, ammount)
    if condition1 and condition2 and condition3:
        if sender["money_amount"] < ammount:
            return{
            'statusCode': 200,
            'body': "Not enough money in sender account"
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
                'body': "Transaction rejected.\n Motive: Less than 100$ in sender account if the transaction is made."
            }
    elif condition1 and condition3 and (not condition2):
        return{
                'statusCode': 200,
                'body': "Transaction rejected.\n Motive: The receiver account can't receive more transactions for today"
            }
    elif condition2 and condition3 and (not condition1):
        return{
                'statusCode': 200,
                'body': "Transaction rejected.\n Motive: Suspicious transaction"
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
    table.update_item(
    Key={
        'user_id': user_id,
        'sk': 'info'
    },
    UpdateExpression='SET money_amount = :val1, daily_transactions = :val2',
    ExpressionAttributeValues={
        ':val1': user["money_amount"] + ammount,
        ':val2': user["daily_transactions"] + 2
    }
)

def cond1(user):
    return user["monthly_salary"] < 2000
def cond2(user):
    return not user["daily_transactions"] == 5
def cond3(user, ammount):
    return user["money_amount"]-ammount > 100
    
def getCompany(user):
    company_name = user["company_name"]
    company_nit = user["nit"]
    company_type = user["company_type"]
    response = table_company.scan(
        FilterExpression=Attr('name').eq(company_name) & Attr("nit").eq(company_nit) & Attr("type").eq(company_type)
    )
    items = response['Items']
    print(items)
    