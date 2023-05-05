# DID-Credential-Site 🗎

> Capstone Project from Dankook University<br>
> ✔ My Role : `Back-end (Flask), Front-end (Webix)` except chatting

## How to run?

### Flask Settings before run

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

### Now you can run it

```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
- You can use `python3 run.py` instead of flask run

---

## How to issue a credential? 🤔

    1) Login First, if you want to issue a credential
    2) Move to 'Issue Credential' menu
    3) Select credential-definition that you want: form_cashTransaction
    4) Enter information: creditor, debtor, amount, debt_term, approved_date
    5) Click 'Submit' then you can have your own credential with CapstoneCredential_no

## How it works 🙋

    0) 2 Docker Servers & Flask Server
        - Alice: client
        - Faber: issuer
        - Flask Server: Medium
    1) Alice is connected with Faber when a client enters 'Issue Credential' menu.
        The process of connection:
            Faber Sends Invitation
            Alice receive the Invitation
    3) Alice enters and submits detail information that is needed for the credential.
        The process of making credential:
            Flask Server saves information
            Flask Server requests of issuing credential to Faber
            Flask Server gets credential information: Credential id, Issue date, Issuing authority number, etc.
            Flask Server makes a PDF/PNG format of credential
    4) Alice downloads credential.

---

## Architecture
![DID인증이용한증명서발급 drawio](https://user-images.githubusercontent.com/62174395/236383720-dafb63d0-991d-444e-95b9-f4eb42391c39.svg)

