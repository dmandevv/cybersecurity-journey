CIPHERTEXT = ''

with open("VigCipher/messages.txt", "r") as f:
    CIPHERTEXT = f.readline().strip().replace(" ", "")
    
def decrypt_vigenere(key_length):
    shifts = []
    for group in get_groups(key_length).values():
        counts = {}
        for letter in group:
            counts.setdefault(letter, 0)
            counts[letter] += 1
        sorted_letters = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        shifts.append(ord(sorted_letters[0][0]) - ord('E'))
    
    decrypted = ''
    for i, c in enumerate(CIPHERTEXT):
        shift = shifts[i % key_length]
        decrypted += chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
    return decrypted


def get_groups(keylength):
    groups = {}
    for index, letter in enumerate(CIPHERTEXT):
        group = index % keylength
        groups.setdefault(group, [])
        groups[group].append(letter)
    return groups

def get_ioc(group) -> float: 
    counts = {}
    for letter in group:
        counts.setdefault(letter, 0)
        counts[letter] += 1
    total = 0
    for count in counts.values():
        total += count * (count - 1)
    N = len(group)
    return total / (N * (N - 1))

for key_length in range(2, 6):
    with open(f"VigCipher/analysis/freq_analysis_group_{key_length}.txt", "w") as f:
        f.write(decrypt_vigenere(key_length))
