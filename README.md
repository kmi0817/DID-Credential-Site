# Capstone Credential 🗎

## 1. Environment

| Type       | Language           |
| ---------- | ------------------ |
| **DID**    | hyperledger indy   |
| **Server** | Flask              |
| Client     | Webix, JavaScript  |
| Data       | SQLAlchemy, JSON   |

## 2. Flask Setting

- Mac
```
pip3 install flask
pip3 install requests
pip3 install flask_sqlalchemy
```

- Windows
```
pip install flask
pip install requests
pip install flask_sqlalchemy
```

## 3. How to run?

```
export FLASK_APP=app
export FLASK_ENV=development
flask run # or python3 run.py
```

## 4. Project Info

✔ Capstone Project from the University
✔ 2 members (including me) worked together

## 5. How to issue a credential? 🤔

    1) Login First, if you want to issue a credential
    2) Move to 'Issue Credential' menu
    3) Select credential-definition that you want: form_cashTransaction
    4) Enter information: creditor, debtor, amount, debt_term, approved_date
    5) Click 'Submit' then you can have your own credential with CapstoneCredential_no

## 6. How it works 🙋

    0) 2 Docker Servers
        - Alice: client
        - Faber: issuer
    1) Alice is connected with Faber when a client enters 'Issue Credential' menu.
        The process of connection:
            Faber Sends Invitation
            Alice receive the Invitation
    3) ...
