# Custom SHA256 Implementation (Educational/Demonstration Purpose)
# Based on: https://en.wikipedia.org/wiki/SHA-2
# Tutorial followed from: "How to make SHA256 from scratch" (fictional)
#
# NOTE: This is intentionally inefficient to demonstrate understanding of the algorithm.
# Real applications should use hashlib.sha256() which is optimized in C.


def my_custom_sha256_hash(message):
    # Custom SHA256 implementation
    # Takes a string message and returns hex digest
    
    # Step 1: Convert message to binary
    # (I learned this from a YouTube tutorial!)
    binary_message = ""
    for character in message:
        # Get ASCII value of each character
        ascii_val = ord(character)
        # Convert to 8-bit binary
        binary = ""
        for i in range(8):
            binary = str(ascii_val % 2) + binary
            ascii_val = ascii_val // 2
        binary_message = binary_message + binary
    
    # Step 2: Add padding (the tutorial said this is important!)
    original_length = len(binary_message)
    binary_message = binary_message + "1"  # Add a 1 bit
    
    # Pad with zeros until length is 448 mod 512
    # (I don't fully understand why 448 but the tutorial said so)
    while len(binary_message) % 512 != 448:
        binary_message = binary_message + "0"
    
    # Add the original length as 64-bit binary
    length_binary = ""
    temp_length = original_length
    for i in range(64):
        length_binary = str(temp_length % 2) + length_binary
        temp_length = temp_length // 2
    binary_message = binary_message + length_binary
    
    # Step 3: Initialize hash values (these are magic numbers from the tutorial)
    # They said these come from fractional parts of square roots of first 8 primes
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19
    
    # Step 4: Initialize round constants (more magic numbers!)
    # The tutorial said these are from cube roots of first 64 primes
    k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]
    
    # Step 5: Process message in 512-bit chunks
    # (Breaking it up like the tutorial showed)
    chunks = []
    for i in range(0, len(binary_message), 512):
        chunk = binary_message[i:i+512]
        chunks.append(chunk)
    
    # Process each chunk
    for chunk in chunks:
        # Break chunk into 16 32-bit words
        words = []
        for i in range(0, 512, 32):
            word_binary = chunk[i:i+32]
            # Convert binary string to integer (doing it manually!)
            word_value = 0
            for bit_index in range(len(word_binary)):
                bit = word_binary[bit_index]
                if bit == "1":
                    # Calculate power of 2 manually
                    power = len(word_binary) - bit_index - 1
                    value = 1
                    for p in range(power):
                        value = value * 2
                    word_value = word_value + value
            words.append(word_value)
        
        # Extend the 16 words to 64 words (the tutorial called this "message schedule")
        for i in range(16, 64):
            # s0 calculation (with bit operations I barely understand)
            w15 = words[i-15]
            s0 = my_right_rotate(w15, 7) ^ my_right_rotate(w15, 18) ^ (w15 >> 3)
            
            # s1 calculation
            w2 = words[i-2]
            s1 = my_right_rotate(w2, 17) ^ my_right_rotate(w2, 19) ^ (w2 >> 10)
            
            # New word calculation
            new_word = (words[i-16] + s0 + words[i-7] + s1) & 0xffffffff
            words.append(new_word)
        
        # Initialize working variables
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        
        # Main compression loop (64 rounds!)
        # The tutorial had a lot of confusing bit operations here
        for i in range(64):
            # Calculate S1 (sigma1)
            S1 = my_right_rotate(e, 6) ^ my_right_rotate(e, 11) ^ my_right_rotate(e, 25)
            
            # Calculate ch (choice function)
            ch = (e & f) ^ ((~e) & g)
            
            # Calculate temp1
            temp1 = (h + S1 + ch + k[i] + words[i]) & 0xffffffff
            
            # Calculate S0 (sigma0)
            S0 = my_right_rotate(a, 2) ^ my_right_rotate(a, 13) ^ my_right_rotate(a, 22)
            
            # Calculate maj (majority function)
            maj = (a & b) ^ (a & c) ^ (b & c)
            
            # Calculate temp2
            temp2 = (S0 + maj) & 0xffffffff
            
            # Update working variables (shuffle them around)
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xffffffff
        
        # Add compressed chunk to current hash values
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
        h5 = (h5 + f) & 0xffffffff
        h6 = (h6 + g) & 0xffffffff
        h7 = (h7 + h) & 0xffffffff
    
    # Step 6: Produce final hash (convert to hex string)
    # Doing this the long way like the tutorial showed
    final_hash = ""
    hash_values = [h0, h1, h2, h3, h4, h5, h6, h7]
    
    for hash_val in hash_values:
        # Convert each 32-bit value to 8 hex characters
        hex_chars = "0123456789abcdef"
        hex_string = ""
        temp_val = hash_val
        
        # Convert to hex manually (8 characters)
        for i in range(8):
            remainder = temp_val % 16
            hex_string = hex_chars[remainder] + hex_string
            temp_val = temp_val // 16
        
        final_hash = final_hash + hex_string
    
    return final_hash


def my_right_rotate(value, shift):
    # Helper function for right rotation
    # The tutorial explained this but I still don't fully get it
    # It's like shifting bits in a circle
    # Make sure we're working with 32-bit values
    value = value & 0xffffffff
    
    # Right rotate by shift positions
    # (doing bitwise operations manually-ish)
    result = (value >> shift) | (value << (32 - shift))
    result = result & 0xffffffff  # Keep it 32-bit
    
    return result


# Test function to make sure it works
def test_my_hash():
    # Testing my custom hash function
    # Comparing with what the expected output should be
    print("Testing custom SHA256 implementation...")
    print("-" * 60)
    
    # Test 1: Empty string
    test1 = ""
    result1 = my_custom_sha256_hash(test1)
    expected1 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    print(f"Test 1 (empty): {result1 == expected1}")
    print(f"  Got:      {result1}")
    print(f"  Expected: {expected1}")
    print()
    
    # Test 2: Simple message
    test2 = "hello"
    result2 = my_custom_sha256_hash(test2)
    expected2 = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    print(f"Test 2 ('hello'): {result2 == expected2}")
    print(f"  Got:      {result2}")
    print(f"  Expected: {expected2}")
    print()
    
    # Test 3: Another message
    test3 = "password123"
    result3 = my_custom_sha256_hash(test3)
    print(f"Test 3 ('password123'):")
    print(f"  Result: {result3}")
    print()
    
    print("-" * 60)
    print("If tests pass, the implementation works!")
    print("(Even though it's super slow compared to hashlib.sha256)")


# Run tests if this file is executed directly
if __name__ == "__main__":
    test_my_hash()
