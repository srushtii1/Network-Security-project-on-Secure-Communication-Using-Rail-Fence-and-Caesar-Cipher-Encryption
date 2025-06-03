from flask import Flask, render_template, request

app = Flask(__name__)

def encryptRailFence(text, key):
    rail = [['\n' for i in range(len(text))] for j in range(key)]
    dir_down = False
    row, col = 0, 0

    for i in range(len(text)):
        if (row == 0) or (row == key - 1):
            dir_down = not dir_down
        rail[row][col] = text[i]
        col += 1
        if dir_down:
            row += 1
        else:
            row -= 1

    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return "".join(result)


def decryptRailFence(cipher, key):
    rail = [['\n' for i in range(len(cipher))] for j in range(key)]
    dir_down = None
    row, col = 0, 0

    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        rail[row][col] = '*'
        col += 1
        if dir_down:
            row += 1
        else:
            row -= 1

    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1

    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        if rail[row][col] != '*':
            result.append(rail[row][col])
            col += 1
        if dir_down:
            row += 1
        else:
            row -= 1
    return "".join(result)


def encrypt(text, s):
    result = ""

    # traverse text
    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters
        if char.isupper():
            result += chr((ord(char) + s - 65) % 26 + 65)

        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)

    return result
    # Your encryption code here

def decrypt(text, s):
    result = ""

    # traverse text
    for i in range(len(text)):
        char = text[i]

        # Decrypt uppercase characters
        if char.isupper():
            result += chr((ord(char) - s - 65) % 26 + 65)

        # Decrypt lowercase characters
        else:
            result += chr((ord(char) - s - 97) % 26 + 97)

    return result


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    plaintext = request.form['plaintext']
    rail_fence_key = int(request.form['rail_fence_key'])
    caesar_shift = int(request.form['caesar_shift'])

    # Encrypt using Rail Fence
    rail_fence_cipher = encryptRailFence(plaintext, rail_fence_key)

    # Encrypt using Caesar Cipher
    combined_cipher = encrypt(rail_fence_cipher, caesar_shift)

    # Decrypt using Caesar Cipher
    decrypted_caesar = decrypt(combined_cipher, caesar_shift)

    # Decrypt using Rail Fence
    decrypted_text = decryptRailFence(decrypted_caesar, rail_fence_key)

    return render_template('result.html', encrypted_text=combined_cipher, decrypted_text=decrypted_text)

if __name__ == '__main__':
    app.run(debug=True)
