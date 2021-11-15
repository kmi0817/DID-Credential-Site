from app import app, db
from time import time
from flask import render_template, redirect, url_for, session, request, json, jsonify
import requests
import os
from ast import literal_eval # 보안 상의 이유로 eval 대신 더 안전한 literal_eval 사용
from app.models import User, Chatinfo, Chat

curr_path = os.getcwd() # 현재 working directory 경로 가져오기
path = os.path.join(curr_path, 'app', 'static') # 경로 병합해 새 경로 생성


@app.route('/')
def index():
    login = False
    if 'login' in session :
        login = True
    return render_template('index.html', login=login)

@app.route('/mypage')
def mypage() :
    login = False
    if 'login' in session :
        login = True
        id = session['login']

        member = User.query.filter(User.id == id).first()
        name = member.name
        return render_template('mypage.html', login=login, name=name, id=id)
    else :
        return render_template('mypage.html', login=login)

@app.route('/signin', methods=['GET', 'POST'])
def singin() :
    if request.method == 'GET':
        login = False
        if 'login' in session :
            login = True
        return render_template('signin.html', login=login)

    elif request.method == 'POST' :
        values = request.get_json(force=True)
        id = values['id']
        password = values['password']

        member = User.query.filter(User.id == id).first()
        if member and member.password == password :
            # User 테이블에 존재하면서 비밀번호와 이름이 일치함
            session['login'] = member.id
            return 'OK'
        else : # 그 외 (비회원이거나 비밀번호가 일치하지 않음)
            return 'FAIL'

@app.route('/signup', methods=['GET', 'POST'])
def singup() :
    if request.method == 'GET':
        login = False
        if 'login' in session :
            login = True
        return render_template('signup.html', login=login)

    elif request.method == 'POST' :
        values = request.get_json(force=True)
        name = values['name']
        id = values['id']
        password = values['password']

        print(f'name: {name}, id: {id}, password: {password}')
        record = User(name=name, id=id, password=password)
        db.session.add(record)
        db.session.commit()
        return 'OK'

@app.route('/signout', methods=['DELETE'])
def signout() :
    session.clear()

    if 'connection' in session :
        conn_id = session['connection']['conn_id']
        with requests.delete(f'http://0.0.0.0:8021/connections/{conn_id}') as del_res :
            print(del_res.json())
    return 'OK'

@app.route('/tutorials')
def tutorials() :
    login = False
    if 'login' in session :
        login = True

    return render_template('tutorial.html', login=login)

@app.route('/credential')
def credential() :
    login = False
    if 'login' in session :
        login = True

    conn = False
    cred_def_ids = None
    if 'connection' in session :
        conn = True
        with requests.get('http://0.0.0.0:8021/credential-definitions/created') as cred_def_res :
            cred_def_ids = cred_def_res.json()['credential_definition_ids']
            # print(cred_def_ids)
    
    return render_template('credential.html', login=login, connection=conn, credential_definition_ids=cred_def_ids)

@app.route('/credential-process', methods=['POST'])
def credential_process() :
    if 'login' in session :
        cred_attrs = request.get_json(force=True) # 대표자가 전송한 증명서 관련 데이터
        cred_def_id = cred_attrs['credential_definition_id'] # cred_def_id 가져오기
        del(cred_attrs['credential_definition_id']) # cred_attrs에서 cred_def_id 제거
        cred_attrs['timestamp'] = str(int(time())) # cred_attrs에 timestamp 추가
        conn_id = session['connection']['conn_id'] # connectino id 가져오기

        offer_request_body = {
            "connection_id": conn_id,
            "comment": f"Offer on cred def id {cred_def_id}",
            "auto_remove": "false",
            "credential_preview": {
                "@type": "https://didcomm.org/issue-credential/2.0/credential-preview",
                "attributes": [
                    {"name": n, "value": v}
                    for (n, v) in cred_attrs.items()
                ]
            },
            "filter": {"indy": {"cred_def_id": cred_def_id}},
            "trace": "false"
        }

        with requests.post('http://0.0.0.0:8021/issue-credential-2.0/send-offer', json=offer_request_body) as offer_res :
            result = offer_res.json()
            cred_ex_id = result['cred_ex_id']

            credential_file = os.path.join(path, 'credential_file', f'{cred_ex_id}.json') # 경로 병합해 새 경로 생성
            with open(credential_file, 'w') as f :
                f.write(str(result).replace("'", '"'))

        return cred_ex_id
    else :
        return 'FAIL'

@app.route('/credential/<cred_ex_id>')
def credential_cred_ex_id(cred_ex_id) :
    login = False
    if 'login' in session :
        login = True

    credential_file = os.path.join(path, 'credential_file', f'{cred_ex_id}.json') # 경로 병합해 새 경로 생성

    with open(credential_file, 'r') as f :
        credential_body = f.read() # 파일 내용 가져오기 (str)
        credential_body = literal_eval(credential_body) # str -> dict
        credential_body = json.dumps(credential_body, indent=4) # dict -> JSON 문자열
    return render_template('credential_issued.html', login=login, cred_ex_id=cred_ex_id, credential_body=credential_body)

@app.route('/chat')
def chatting() :
    login = False
    if 'login' in session :
        login = True

    return render_template('chat.html', login=login)




## 발급기관(faber)와 플라스크 서버(alice) 간 연결 ##
@app.route('/create-connection', methods=['POST'])
def create_connection() :
    if 'login' in session :
        with requests.post("http://0.0.0.0:8021/connections/create-invitation") as create_res :
            print("faber: create-invitation OK")
            invitation = create_res.json()['invitation'] # invitation 부분만 꺼내오기
            conn_id = create_res.json()['connection_id'] # connection id만 꺼내오기

            with requests.post("http://0.0.0.0:8031/connections/receive-invitation", json=invitation) as receive_res :
                my_did = receive_res.json()['my_did']

        ret = {
            "conn_id": conn_id,
            "my_did": my_did
        }
        session['connection'] = ret
        return ret
    else :
        return 'FAIL'

@app.route('/session-pop', methods=['POST'])
def session_pop() :
    session.clear()
    return 'session pop'

@app.route('/create-cred-def/<type>', methods=['POST'])
def created_cred_def(type) :
    # type : 등록할 증명서 양식 종류 1) 현금거래 (cash transaction), 2) 부동산거래? 3)...
    if type == 'cash-transaction' :
        schema_body = {
            "schema_name": "cash transaction schema",
            "schema_version": "32.21.70",
            "attributes": ["creditor", "debtor", "amount","debt_term",
            "CapstoneCredential_no","approved_date", "timestamp"]
        }
        with requests.post('http://0.0.0.0:8021/schemas', json=schema_body) as schema_res :
            schema_id = schema_res.json()['schema_id']

        credential_definition_body = {
            "schema_id": schema_id,
            "support_revocation": False,
            "revocation_registry_size": 100,
        }
        with requests.post('http://0.0.0.0:8021/credential-definitions', json=credential_definition_body) as creddef_res :
            creddef_id = creddef_res.json()['credential_definition_id']
        
    elif type == '부동산...' :
        print('제작 예정')

    return creddef_res.json()

@app.route('/credential-to-datatable', methods=['POST'])
def credential_to_datatable() :
    if 'login' in session :
        credential = request.get_json(force=True)
        created_at = credential['created_at']
        cred_ex_id = credential['cred_ex_id']

        cred_proposal = credential['cred_proposal']
        cred_proposal_id = cred_proposal['@id']
        cred_proposal_type = cred_proposal['@type']

        attributes = cred_proposal['credential_preview']['attributes']

        datatable_data = [
            {
                "id": 1,
                "key": "created_at",
                "value": created_at
            },
            {
                "id": 2,
                "key": "cred_ex_id",
                "value": cred_ex_id
            },
            {
                "id": 3,
                "key": "cred_proposal_id",
                "value": cred_proposal_id
            },
            {
                "id": 4,
                "key": "cred_proposal_type",
                "value": cred_proposal_type
            }
        ]

        id = 5
        for attr in  attributes :
            datatable_data.append({"id": id, "key": attr["name"], "value": attr["value"]})
            id = id + 1

        session['cred_ex_id'] = cred_ex_id
        datatable_file = os.path.join(path, 'datatable_file', f'{cred_ex_id}.json') # 경로 병합해 새 경로 생성
        with open(datatable_file, 'w') as f :
            f.write(str(datatable_data).replace("'", '"'))
        return 'OK'
    else :
        return 'FAIL'

@app.route('/credential-download')
def credential_download() :
    login = False
    if 'login' in session :
        login = True

    cred_ex_id = session['cred_ex_id']

    datatable_file = os.path.join(path, 'datatable_file', f'{cred_ex_id}.json') # 경로 병합해 새 경로 생성
    with open(datatable_file, 'r') as f :
        data = f.read()
    return render_template('credential_download.html', login=login, cred_ex_id=cred_ex_id, data=data)

@app.route('/datatable-data/<cred_ex_id>')
def datatable_data(cred_ex_id) :
    if 'login' in session :
        datatable_file = os.path.join(path, 'datatable_file', f'{cred_ex_id}.json') # 경로 병합해 새 경로 생성
        with open(datatable_file, 'r') as f :
            data = f.read()
        return data
    else :
        return 'FAIL'