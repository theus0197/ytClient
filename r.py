import requests 


data = {
  "id": "caf70e1e-6ce3-4017-b057-c895050a155f",
  "creation_date": 1693584244345,
  "event": "PURCHASE_APPROVED",
  "version": "2.0.0",
  "data": {
    "product": {
      "id": 3294410,
      "ucode": "a4dfd341-f55e-49ad-af1f-fb8ef133eacd",
      "name": "App ",
      "has_co_production": False
    },
    "affiliates": [
      {
        "affiliate_code": "",
        "name": ""
      }
    ],
    "buyer": {
      "email": "cethomas0910@gmail.com",
      "name": "Chris Thomas",
      "checkout_phone": "99999999900"
    },
    "producer": {
      "name": "Filipe Almeida De Abreu"
    },
    "commissions": [
      {
        "value": 2.48,
        "source": "MARKETPLACE",
        "currency_value": "USD"
      },
      {
        "value": 17.51,
        "source": "PRODUCER",
        "currency_value": "USD"
      }
    ],
    "purchase": {
      "approved_date": 1693584240000,
      "full_price": {
        "value": 19.99,
        "currency_value": "USD"
      },
      "original_offer_price": {
        "value": 19.99,
        "currency_value": "USD"
      },
      "price": {
        "value": 19.99,
        "currency_value": "USD"
      },
      "offer": {
        "code": "t7hwya5i"
      },
      "checkout_country": {
        "name": "United States",
        "iso": "US"
      },
      "order_bump": {
        "is_order_bump": False
      },
      "order_date": 1693584238000,
      "status": "APPROVED",
      "transaction": "HP2449012225",
      "buyer_ip": "76.106.208.28",
      "payment": {
        "installments_number": 1,
        "type": "CREDIT_CARD"
      }
    }
  }
}
response = requests.post(' https://ytclient-production.up.railway.app/api/webhook/hotmart', json=data)
with open('teste.html', 'w')as f:
    f.write(response.text)