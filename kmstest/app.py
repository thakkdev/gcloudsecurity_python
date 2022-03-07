# app.py

# Required imports
import os
import base64
from flask import Flask, request, jsonify
from google.cloud import firestore
from encrypt_symmetric import encrypt_symmetric
from helper import decodeto_base64_message, passphraseplaintext


# Initialize Flask app
app = Flask(__name__)


db = firestore.Client()
profile_db = db.collection('profile')

@app.route('/list', methods=['GET'])
def list():
    
    #    list() : Fetches documents from Firestore collection as JSON.
    #    profile : Return document that matches query ID.
    #    all_profiles : Return all documents.
    
    try:
        profile_id = request.args.get('id')
        if profile_id:
            profile = []
            dictionary_doc = profile_db.document(profile_id).get()
            #convert encrypted passphrase to plaintext
            passphraseplaintext( dictionary_doc, dictionary_doc.get('passphrase'))
            profile.append(dictionary_doc)
            return jsonify(profile.to_dict()), 200
        else:
            all_profiles = []
            for doc in profile_db.stream():
                dictionary_doc = doc.to_dict()
                passphraseplaintext( dictionary_doc, dictionary_doc.get('passphrase'))
               
                all_profiles.append(dictionary_doc)
            return jsonify(all_profiles), 200
    except Exception as e:
        return f"Error: {e}"

 

@app.route('/add', methods=['POST'])
def add():
    
    #    add() : Add document to Firestore collection with request body.
    #    e.g. json={"id": "1", "passphrase": "Alpha Jumbo Query Boat"}

    try:
        id = request.json['id']
        passphrase = request.json['passphrase']
        encryptedresp = encrypt_symmetric('kmstestproj', 'us-east1', 'kmstestprojkeyring', 
                                     'kmstestkeyname',str(passphrase) )
        #convert encryptedresp.ciphertext from bytes to string
        encryptedtext = decodeto_base64_message(encryptedresp.ciphertext)
        profile_db.document(id).set({'id':id, 'passphrase': encryptedtext})
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"Error : {e}"


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')