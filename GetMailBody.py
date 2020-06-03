from MailHeroku import TextBody,MailSenderList,MailSubjectList
msgformat=[]
msglink=[]

if len(TextBody)!=0:
	i=0
	for msg in TextBody:
		start = msg.find('Disclaimer:') 
		end = msg.find("To view this discussion on the web, visit ", start)+42
		msgformat.append(MailSubjectList[0] + MailSenderList[0] + msg[end:] + msg[:start])
		i=i+1

if __name__ == "__main__":
	for msg in msgformat:
		print(msg)
		print("====================================\n\n\n\n")
