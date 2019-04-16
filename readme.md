
# Jokewallet 0.1
You can create a offline wallet and do some operation.

If I have free time I will complete it and make a standalone installer for it~

Or use Django make a web application and add the private_key protection.

I just know base64 and maybe cut the key and exchange the order?

I will learn something about it .

I didn't get transaction api still now, so I can't do transaction now.

I was trying to use RPC, but I can't connect to my BTC core so change to this way.

This is my second time use python.

## Implemented feature
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
I don't want to teach how to install python...

But after install python

You need install ~~these~~ :


   ~~pip install os~~
   ~~pip install ecdsa~~
   ~~pip install requests~~
   ~~pip install qrcode_terminal~~
    You can use pip install it !

## Install Jokewallet
Install Jokewallet:
    https://pypi.org/manage/project/jokewallet/collaboration/
    ~~Git clone https://github.com/zots0127/Jokewallet.git ~~
    ~~cd Jokewallet~~
    pip install Jokewallet

## Usage
Run Jokewallet:

    python
    
    import jokewallet

    start()
    
    Then you can use it.

## License

I don't know about it. Let it go.
