import requests

data = {
  "id": "db0bcbfd-45d6-4240-9b2f-4710330e954f",
  "creation_date": 1692901532001,
  "event": "PURCHASE_APPROVED",
  "version": "2.0.0",
  "data": {
    "product": {
      "id": 0,
      "ucode": "fb056612-bcc6-4217-9e6d-2a5d1110ac2f",
      "name": "Produto test postback2",
      "has_co_production": False
    },
    "affiliates": [
      {
        "affiliate_code": "Q58388177J",
        "name": "Affiliate name"
      }
    ],
    "buyer": {
      "email": "testeComprador271101postman15@example.com",
      "name": "Teste Comprador",
      "checkout_phone": "99999999900"
    },
    "producer": {
      "name": "Producer Test Name"
    },
    "commissions": [
      {
        "value": 149.5,
        "source": "MARKETPLACE",
        "currency_value": "BRL"
      },
      {
        "value": 1350.5,
        "source": "PRODUCER",
        "currency_value": "BRL"
      }
    ],
    "purchase": {
      "approved_date": 1511783346000,
      "full_price": {
        "value": 1500,
        "currency_value": "BRL"
      },
      "original_offer_price": {
        "value": 1500,
        "currency_value": "BRL"
      },
      "price": {
        "value": 1500,
        "currency_value": "BRL"
      },
      "offer": {
        "code": "test"
      },
      "checkout_country": {
        "name": "Brasil",
        "iso": "BR"
      },
      "order_bump": {
        "is_order_bump": True,
        "parent_purchase_transaction": "HP02316330308193"
      },
      "order_date": 1511783344000,
      "status": "APPROVED",
      "transaction": "HP1121336654889",
      "buyer_ip": "00.00.00.00",
      "payment": {
        "installments_number": 12,
        "type": "CREDIT_CARD"
      }
    },
    "subscription": {
      "status": "ACTIVE",
      "plan": {
        "id": 123,
        "name": "plano de teste"
      },
      "subscriber": {
        "code": "I9OT62C3"
      }
    }
  },
  "hottok": "ypwFN5FP6MX0x4wPCKVV0NdhFbkkLR1377d3bb-b62e-43e3-95df-78fd85993967"
}

response = requests.post('https://ytclient-production.up.railway.app/api/webhook/hotmart', data=data)
with open('w.html', 'w') as f:
    f.write(response.text)