def custom_format(text):
    input_string = text
    number_map = {'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'}
    for persian, english in number_map.items():
        input_string = input_string.replace(persian, english)
    else:
        output_string = f" {input_string}"
    return output_string

def full_plate(plate):
    try:
        city = custom_format(plate[6:])
        left_code = custom_format(plate[:2])
        char = plate[2]
        right_code = custom_format(plate[3:6])
        full_plate = f"{left_code}{right_code}{char}{city}".replace(" ", "")
        return full_plate
    except Exception as e:
        print(f"Error in full_plate function: {e}")
        return ""

def code_plate(plate):
    try:
        city = custom_format(plate[6:])
        left_code = custom_format(plate[:2])
        char = plate[2]
        right_code = custom_format(plate[3:6])
        code_plate = f"{left_code}{right_code}".replace(" ", "")
        return code_plate
    except Exception as e:
        print(f"Error in code_plate function: {e}")
        return ""