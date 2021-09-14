from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook
from cardcontent import *
import smartsheet

app = Flask(__name__)
api = WebexTeamsAPI(access_token="MzA1ZDk3MzQtZTE4Ni00MDE3LWJiYzYtMjBiZmY4MDM1Yjc4MzMxNWZmZDAtNDcz_PF84_a4641176-1d5e-4cc4-a7c3-f37bb89b0635")

@app.route('/', methods=['Post', 'Get'])
def home():
    return 'OK', 200

@app.route('/webhookreq', methods=['POST', 'GET'])
def webhookreq():
    if request.method == 'POST':
        req = request.get_json()

        data_personID = req['data'] ['personId']
        data_roomID = req['data']['roomId']

        #Loop prevention VERY Important!
        me = api.people.me()
        if data_personID == me.id:
            return 'OK', 200
        else:
            if api.messages.create(roomId=data_roomID, text='Hello World!', attachments = [{"contentType":"application/vnd.microsoft.card.adaptive", "content":cardcontent}]):
                return "OK"

    elif request.method == 'GET':
        return "Yes, this is working!"
    return 'OK', 200

@app.route('/cardsubmitted', methods=['POST'])
def cardsubmitted():
    if request.method =="POST":
        req = request.get_json()

        data_id = req['data']['id']
        attachment_actions = api.attachment_actions.get(data_id)
        inputs = attachment_actions.inputs

        myName = inputs['myName']
        myEmail = inputs['myEmail']
        myTel = inputs['myTel']

        print(myName)
        print(myEmail)
        print(myTel)

        smart = smartsheet.Smartsheet('WC8pMERTs6Y9QgvCxRsGB83UbKzg0wC15THfy') #Smartsheet Access Token
        smart.errors_as_exceptions(True)

        #Specify cell values for the added row
        newRow = smartsheet.models.Row()
        newRow.to_top = True

        #The above variables are the incoming JSON

        newRow.cells.append({ 'column_id': 6831011559434116, 'value': myName })

        newRow.cells.append({ 'column_id': 1201512025220996, 'value': myEmail, 'strict': False})

        newRow.cells.append({ 'column_id': 5705111652591492, 'value': myTel, 'strict': False})

        response = smart.Sheets.add_rows(6751367692871556, newRow) # The --xxxxxxxxxxxxxx -- on this line is the sheet ID.


        return 'OK', 200
     
if __name__=='__main__':
     app.debug = True
     app.run(host="0.0.0.0")