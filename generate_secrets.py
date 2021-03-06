from cryptography.fernet import Fernet
import base64
import os

# Check for previous generated Keys and secrets
if os.path.isfile(os.path.expanduser('~/neo4j_db_user.secret')):
    os.chmod(os.path.expanduser('~/neo4j_db_user.secret'), 0o640)

if os.path.isfile(os.path.expanduser('~/neo4j_db_password.secret')):
    os.chmod(os.path.expanduser('~/neo4j_db_password.secret'), 0o640)

if os.path.isfile(os.path.expanduser('~/default_app_user_name.secret')):
    os.chmod(os.path.expanduser('~/default_app_user_name.secret'), 0o640)

if os.path.isfile(os.path.expanduser('~/default_app_user_password.secret')):
    os.chmod(os.path.expanduser('~/default_app_user_password.secret'), 0o640)

if os.path.isfile(os.path.expanduser('~/default_app_admin_name.secret')):
    os.chmod(os.path.expanduser('~/default_app_admin_name.secret'), 0o640)

if os.path.isfile(os.path.expanduser('~/default_app_admin_password.secret')):
    os.chmod(os.path.expanduser('~/default_app_admin_password.secret'), 0o640)

if os.path.isfile(os.path.expanduser('~/jwt_secret_key.secret')):
    os.chmod(os.path.expanduser('~/jwt_secret_key.secret'), 0o640)

if os.path.isfile(os.path.expanduser('~/encryption_key.secret')):
    os.chmod(os.path.expanduser('~/encryption_key.secret'), 0o640)


# Generate a Key and save it
key = Fernet.generate_key()
f = open(os.path.expanduser('~/encryption_key.secret'), 'wb')
f.write(key)
f.close()
os.chmod(os.path.expanduser('~/encryption_key.secret'), 0o440)

# Binary Files
file_neo4j_db_user = open(os.path.expanduser('~/neo4j_db_user.secret'), 'wb')
file_neo4j_db_password = open(os.path.expanduser('~/neo4j_db_password.secret'), 'wb')
file_default_app_user_name = open(os.path.expanduser('~/default_app_user_name.secret'), 'wb')
file_default_app_user_password = open(os.path.expanduser('~/default_app_user_password.secret'), 'wb')
file_default_app_admin_name = open(os.path.expanduser('~/default_app_admin_name.secret'), 'wb')
file_default_app_admin_password = open(os.path.expanduser('~/default_app_admin_password.secret'), 'wb')
file_jwt_secret_key = open(os.path.expanduser('~/jwt_secret_key.secret'), 'wb')

# Get your secrets input
# TODO: Customize the neo4j container to be able to have a user name different from neo4j
neo4j_db_user = 'neo4j'
neo4j_db_password = input("Please enter the neo4j_db_password: ")
default_app_user_name = input("Please enter the default_app_user_name: ")
default_app_user_password = input("Please enter the default_app_user_password: ")
default_app_admin_name = input("Please enter the default_app_admin_name: ")
default_app_admin_password = input("Please enter the default_app_admin_password: ")
jwt_secret_key = input("Please enter the jwt_secret_key: ")

# Base64 encode the secrets, requires the string to be converted to bytes
encoded_neo4j_db_user = base64.b64encode(bytes(neo4j_db_user, 'utf-8'))
encoded_neo4j_db_password = base64.b64encode(bytes(neo4j_db_password, 'utf-8'))
encoded_default_app_user_name = base64.b64encode(bytes(default_app_user_name, 'utf-8'))
encoded_default_app_user_password = base64.b64encode(bytes(default_app_user_password, 'utf-8'))
encoded_default_app_admin_name = base64.b64encode(bytes(default_app_admin_name, 'utf-8'))
encoded_default_app_admin_password = base64.b64encode(bytes(default_app_admin_password, 'utf-8'))
encoded_jwt_secret_key = base64.b64encode(bytes(jwt_secret_key, 'utf-8'))

# Encrypt the encoded secrets with the key
f = open(os.path.expanduser('~/encryption_key.secret'), 'rb')
key0 = f.read()
f.close()

if key == key0:
    print("Encrypting your secrets...")
else:
    print("You failed as programmer")

fer = Fernet(key)
encrypted_neo4j_db_user = fer.encrypt(encoded_neo4j_db_user)
encrypted_neo4j_db_password = fer.encrypt(encoded_neo4j_db_password)
encrypted_default_app_user_name = fer.encrypt(encoded_default_app_user_name)
encrypted_default_app_user_password = fer.encrypt(encoded_default_app_user_password)
encrypted_default_app_admin_name = fer.encrypt(encoded_default_app_admin_name)
encrypted_default_app_admin_password = fer.encrypt(encoded_default_app_admin_password)
encrypted_jwt_secret_key = fer.encrypt(encoded_jwt_secret_key)

# Write the encrypted secrets
file_neo4j_db_user.write(encrypted_neo4j_db_user)
file_neo4j_db_password.write(encrypted_neo4j_db_password)
file_default_app_user_name.write(encrypted_default_app_user_name)
file_default_app_user_password.write(encrypted_default_app_user_password)
file_default_app_admin_name.write(encrypted_default_app_admin_name)
file_default_app_admin_password.write(encrypted_default_app_admin_password)
file_jwt_secret_key.write(encrypted_jwt_secret_key)

file_neo4j_db_user.close()
file_neo4j_db_password.close()
file_default_app_user_name.close()
file_default_app_user_password.close()
file_default_app_admin_name.close()
file_default_app_admin_password.close()
file_jwt_secret_key.close()


# Decryption test from files
# Secret files
file_neo4j_db_user = open(os.path.expanduser('~/neo4j_db_user.secret'), 'rb')
file_neo4j_db_password = open(os.path.expanduser('~/neo4j_db_password.secret'), 'rb')
file_default_app_user_name = open(os.path.expanduser('~/default_app_user_name.secret'), 'rb')
file_default_app_user_password = open(os.path.expanduser('~/default_app_user_password.secret'), 'rb')
file_default_app_admin_name = open(os.path.expanduser('~/default_app_admin_name.secret'), 'rb')
file_default_app_admin_password = open(os.path.expanduser('~/default_app_admin_password.secret'), 'rb')
file_jwt_secret_key = open(os.path.expanduser('~/jwt_secret_key.secret'), 'rb')

# Decrypt
decrypted_neo4j_db_user = fer.decrypt(file_neo4j_db_user.read())
decrypted_neo4j_db_password = fer.decrypt(file_neo4j_db_password.read())
decrypted_default_app_user_name = fer.decrypt(file_default_app_user_name.read())
decrypted_default_app_user_password = fer.decrypt(file_default_app_user_password.read())
decrypted_default_app_admin_name = fer.decrypt(file_default_app_admin_name.read())
decrypted_default_app_admin_password = fer.decrypt(file_default_app_admin_password.read())
decrypted_jwt_secret_key = fer.decrypt(file_jwt_secret_key.read())

# Base64 Decode
decoded_neo4j_db_user = base64.b64decode(decrypted_neo4j_db_user)
decoded_neo4j_db_password = base64.b64decode(decrypted_neo4j_db_password)
decoded_default_app_user_name = base64.b64decode(decrypted_default_app_user_name)
decoded_default_app_user_password = base64.b64decode(decrypted_default_app_user_password)
decoded_default_app_admin_name = base64.b64decode(decrypted_default_app_admin_name)
decoded_default_app_admin_password = base64.b64decode(decrypted_default_app_admin_password)
decoded_jwt_secret_key = base64.b64decode(decrypted_jwt_secret_key)

# UTF-8 Decode
decoded_neo4j_db_user = decoded_neo4j_db_user.decode()
decoded_neo4j_db_password = decoded_neo4j_db_password.decode()
decoded_default_app_user_name = decoded_default_app_user_name.decode()
decoded_default_app_user_password = decoded_default_app_user_password.decode()
decoded_default_app_admin_name = decoded_default_app_admin_name.decode()
decoded_default_app_admin_password = decoded_default_app_admin_password.decode()
decoded_jwt_secret_key = decoded_jwt_secret_key.decode()

# Test
assert neo4j_db_user == 'neo4j', 'neo4j_db_user should be neo4j'
assert neo4j_db_password == decoded_neo4j_db_password, 'you failed as programmer'
assert default_app_user_name == decoded_default_app_user_name, 'you failed as programmer'
assert default_app_user_password == decoded_default_app_user_password, 'you failed as programmer'
assert default_app_admin_name == decoded_default_app_admin_name, 'you failed as programmer'
assert default_app_admin_password == decoded_default_app_admin_password, 'you failed as programmer'
assert jwt_secret_key == decoded_jwt_secret_key, 'you failed as programmer'

# Set file permissions
os.chmod(os.path.expanduser('~/neo4j_db_user.secret'), 0o440)
os.chmod(os.path.expanduser('~/neo4j_db_password.secret'), 0o440)
os.chmod(os.path.expanduser('~/default_app_user_name.secret'), 0o440)
os.chmod(os.path.expanduser('~/default_app_user_password.secret'), 0o440)
os.chmod(os.path.expanduser('~/default_app_admin_name.secret'), 0o440)
os.chmod(os.path.expanduser('~/default_app_admin_password.secret'), 0o440)
os.chmod(os.path.expanduser('~/jwt_secret_key.secret'), 0o440)
