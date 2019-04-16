
# Jokewallet 0.0.4
You can create a offline wallet and do some operation.

## (send() need a privity api but apply it need 3~4days)

If I have free time I will complete it and make a standalone installer for it~

Or use Django make a web application and add the private_key protection.

I just know base64 and maybe cut the key and exchange the order?

I will learn something about it .

I didn't get transaction api still now, so I can't do transaction now.

## I was trying to use RPC, but I can't connect to my BTC core so change to this way.

This is my second time use python.

## Implemented feature
![Image text](https://github.com/zots0127/Jokewallet/raw/master/img/create.png)\
![Image text](https://github.com/zots0127/Jokewallet/raw/master/img/menu.png)\
![Image text](https://github.com/zots0127/Jokewallet/raw/master/img/feature.png)\
1.Open my wallet       

Use public api query address infomation

2.Create new wallet    

Generate a new key and new address

3.Show my QR codd     

Use funny terminal qrcode lib show qrcode in terminal,actully it can also  use an api but can't show without GUI



4.Show my transaction history   

Use public api query TX info but if don't have can't get right result

5.Change a wallet

Call another function to change Wallet

0.Exit

Exit


## Install Dependencies
I don't want to teach how to install python3.7...

But after install python3.7

You need install ~~these~~ :



    pip install ecdsa
    pip install requests
    pip install qrcode_terminal


## Install Jokewallet
Install Jokewallet:
    https://pypi.org/manage/project/jokewallet/collaboration/
    Git clone https://github.com/zots0127/Jokewallet.git \
    cd Jokewallet/jokewallet \
    ~~pip install Jokewallet~~  Will be fixed

## Usage
Run Jokewallet:

    python jokewallet.py    

    Input a wallet name ,if already exist will open wallet,then you can use it.

    Otherwise create a new wallet.

## License

MIT
