from flask import Flask, jsonify, request
from num2words import num2words

app = Flask(__name__)
output = ["machine_on","grinding_beans","empty_grounds_fault","water_empty_fault","number_of_cups_today","descale_required","have_another_one_carl"]
scale = 16 ## equals to hexadecimal
num_of_bits = 16

def binary_to_decimal(binary_str):
    decimal_num = int(binary_str, 2)
    print(decimal_num)
    return decimal_num

def validate_hex_string(hex_string):
    try:
        value = int(hex_string, 16)
    except ValueError:
        return False

    # Check if the value fits in 2 bytes (unsigned representation)
    if 0 <= value <= 0xFFFF:
        return True
    else:
        return False

@app.route('/numberToWords', methods=['POST'])
def processData():
    # Extract the input
    # Take input as a 32-bit binary string
    binary_input = request.form['user_input']
    print(binary_input)
    
    # Check if the input is 32 bits
    if len(binary_input) == 32 and all(bit in '01' for bit in binary_input):
        # slice out 1st bit to check positive or negative : if 1(Negative) else 0 (Positive)
        first = binary_input[:1]
        second = binary_input[1:32]

        # Convert binary to decimal
        decimal_number = binary_to_decimal(second)

        # Print number to word
        if (first == '1'):
            print(f"Decimal Number: -{decimal_number}")
            print("Negative " + str(num2words(decimal_number)))
            return jsonify({'Output': "Negative " + str(num2words(decimal_number))}), 200
        else:
            print(f"Decimal Number: {decimal_number}")
            print(num2words(decimal_number))
            return jsonify({'Output': num2words(decimal_number)}), 200
    else:
        print("Invalid input. Please enter a valid 32-bit binary string.")
        return jsonify({'Output': "NA", 'Error': "Invalid input. Please enter a valid 32-bit binary string."}), 400

@app.route('/checkHexadecimal', methods=['POST'])
def checkHexadecimal():
    # Extract the input
    # Take input as a Hexadecimal string
    hexadecimal_input = request.form['user_input']
    print(hexadecimal_input)    
    
    if validate_hex_string(hexadecimal_input):
        # Convert Hexadecimal string into 16bit
        bits_16 = bin(int(hexadecimal_input, scale))[2:].zfill(num_of_bits)
        print("bits 16: ",bits_16)

        # Logic Conditions
        output[0]="machine_on:"+str(bool(bits_16[:1] == '0'))
        output[1]="grinding_beans:"+str(bool(bits_16[1:2] == '0'))
        output[2]="empty_grounds_fault:"+str(bool(bits_16[2:3] == '0'))
        output[3]="water_empty_fault:"+str(bool(bits_16[3:4] == '0'))
        output[4]="number_of_cups_today:"+str(int(bits_16[4:12], 2))
        output[5]="descale_required:"+str(bool(bits_16[14:15] == '0'))
        output[6]="have_another_one_carl:"+str( bool(bits_16[13:14] or bits_16[15:16]))
        print(output)
        return jsonify({'Output': output}), 200
    else:
        return jsonify({'error': 'Invalid Hexadecimal string'}), 400
    

if __name__ == '__main__':
    app.run()