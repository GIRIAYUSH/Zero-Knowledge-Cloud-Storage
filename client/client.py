from doctest import master
import menu
import requests
from backports.pbkdf2 import pbkdf2_hmac
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util import Padding
from Cryptodome.Hash import HMAC
from time import sleep


url = "http://127.0.0.1:8000/"
token = None
master_key = None

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def Login():
    global master_key;
    global token;
    email = input("Enter Email:")
    password = input("Enter password:")
    resp = requests.get(url + "users/get_salt",params={"email":email})
    if resp.status_code == 404:
        print("User does not exist")
        exit()
    salt = bytes.fromhex(resp.text.strip('"'))
    master_and_derived_key = pbkdf2_hmac("sha256","{}:{}".format(email,password).encode(),salt,50000,32)
    derived_key = master_and_derived_key[:len(master_and_derived_key)//2]
    master_key_enc_key = master_and_derived_key[len(master_and_derived_key)//2:]
    crypt = AES.new(master_key_enc_key,AES.MODE_CBC)

    resp = requests.post(url + "users/login",json={"email":email,"derived_key":derived_key.hex()})
    if resp.status_code in [404,403]:
        print("Invalid credentials")
        exit()
    token = resp.json()["access_token"]
    encrypted_master_key = resp.json()["encrypted_master_password"]
    master_key = crypt.decrypt(bytes.fromhex(encrypted_master_key))
    print("Login successful")
    sleep(5)


def Register():
    global master_key;
    global token;
    name = input("Enter name:")
    email = input("Enter Email:")
    password = input("Enter password:")
    salt = get_random_bytes(16)
    master_key = get_random_bytes(32)
    master_and_derived_key = pbkdf2_hmac("sha256","{}:{}".format(email,password).encode(),salt,50000,32)
    derived_key = master_and_derived_key[:len(master_and_derived_key)//2]
    master_key_enc_key = master_and_derived_key[len(master_and_derived_key)//2:]
    crypt = AES.new(master_key_enc_key,AES.MODE_CBC)
    encrypted_master_key = crypt.encrypt(master_key)

    resp = requests.put(url + "users/register",json={"email":email,"derived_key":derived_key.hex(),"name":name,"encrypted_master_password":encrypted_master_key.hex(),"salt":salt.hex()})

    if resp.status_code != 200:
        print("Invalid input")
        print(resp.json())
        exit()
    print("Successfully created user")
    exit()

def Quit():
    exit()

def UploadFile():
    if token == None:
        print("Please login")
        sleep(10)
        return
    file_path = input("Enter file location:")
    with open(file_path,"rb") as file:
        file_name = file_path.split("/")[-1]
        file_key = get_random_bytes(32)
        crypt = AES.new(file_key,AES.MODE_ECB)
        key_crypt = AES.new(master_key,AES.MODE_ECB)
        encrypted_file_key = key_crypt.encrypt(file_key)
        encrypted_data = crypt.encrypt(Padding.pad(file.read(),16))
        hmac = HMAC.new(master_key,encrypted_data).hexdigest()
        temp = open("/tmp/" + file_name,"wb")
        temp.write(encrypted_data)
        temp.close()
        temp = open("/tmp/" + file_name,"rb")
        resp = requests.put(url + "files/upload",auth=BearerAuth(token),files={"encrypted_file":temp},data={"encrypted_file_key":encrypted_file_key.hex(),"hmac":hmac})
        temp.close()
        if resp.status_code != 200:
            print("Something went wrong")
            exit()
        file_id = resp.json()["file_id"]
        print("File_id:",file_id)
        sleep(10)

def GetFileById():
    if token == None:
        print("Please login")
        sleep(10)
        return
    file_id = input("Enter file_id:")
    resp = requests.get(url + "files/{}".format(file_id),auth=BearerAuth(token))
    if resp.json().get("status") == "error":
        print("Invalid file id")
        sleep(10)
        return
    file_name = resp.json()["file_name"]
    encrypted_file_key = bytes.fromhex(resp.json()["encrypted_file_key"])
    dirty_hmac = bytes.fromhex(resp.json()["hmac"])
    key_crypt = AES.new(master_key,AES.MODE_ECB)
    file_key = key_crypt.decrypt(encrypted_file_key)
    resp = requests.get(url + "files/{}/download".format(file_id),auth=BearerAuth(token))
    crypt = AES.new(file_key,AES.MODE_ECB)
    print("Decrypting {}...".format(file_name))
    with open(file_name,"wb") as file:
        hmac = HMAC.new(master_key,resp.content)
        try:
            hmac.verify(dirty_hmac)
        except:
            print("INVALID HMAC ,FILE HAS BEEN MODIFIED")
            exit()
        file_data = Padding.unpad(crypt.decrypt(resp.content),16)
        file.write(file_data)
    print("Data written to {}".format(file_name))
    sleep(10)

print("Welcome to Encrypt EveryWhere Client")
splash_options = [("Login",Login),
            ("Register",Register),
            ("Upload",UploadFile),
            ("Download",GetFileById),
            ("Quit",Quit)]
splash_menu = menu.Menu(title="Welcome to Encrypt EveryWhere Client",options=splash_options)
splash_menu.open()
