from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from Auction.models import ItemsClaimed, ItemsOnBid, Users
from web3 import Web3
from Auction.exceptions import UserNotFoundException, InsufficientBalanceException, InsufficientAmountException


def SendNotif(bid):
    item = ItemsOnBid.objects.get(itemId=bid.itemId)
    curr_bidders = list(bid.contribution.keys())
    req_bidders = [bidder for bidder in item.bidders if bidder not in curr_bidders]
    for bidder in req_bidders:
        user = Users.objects.get(userId=bidder)

        subject = 'New Bid Placed on {}'.format(item.itemName)
        message = 'Hello {},\n\nA new bid has been placed on the item "{}".\n\nSincerely,\nYourApp Team'.format(
            user.username, item.itemName
        )
        from_email = 'yourapp@example.com' #add our email id here
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

def SendConfirmationNotif(bid):
    item = ItemsOnBid.objects.get(itemId=bid.itemId)
    curr_bidders = list(bid.contribution.keys())

    for bidder in curr_bidders:
        user = Users.objects.get(userId=bidder)

        subject = 'New Bid Successfully Placed on {}'.format(item.itemName)
        message = 'Hello {},\n\nYou have successfully placed a new bid on the item "{}".\n\nSincerely,\nYourApp Team'.format(
            user.username, item.itemName
        )
        from_email = 'yourapp@example.com' #add our email id here
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

def TimeBuffer(itemId):
    item = ItemsOnBid.objects.get(itemId=itemId)

    if timezone.now()< item.timeBuffer:
        return False
    else:
        item.timeBuffer = timezone.now() + timedelta(days=0, seconds=1)
        item.save()
        return True
    
def CheckBalance(userId, bidAmount):
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  #add url for our ethereum node here

    user = Users.objects.get(userId=userId)
    wallet_address = user.walletAddress

    try:
        balance_wei = w3.eth.get_balance(wallet_address)
        balance_eth = w3.fromWei(balance_wei, 'ether')
        
        if balance_eth >= bidAmount:
            return True
        else:
            return False
    
    except Exception as e:
        return False
    

def MaxBid(itemId):
    ItemsClaimed_list = ItemsClaimed.objects.filter(itemId=itemId)
    max_bid = max(ItemsClaimed_list, key=lambda x: x.amount)
    return max_bid

def CheckBid(bid):
    total_amount = sum(bid.contribution.values())
    bid.amount = total_amount
    bid.save()
    max_bid = MaxBid(bid.itemId)
    for userId, amount in bid.contribution.ItemsOnBid():
        try:
            user = Users.objects.get(userId=userId)
        except Users.DoesNotExist:
            raise UserNotFoundException(f"Error: Cannot place bid. User {userId} does not exist.")

        if not CheckBalance(userId, amount):
            raise InsufficientBalanceException(f"Error: Cannot place bid. User {userId} has insufficient balance.")    
    
    if total_amount < max_bid.amount:
        raise InsufficientAmountException(f"Error: Cannot place bid. The bid amount is insufficient. Max bid is {max_bid}.")
    
    if total_amount == max_bid:
        if bid.bidPlacedTime>max_bid.bidPlacedTime:
           raise InsufficientAmountException(f"Error: Cannot place bid. The bid amount is insufficient. Max bid is {max_bid}.") 
    
        
    return True

def AuctionInProgress(itemId):
    item = ItemsOnBid.objects.get(itemId=itemId)
    if item.auctionStartTime <= timezone.now() < item.auctionEndTime:
        return True
    else:
        return False