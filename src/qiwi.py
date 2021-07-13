import arrow as arrow
from dateutil.relativedelta import relativedelta
import aiohttp
import time
import uuid

API_TOKEN = 'eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjZpZmV5MC0wMCIsInVzZXJfaWQiOiI3OTExNzY4NDg4MiIsInNlY3JldCI6IjE2YzcyYWU0NmMxNmM1NjY0YjIzNGQzNmI0YzQ2ZTkxNjFiNDU5NmZmNDI4ZGY3ZjdiOTMwMTZlYWVkMjI2MDIifX0='
# API_TOKEN = '2904fff5d1cefe58ca1a0759105072c3'
my_login = '79117684882'


async def check_status(bill_id):
    async with aiohttp.ClientSession() as session:
        headers = {
            'authorization': 'Bearer ' + API_TOKEN,
            'Accept': 'application/json',
        }
        async with session.get(f'https://edge.qiwi.com/payment-history/v2/transactions/{bill_id}?type=OUT', headers = headers) as resp:
            if resp.status == 200:
                return await resp.json()


async def check_status_p2p(bill_id):
    async with aiohttp.ClientSession() as session:
        headers = {
            'authorization': 'Bearer ' + API_TOKEN,
            'Accept': 'application/json',
        }
        async with session.get(f'https://api.qiwi.com/partner/bill/v1/bills/{bill_id}', headers = headers) as resp:
            if resp.status == 200:
                return await resp.json()


# Перевод на QIWI Кошелек
async def send_qiwi(user, to_qw, sum_p2p):
    async with aiohttp.ClientSession() as session:
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + API_TOKEN,
            'Accept': 'application/json',
        }

        json = {
            "sum": {"amount": "", "currency": ""},
            "paymentMethod": {"type": "Account", "accountId": "643"},
            "comment": str(user), # комментарий платежа
            "fields": {"account": ""},
            'id': str(int(time.time() * 1000)),
        }

        json['sum']['amount'] = str(sum_p2p)
        json['sum']['currency'] = '643'
        json['fields']['account'] = str(to_qw)

        print(json)
        async with session.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments', headers = headers, json = json) as resp:
            print(resp.status)
            if resp.status == 200:
                return await resp.json()


async def send_card(user, bank_id, amount, card_no):
    async with aiohttp.ClientSession() as session:
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + API_TOKEN,
            'Accept': 'application/json',
        }
        json = {
            'id': str(int(time.time() * 1000)),
            "sum": {
                    "amount": str(amount),
                    "currency":"643"
            },
            "paymentMethod": {
                "type":"Account",
                "accountId":"643"
            },
            "comment": str(user), # комментарий платежа
            "fields": {
                    "account": str(card_no), # card no
                    "account_type": "1", # 1
                    #"exp_date": exp_date # MMYY
            }
        }
        async with session.post(f'https://edge.qiwi.com/sinap/api/v2/terms/{bank_id}/payments', headers = headers, json = json) as resp:
            print(resp.status)
            if resp.status == 200:
                return await resp.json()


async def check_card_system(card_number):
    async with aiohttp.ClientSession() as session:
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        }
        async with session.post('https://qiwi.com/card/detect.action', data = {'cardNumber': card_number }) as resp:
            if resp.status == 200:
                return await resp.json()


async def create_p2p_link(user: int, amount: int):
    async with aiohttp.ClientSession() as session:
        utc = arrow.utcnow().shift(hours=1)
        local = utc.to('Europe/Moscow') + relativedelta(minutes=30)
        timestr = local.format('YYYY-MM-DDTHH:mm:ssZZ')
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'Bearer ' + API_TOKEN,
            'Accept': 'application/json',
        }
        json = {
            "amount": {
                "currency": "RUB",
                "value": amount
            },
            "comment": user,
            "expirationDateTime": timestr, #'2021-03-15T23:02:00+03:00'
            "customFields" : {
                "paySourcesFilter":"qw,card"
            }
        }
        async with session.put(f'https://api.qiwi.com/partner/bill/v1/bills/{uuid.uuid1()}', headers = headers, json = json) as resp:
            if resp.status == 200:
                return await resp.json()


