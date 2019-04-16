import os
import ecdsa
import requests
import qrcode_terminal

def save_to_file(wallet_name,file_name, contents):
    fh = open(wallet_name+file_name, 'w')
    fh.write(contents)
    fh.close()

def account(wallet_name):
    f = open(wallet_name + '_address.txt')
    btcaddress = f.read()
    print("Your address is :" + btcaddress)
    txinfo = requests.get("https://blockchain.info/rawaddr/" + btcaddress)
    print(txinfo.text)
    infi(wallet_name)

def qr(wallet_name):
    f = open(wallet_name + '_address.txt')
    btcaddress = f.read()
    qrcode_terminal.draw(btcaddress)
    infi(wallet_name)
def newwallet(wallet_name):
    print('Wallet key file is not found.Creating a new wallet')
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    save_to_file(wallet_name, '_private_key.txt', private_key.to_string().hex())
    print("private key: 0x" + private_key.to_string().hex())
    public_key = private_key.get_verifying_key()
    print("public key: 0x" + public_key.to_string().hex())
    addr = requests.get("https://blockchain.info/q/addrpubkey/" + public_key.to_string().hex())
    print("Your address is :" + addr.text)
    save_to_file(wallet_name, '_address.txt', addr.text)
    save_to_file(wallet_name, '_public_key.txt', private_key.to_string().hex())
    infi(wallet_name)
def gethistory(wallet_name):
    f = open(wallet_name + '_address.txt')
    btcaddress = f.read()
    hist = requests.get("https://blockchain.info/q/txresult/" + btcaddress)
    print(hist.text)
    infi(wallet_name)
def infi(wallet_name):
    if os.path.exists(wallet_name+'_address.txt'):
            pd = input("Which operation you want?(This is not testnet!)\n"
                       "Wallet name now is "+wallet_name +"\n"
                  "1.Open my wallet\n"
                  "2.Create new wallet\n"
                       "3.Show my QR codd\n"
                       "4.Show my transaction history\n"
                       "5.Change a wallet\n"
                       "0.Exit\n")
            if pd == '1':
                account(wallet_name)

            elif pd == '2' :
                newwallet_name = input("Please type your new wallet's name:")
                newwallet(newwallet_name)
            elif pd == '3':
                qr(wallet_name)
            elif pd == '4':
                gethistory(wallet_name)
            elif pd == '5':
                start()
            elif pd == '0':
                os._exit(1)

    else:
        pd = input("Do you want a wallet named :"+wallet_name+"?(y/n)")
        if pd == 'y':
            newwallet(wallet_name)
        else:
            infi(wallet_name)
def start():
    wallet_name = input("Please type your wallet's name:")
    infi(wallet_name)

start()