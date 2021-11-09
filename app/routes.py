from app import app
from time import time
from flask import render_template, redirect, url_for, session, request, json, jsonify
import requests


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mypage')
def mypage() :
    return render_template('mypage.html')
@app.route('/signin')
def singin() :
    return render_template('signin.html')

@app.route('/signup')
def singup() :
    return render_template('signup.html')

@app.route('/tutorials')
def tutorials() :
    return render_template('tutorial.html')

@app.route('/credential')
def credential() :
    return render_template('credential.html')

@app.route('/credential-process', methods=['POST'])
def credential_process() :
    cred_attrs = request.get_json(force=True) # 대표자가 전송한 증명서 관련 데이터
    cred_def_id = cred_attrs['credential_definition_id']
    cred_attrs['timestamp'] = str(int(time()))
    del(cred_attrs['credential_definition_id'])

    ## 발급기관(faber)와 플라스크 서버(alice) 간 연결 ##
    with requests.post("http://0.0.0.0:8021/connections/create-invitation") as create_res :
        invitation = create_res.json()['invitation'] # invitation 부분만 꺼내오기
        conn_id = create_res.json()['connection_id'] # connection id만 꺼내오기

        with requests.post("http://0.0.0.0:8031/connections/receive-invitation", json=invitation) as receive_res :
            # cred_preview = {
            #     "@type": "https://didcomm.org/issue-credential/2.0/credential-preview",
            #     "attributes": [
            #         {"name": n, "value": v}
            #         for (n, v) in cred_attrs.items()
            #     ]
            # }

            offer_request = {
                "connection_id": conn_id,
                "comment": f"Offer on cred def id {cred_def_id}",
                "auto_remove": False,
                "credential_preview": {
                    "@type": "https://didcomm.org/issue-credential/2.0/credential-preview",
                    "attributes": [
                        {"name": n, "value": v}
                        for (n, v) in cred_attrs.items()
                    ]
                },
                "filter": {"indy": {"cred_def_id": cred_def_id}},
                "trace": False
            }

            with requests.post('http://0.0.0.0:8021/issue-credential-2.0/send-offer', json=offer_request) as offer_res :
                print(offer_res)

    return 'gu'

@app.route('/credential-issued')
def credential_issued() :
    return render_template('credential_issued.html')

@app.route('/chat')
def chatting() :
    return render_template('chat.html')



# # schema 등록
# @app.route('/register/cash-transaction', methods=['POST'])
# def register_cash_transaction() :
#     schema_body = {
#         "schema_name": "cash transaction schema",
#         "schema_version": "01",
#         "attributes": ["creditor","debtor", "amount",
#         "debt_term", "CapstoneCredential_no","approved_date", "timestamp"],
#     }

#     with requests.post('http://0.0.0.0:8021/schemas', json=schema_body) as schema_res :
#         schema_id = schema_res.json()['schema_id']
#         print("schema_id: " + schema_id)
#         credential_definition_body = {
#             "schema_id": schema_id,
#             "support_revocation": False,
#             "revocation_registry_size": 100,
#         }

#         with requests.post('http://0.0.0.0:8021/credential-definitions', json=credential_definition_body) as creddef_res :
#             credential_definition_id = creddef_res.json()['credential_definition_id']
#             print("credential_definition_id: " + credential_definition_id)

#     return "cash tranaction format registered"

# @app.route("/register/schema", methods=['POST'])
# def schema() :
#     schema_body = {
#         "schema_name": "cash transaction schema",
#         "schema_version": "01",
#         "attributes": ["creditor","debtor", "amount",
#         "debt_term", "CapstoneCredential_no","approved_date", "timestamp"],
#     }

#     with requests.post('http://0.0.0.0:8021/schemas', json=schema_body) as schema_res :
#         schema_id = schema_res.json()['schema_id']
#         print("schema_id: " + schema_id)
#     return 'schema registered'

