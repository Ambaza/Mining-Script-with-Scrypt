import hashlib
import struct
import platform
import os


# Fonction pour installer les bibliothèques de hachage Scrypt nécessaires
def install_scrypt_libraries():
    system = platform.system()
    if system == "Windows":
        os.system("pip install scrypt_win")
    elif system == "Linux":
        os.system("pip install scrypt_linux")
    elif system == "Darwin":
        os.system("pip install scrypt_mac")
    else:
        print("System not supported")

# Fonction pour calculer le hash Sha256
def sha256(data):
    sha = hashlib.sha256()
    sha.update(data)
    return sha.digest()

# Fonction pour calculer le hash Scrypt
def scrypt(data):
    # Utiliser une bibliothèque de calcul de hachage Scrypt compatible avec le système d'exploitation
    if platform.system() == "Windows":
        import scrypt_win
        return scrypt_win.getPoWHash(data)
    elif platform.system() == "Linux":
        import scrypt_linux
        return scrypt_linux.getPoWHash(data)
    elif platform.system() == "Darwin":
        import scrypt_mac
        return scrypt_mac.getPoWHash(data)
    else:
        print("System not supported")


# Fonction pour trouver un bloc valide
def mine_block(block_header, target):
    nonce = 0
    iterations = 0
    while True:
        header = block_header + struct.pack("<I", nonce)
        hash = sha256(scrypt(header))
        if int.from_bytes(hash, byteorder='big', signed=False) < int(target, 16):
            return (hash, nonce)
        nonce += 1
        iterations += 1
        if iterations > 10000000: # limite raisonnable pour le nombre d'itérations
            print("Aucun hash valide trouvé après 10 millions d'itérations")
            return None

# Exemple d'utilisation
install_scrypt_libraries()
block_header = "bloc de données à inclure dans le header"
target = "cible de difficulté (en hexadécimal)"

result = mine_block(block_header, target)
if result:
    print("Hash valide:", result[0].encode('hex'))
    print("Nonce utilisé:", result[1])
