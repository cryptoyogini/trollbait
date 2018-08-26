
%run xetrapalworkflow-final.py
with open("/home/ananda/profanity.txt","r") as f:
    profanitylist=json.loads(f.read())
def isprofane(text):
    for word in profanitylist:
       if word in text.lower():
           print word
           return True

    return False
trainsheet=anandagd.open_by_key("1FRE-7UFoQN0V0qqaRCeMTkNWDxKpYYZuJqRi5TLUQf4")
trollvic=trainsheet.worksheet_by_title("trollvictimlabel")
trollvicdf=trollvic.get_as_df()
