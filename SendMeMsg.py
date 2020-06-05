from twilio.rest import Client 
from GetMailBody import msgformat
import time

def SendMeMsg():
    account_sid = 'AC72656992c0449bc1d0160ce666591eb8' 
    auth_token = 'ac2c4ac5529e442c619eba28d4b52957' 

    client = Client(account_sid, auth_token) 

    fromID='whatsapp:+14155238886'
    toID='whatsapp:+917249255271'
    mailSeparator="|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |\n"
    Separate=3*mailSeparator

    
    maxsize=1599

    if len(msgformat) != 0:
        message = client.messages.create( 
                                from_=fromID,  
                                body=f"=======================\n     Total {len(msgformat)} messages today\
                                    =======================\n",    
                                to=toID)
        for msg in msgformat:
            msglen=len(msg)
            i=0
            next=0
            while True:
                next=i+maxsize
                if next > msglen-1:
                    next=msglen-1
                while(msg[next] != "\n"):
                    next=next-1
                partial=msg[i:next]
                #print(partial)
                if len(partial)==0:
                    partial=Separate
                message = client.messages.create( 
                                from_=fromID,  
                                body=partial,    
                                to=toID
                            ) 
                if(partial == Separate):
                    break
                time.sleep(1)
                i=next
        
            time.sleep(1)
    
        #print(message.sid)


if __name__ == "__main__":
    SendMeMsg()