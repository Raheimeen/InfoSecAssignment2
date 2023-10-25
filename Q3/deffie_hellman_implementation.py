def generate_public_key(a, p, g):
    
    r = (g**a)%p

    return r

def decode_public_key(r_other, a, p):
    
    key = (r_other**a)%p
    
    return key

import math

# Encoding dictionary
str_dict = {'a': "101", 'b': "102", 'c': "103", 'd': "104", 'e': "105", 'f': "106", 'g': "107", 'h': "108", 
            'i': "109", 'j': "110", 'k': "111", 'l': "112", 'm': "113", 'n': "114", 'o': "115", 'p': "116", 
            'q': "117", 'r': "118", 's': "119", 't': "120", 'u': "121", 'v': "122", 'w': "123", 'x': "124", 
            'y': "125", 'z': "126", " ": "127", 'A': "201", 'B': "202", 'C': "203", 'D': "204", 'E': "205", 
            'F': "206", 'G': "207", 'H': "208", 'I': "209", 'J': "210", 'K': "211", 'L': "212", 'M': "213", 
            'N': "214", 'O': "215", 'P': "216", 'Q': "217", 'R': "218", 'S': "219", 'T': "220", 'U': "221", 
            'V': "222", 'W': "223", 'X': "224", 'Y': "225", 'Z': "226", ",": "301", ".": "302"}


# Encrypt a string
def encrypt_string(string_in, secret_key):

    string_as_num = "".join((str_dict[string_in[n]] for n in range(0,len(string_in))))

    return int(string_as_num) * secret_key


# Decrypt a string
def decrypt_string(encrypted_str, secret_key):
    string_as_num = str(int(encrypted_str // secret_key))
    start_index = 0
    end_index = 3
    string_out = ""

    for _ in range(0, len(string_as_num) // 3):
        string_out += "".join([k for k,v in str_dict.items() if v == string_as_num[start_index:end_index]])
        start_index += 3
        end_index += 3

    return string_out

from random import randint

# Generate a prime number
def gen_prime(start, stop):
    mod_list = []

    # Generate list of prime numbers
    for num in range(start, stop):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                mod_list.append(num)

    # Randomly pick a number to pick a number from the list
    x = randint(1,len(mod_list))

    return mod_list[x]

def main():
    # Generate modulo and base
    p = gen_prime(2000,6000) # Modulus
    g = gen_prime(500, 1000) # Base
    print(f"The modulo is {p} and base is {g} and made public to all users.\n")


    # User 1 - Set user 1's secret key and generate the public key based of it
    a1 = gen_prime(1000, 3000) # Secret key
    r1 = generate_public_key(a1, p, g) # Public key


    # User 2 - Set user 2's secret key and generate the public key based of it
    a2 = gen_prime(1000, 3000) # Secret key
    r2 = generate_public_key(a2, p, g) # Public key

    print("User 1 and User 2 determine their own secret key and use it to generate their public key, which they distribute to eachother.\n")
    print("Using eachothers public key, the modulo and their own private key, each user generates the encryption key. These end up being the same as per the maths.\n")
    
    
    # User 1 and USer 2 - Makes encryption key from the modulus, public key and own private key
    key1 = decode_public_key(r2, a1, p)
    key2 = decode_public_key(r1, a2, p)


    # This should hold true for trust to be established
    if key1 == key2:

        # User 1 - Encrypt and send message to user 2
        data1_in = input("Enter text to send to user 2: ") # Secret message
        data_encrypted1 = encrypt_string(data1_in, key1) # Encrypts message using key
        data1 = {"modulo": p, "public key of sender": r1, "data": data_encrypted1} # Sets up data packet to send
        print(f"Sending user 2 the encrypted data of user 1:\n{data1}\n")

        # User 2 - Recieves the message from user 1 and decrypts it
        data_in = data1
        p_in = data_in["modulo"]
        r_in = data_in["public key of sender"]
        data_rec2 = data_in["data"]
        print(f"Decrypting User 1's message:\n{decrypt_string(data_rec2, decode_public_key(r_in, a2, p_in))}\n")

    else:
        print("Incorrect keys.")

main()