from random import randint

def factor_script(k):
    fact_list = []
    found = False

    for x in range(2, k):
        if k % x == 0 and found == False:
            fact_list.append((int(k/x),x))
            found = True
            
        if found == True:
            break
    
    return fact_list

def find_de_as_k(phi_pq, prime1, prime2, factor_script_func):
    # Generate candidate list for k = d*e
    de_list = []

    # Set k as the maximum of prime1 or prime2
    k = max(prime1, prime2)

    # Loop through and increase k options by 1 every time, and check criteria for eligability
    found_de = False
    while found_de == False:

        # Factorises K into d*e and returns it if it exists, returns an empty list if it can't be factorised
        de = factor_script_func(k)

        # Check that k * modphi(N) = 1 and that k has factors
        if (k) % phi_pq == 1 and de != []:

            # Select the first candidate for K and end the loop
            de_list.append(de)
            found_de = True

        k += 1

    # Return k as a list make up of (d, e)
    return de_list

# Encoding dictionary
str_dict = {'a': "1", 'b': "2", 'c': "3", 'd': "4", 'e': "5", 'f': "6", 'g': "7", 'h': "8", 'i': "9", 
            'j': "10", 'k': "11", 'l': "12", 'm': "13", 'n': "14", 'o': "15", 'p': "16", 'q': "17", 
            'r': "18", 's': "19", 't': "20", 'u': "21", 'v': "22", 'w': "23", 'x': "24", 'y': "25", 
            'z': "26", ' ': "27"}


# Encodes the string (M) and encrypts it with Enc = M^e mod N, where M is the message as an integer
def encrypt_string(string_in, bank_code1,bank_code2):

    string_as_num = [(int(str_dict[item])**bank_code1)%bank_code2 for item in string_in]

    return string_as_num


# Decrypt a list of encrypted characters and return the message M, M = Enc^d mod N
def decrypt_string(encrypted_str, bank_secret, bank_code2):

    # Decrypts the message into the encoded list
    decrypted_list = [(item**bank_secret)%bank_code2 for item in encrypted_str]    
    
    # Matches the key with the letter and appends it into a string
    string_out = ""
    for char in decrypted_list:
        string_out += "".join([k for k,v in str_dict.items() if v == str(char)][0])


    return string_out

# Generate two prime numbers
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
    x = randint(1,len(mod_list)-1)
    y = randint(x,len(mod_list)-1)

    return mod_list[x], mod_list[y]

def main():
    # Banks secret keys - Two primes that make up N
    prime1, prime2 = gen_prime(3,200)
    print(f"Two secret primes that make up N = p*q = {prime1} * {prime2} = {prime1 * prime2} where N is a public key and p and q are bank secrets.\n")

    # Find phi(N) = phi(pq)
    phi_pq = (prime1-1) * (prime2-1)
    print(f"Phi(N) = (p - 1) * (q - 1)= {phi_pq}\n")

    # Find K
    # K = 1mod(fi(N))- K has to be able to be factored
    de = find_de_as_k(phi_pq, prime1, prime2,factor_script)[0]
    d, e = de[0]
    print(f"K = 1mod(Phi(N)) = d*e = {d} * {e}.\n")
    print(f"So, d = {d} and e = {e}. Then, 'd' becomes the banks secret key and 'e' is the other public key.\n")

    # Banks other secret key is d
    bank_secret = d

    # Bank public keys which are e and N
    bank_code1 = e
    bank_code2 = prime1 * prime2
    
    print(f"So, we have built the banks two public keys, which are {bank_code1} and {bank_code2}, these are used by senders to encrypt data.\n")
    print(f"As a result of this one way modular maths, it is essentially impossible to reverse the encryption without the private keys.\n")

    # Raw message
    message_raw = "this is a test"

    # Convert message into list and then encrypts each letter.
    encr_list = encrypt_string(message_raw, bank_code1, bank_code2)
    print(f"Encrypted message: {encr_list}\n")

    # Decrypt message
    print(f"Decrypted message: {decrypt_string(encr_list, bank_secret, bank_code2)}")

main()