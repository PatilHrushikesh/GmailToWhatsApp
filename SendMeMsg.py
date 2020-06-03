from twilio.rest import Client 
from GetMailBody import msgformat
import time

def SendMeMsg():
    account_sid = 'AC72656992c0449bc1d0160ce666591eb8' 
    auth_token = 'ac2c4ac5529e442c619eba28d4b52957' 
    client = Client(account_sid, auth_token) 
    fromID='whatsapp:+14155238886'
    toID='whatsapp:+917249255271'
    if len(msgformat) != 0:
        for msg in msgformat:
            maxsize=1599
            times=len(msg)//maxsize + 2
            i=0
            while i< times:
                partial=msg[i*maxsize:(i+1)*maxsize]
                #print(partial)
                if len(partial)==0:
                    partial="-------------------------------\n-------------------------------"
                message = client.messages.create( 
                                from_=fromID,  
                                body=partial,    
                                to=toID
                            ) 
                time.sleep(1)
                i=i+1
        
            time.sleep(3)
    
        #print(message.sid)


if __name__ == "__main__":
    SendMeMsg()