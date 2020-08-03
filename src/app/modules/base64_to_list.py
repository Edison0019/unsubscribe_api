import base64

def base_converter(objects):
    try:
        decoded_values = {x:base64.b64decode(objects[x]).decode('ascii') for x in objects}
        return decoded_values
    except:
        return None