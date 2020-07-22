from MailHeroku import TextBody,MailSenderList,MailSubjectList
msgformat=[]
msglink=[]
no_of_msgs=len(TextBody)
if no_of_msgs !=0:
	i=0
	for msg in TextBody:
		# print("START\n")
		# print(msg)
		start = msg.find('Disclaimer:') 
		end = msg.find("To view this discussion on the web visit ", start)+41
		msgformat.append(f"---- Message {i+1}/{no_of_msgs} ----\n\n"+MailSubjectList[i] + MailSenderList[i] + msg[end:] + msg[:start]+ " ")
		i=i+1

if __name__ == "__main__":
	for msg in msgformat:
		print("====================================\n\n\n\n")
		print(msg)
		
