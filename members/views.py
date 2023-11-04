from math import floor
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Users,ItemsOnBid, ItemsClaimed
from requests import Session
import json
import time
from django.contrib.auth.hashers import make_password, check_password
import js2py
# from temp import *
from web3 import Web3

hashed_pwd = make_password("plain_text")
check_password("plain_text",hashed_pwd)

# def transfer_ether(request):
#     # eval_res, tempfile = js2py.run_file("./members/javascript.js") 
#     # tempfile.transfer("0x74bbf4b2223496C4547c44268242A5196E3c6499","0x532600377959B703AA4AC2c468DeDe8FAA40B576",0.1)
#     js2py.translate_file("javascript.js", "temp.py") 
#     temp.transfer("0x74bbf4b2223496C4547c44268242A5196E3c6499","0x532600377959B703AA4AC2c468DeDe8FAA40B576",0.1)
#     print("success")
#     return HttpResponse("done")
infura_url = "https://sepolia.infura.io/v3/ba4a7cd723164ef58662195dfa699f99"
web3 = Web3(Web3.HTTPProvider(infura_url))

def form_view(request):
    return render(request,"form.html")

def wallet_view(request):
    return render(
        request,'wallet.html'
    )
def index(request):
    template=loader.get_template('index.html')
    return HttpResponse(template.render())

def first(request):
    template=loader.get_template('first.html')
    return HttpResponse(template.render())

def clientLogin(request):
    template=loader.get_template('cl.html')
    return HttpResponse(template.render({},request))

def clientRegister(request):
    template=loader.get_template('cr.html')
    return HttpResponse(template.render({},request))

def clientRegistered(request):
    client_username=request.POST['username']
    client_password=request.POST['password']
    wallet_addr = request.POST['wallet_address']
    hashed_client_password=make_password(client_password)
    client_email=request.POST['email']
    client_confirm_password=request.POST['confirm_password']

    for x in Users.objects.all().values():
        if(x['username']==client_username):
            message="USERNAME TAKEN"
            context={
                "message":message
            }
            return render(request,'message.html',context)

    if(client_confirm_password!=client_password):
        message="PASSWORDS DO NOT MATCH"
        context={
            "message":message
        }
        return render(request,'message.html',context)
    user=Users(username=client_username, role='0',password=hashed_client_password,balance=10000,email=client_email, wallet_addr = wallet_addr)
    user.save()
    return HttpResponseRedirect(reverse('clientLogin'))

def clientLoggedIn(request):
    
    client_username=request.POST['username']
    client_password=request.POST['password']
    clients=Users.objects.filter(username=client_username).values()
    if(len(clients)==0):
        message="USERNAME DOES NOT EXIST"
        context={
            "message":message
        }
        return render(request,'message.html',context)

    saved_hashed_password = clients[0]['password']
    saved_role=clients[0]['role']
    
    if(saved_role!=0):
        message="NOT A VALID CLIENT"
        context={
            "message":message
        }
        return render(request,'message.html',context)
    if(check_password(client_password,saved_hashed_password)!=True):
        message="WRONG PASSWORD"
        context={
            "message":message
        }
        return render(request,'message.html',context)
    template=loader.get_template('chome.html')
    context={
        'client':clients[0]
        # more to be added
    }
    return HttpResponse(template.render(context,request))

def adminLogin(request):
    template=loader.get_template('al.html')
    return HttpResponse(template.render({},request))

def adminRegister(request):
    template=loader.get_template('ar.html')
    return HttpResponse(template.render({},request))

def adminRegistered(request):
    admin_username=request.POST['username']
    admin_password=request.POST['password']
    hashed_admin_password=make_password(admin_password)
    admin_email=request.POST['email']
    admin_confirm_password=request.POST['confirm_password']

    for x in Users.objects.all().values():
        if(x['username']==admin_username):
            message="USERNAME TAKEN"
            context={
                "message":message
            }
            return render(request,'message.html',context)

    if(admin_confirm_password!=admin_password):
        message="PASSWORDS DO NOT MATCH"
        context={
            "message":message
        }
        return render(request,'message.html',context)

    user=Users(username=admin_username, role='1',password=hashed_admin_password,balance=10000,email=admin_email)
    user.save()
    return HttpResponseRedirect(reverse('adminLogin'))

def adminLoggedIn(request):
    admin_username=request.POST['username']
    admin_password=request.POST['password']
    admins=Users.objects.filter(username=admin_username).values()
    if(len(admins)==0):
        message="USERNAME DOES NOT EXIST"
        context={
            "message":message
        }
        return render(request,'message.html',context)

    saved_hashed_password = admins[0]['password']
    saved_role=admins[0]['role']
    if(saved_role!=1):
        message="NOT A VALID ADMIN!"
        context={
            "message":message
        }
        return render(request,'message.html',context)
    if(check_password(admin_password,saved_hashed_password)!=True):
        message="PASSWORDS DO NOT MATCH"
        context={
            "message":message
        }
        return render(request,'message.html',context)

    template=loader.get_template('ahome.html')
    context={
        'admin':admins[0]
        # more to be added
    }
    return HttpResponse(template.render(context,request))

# def auctionPortalItems(request):
#     items=ItemsOnBid.objects.filter(valid=1).values()
#     current_username=request.POST['username']
#     context={
#     'items':items,
#     'current_username':current_username
#     }
#     return render(request,'auction.html',context)

def auctionPortalItems(request):
    items=ItemsOnBid.objects.filter(valid=1).values()
    current_username=request.POST['username']
    current_time=int(time.time())
    for item in ItemsOnBid.objects.filter(valid=1):
        item.time_left=70-current_time+item.initial_time
        item.hours=int((item.time_left)/3600)
        item.minutes=(item.time_left)/60 -item.hours*60
        item.save()
        if item.time_left<=0:
            # variable created
            sender_address = Users.objects.get(username=item.highest_bidder_username).wallet_addr
            receiver_address = Users.objects.get(username=item.owner_username).wallet_addr
            amount = item.highest_bid

            owner=Users.objects.filter(username=item.owner_username)[0]
            item.owner_username=item.highest_bidder_username
            owner.balance=owner.balance+item.highest_bid
            item.save()
            claimed_item=ItemsClaimed(item_name=item.item_name,item_descr=item.item_descr,item_picture=item.item_picture,owner_username=item.owner_username,highest_bidder_username=item.highest_bidder_username, highest_bid = item.highest_bid)
            claimed_item.save()
            user=Users.objects.filter(username=item.highest_bidder_username)[0]
            user.balance=user.balance-item.highest_bid
            owner.save()
            user.save()
            item.delete()

            
            context={
                "senderAddress":sender_address,
                "receiverAddress":receiver_address,
                "amount":amount,
            }
            return render(request,'form.html',context)

    context={
    'items':items,
    'current_username':current_username
    }
    return render(request,'auction.html',context)

def addItem(request):
    current_username=request.POST['username']
    context={
        'current_username':current_username
    }
    return render(request,'addItem.html',context)

def itemAdded(request):
    item_name=request.POST['item_name']
    item_descr=request.POST['item_descr']
    item_picture=request.POST['item_picture']
    minimum_bid=request.POST['minimum_bid']
    username=request.POST['username']
    item=ItemsOnBid(item_name=item_name,item_descr=item_descr,item_picture=item_picture,highest_bid=minimum_bid,highest_bidder_username=username,owner_username=username,valid='0')
    item.save()
    message="REQUEST HAS BEEN SENT TO ADMIN"
    context={
        "message":message
    }
    return render(request,'message.html',context)

def bidUpdate(request) :
    
    current_item_bid=int(request.POST['bid'])
    current_item_id=request.POST['item_id']
    current_username=request.POST['username']
    wallet_address = Users.objects.get(username=current_username).wallet_addr
    balance_wei = web3.eth.get_balance(wallet_address)
    balance_eth = web3.from_wei(balance_wei, 'ether')
    print(wallet_address, balance_eth)
    item=ItemsOnBid.objects.get(id=current_item_id)
    saved_highest_bid=item.highest_bid
    if(current_item_bid>saved_highest_bid and current_item_bid < balance_eth) :
        item.highest_bid=current_item_bid
        item.highest_bidder_username=current_username
        item.save() 
        message="BID UPDATED"
        context={
            "message":message
        }
        return render(request,'message.html',context)
    elif(current_item_bid<balance_eth):
        message="BID NOT ACCEPTED! You don't have enough balance"
    message="BID NOT ACCEPTED! Auction has ended"

    context={
        "message":message
    }
    return render(request,'message.html',context)

def bidRequest(request) :
    items=ItemsOnBid.objects.filter(valid=0).values()
    context={
    'items':items
    }
    return render(request,'requests.html',context)

# def bidAccept(request) :
#     current_item_id=request.POST['item_id']
#     item=ItemsOnBid.objects.get(id=current_item_id)
#     item.valid=1
#     item.save()
#     return HttpResponse("Item Accepetd")

def bidAccept(request) :
    current_item_id=request.POST['item_id']
    item=ItemsOnBid.objects.get(id=current_item_id)
    item.valid=1
    item.initial_time=time.time()
    item.save()
    message="ITEM ACCEPTED"
    context={
        "message":message
    }
    return render(request,'message.html',context)

def bidReject(request) :
    current_item_id=request.POST['item_id']
    item=ItemsOnBid.objects.get(id=current_item_id)
    item.delete()
    message="ITEM REJECTED"
    context={
        "message":message
    }
    return render(request,'message.html',context)

def balanceUpdate(request):
    username=request.POST['username']
    price=request.POST['price']
    bitcoins=request.POST['bitcoins']
    name=Users.objects.filter(username=username)[0]
    amount=floor(float(price))*int(bitcoins)
    name.balance= name.balance + amount
    context={
        "message":"Current balance:" + str(name.balance)
    }
    name.save()
    
    return render(request,'message.html',context)

def myProfile(request):
        username=request.POST['username']
        items=ItemsClaimed.objects.filter(owner_username=username).values()
        user=Users.objects.filter(username=username)
        if(user[0].role==0): 
            role="client"
        else:
            role="admin"
        context={
            'items':items,
            'user':user[0],
            'role':role
        }
        return render(request,'myProfile.html',context)

# def crypto(request):
#     url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category'

#     parameters = {
#     'id':"605e2ce9d41eae1066535f7c",
#     'start':'1',
#     'limit':'20',
#     'convert':'USD'
#     }
#     headers = {
#     'Accepts': 'application/json',
#     'X-CMC_PRO_API_KEY': '3a23a8ef-d582-4884-8ae5-7c8acaaf56a7',
#     }

#     session = Session()
#     session.headers.update(headers)

#     response = session.get(url, params=parameters)
#     json_data = json.loads(response.text)
#     with open("data_file.json", "w") as write_file:
#         json.dump(json_data, write_file, indent=4)
#     newdata=json_data['data']
#     Bitcoin=newdata['coins']
#     #Bitcoin
#     coinarray=Bitcoin[0]
#     quote=coinarray['quote']
#     USD=quote['USD']
#     price=USD['price']
#     #Ethereum
#     coinarray_2=Bitcoin[1]
#     quote_2=coinarray_2['quote']
#     USD_2=quote_2['USD']
#     price_2=USD_2['price']
#     #Maker
#     coinarray_4=Bitcoin[6]
#     quote_4=coinarray_4['quote']
#     USD_4=quote_4['USD']
#     price_4=USD_4['price']
    
#     template=loader.get_template('crypto.html')
#     # username=request.POST['username']
#     context={
#         "price_1":price,
#         "price_2":price_2,
#         # "username":username  
#     }
#     return HttpResponse(template.render(context,request))

# def crypto2(request):
#     url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category'

#     parameters = {
#     'id':"605e2ce9d41eae1066535f7c",
#     'start':'1',
#     'limit':'20',
#     'convert':'USD'
#     }
#     headers = {
#     'Accepts': 'application/json',
#     'X-CMC_PRO_API_KEY': '3a23a8ef-d582-4884-8ae5-7c8acaaf56a7',
#     }

#     session = Session()
#     session.headers.update(headers)

#     response = session.get(url, params=parameters)
#     json_data = json.loads(response.text)
#     with open("data_file.json", "w") as write_file:
#         json.dump(json_data, write_file, indent=4)
#     newdata=json_data['data']
#     Bitcoin=newdata['coins']
#     #Bitcoin
#     coinarray=Bitcoin[0]
#     quote=coinarray['quote']
#     USD=quote['USD']
#     price=USD['price']
#     #Ethereum
#     coinarray_2=Bitcoin[1]
#     quote_2=coinarray_2['quote']
#     USD_2=quote_2['USD']
#     price_2=USD_2['price']
#     #Maker
#     coinarray_4=Bitcoin[6]
#     quote_4=coinarray_4['quote']
#     USD_4=quote_4['USD']
#     price_4=USD_4['price']
    
#     template=loader.get_template('crypto.html')
#     username=request.POST['username']
#     context={
#         "price_1":price,
#         "price_2":price_2,
#         "username":username  
#     }
#     return HttpResponse(template.render(context,request))

    