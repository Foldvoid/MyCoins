import base64

def jiber(word: str):
    encoded_bytes = base64.b64encode(word.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def jaber(word: str):
    decoded_bytes = base64.b64decode(word.encode('utf-8'))
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string