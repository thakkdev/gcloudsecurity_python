import base64
from decrypt_symmetric import decrypt_symmetric

def decodeto_base64_message(response_ciphertext):
    
    #  decodeto_base64_message() 
    #  encode bytes using base64 and convert to string
    
    base64_bytes = base64.b64encode(response_ciphertext)
    base64_message = base64_bytes.decode('ascii') 
    return base64_message


def encodeto_base64_bytes(base64_message):
    
    #  encodeto_base64_bytes()
    #  convert to bytes and base64 decode
    
    base64_bytes = base64_message.encode('ascii')
    ciphertext_bytes = base64.b64decode(base64_bytes)
    return ciphertext_bytes

def passphraseplaintext(dictionary_doc, passphrasetext):
     if passphrasetext:
        passphrase_bytes = encodeto_base64_bytes(passphrasetext)
        descryptext = decrypt_symmetric('kmstestproj', 'us-east1', 
                                        'kmstestprojkeyring', 'kmstestkeyname',passphrase_bytes)
        dictionary_doc['passphrase'] = str(descryptext.plaintext, 'utf-8')