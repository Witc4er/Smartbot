import re


# def find_all_emails(text):
#     result = re.findall(r"[a-zA-Z._]{1}[a-zA-Z._0-9]+@[a-zA-Z]+\.[a-z]{2}[a-z]*", text)
#     return resul
# print(find_all_emails( 'Ima.Fool@iana.org Ima.Fool@iana.o 1Fool@iana.org first_last@iana.org first.middle.last@iana.or a@test.com abc111@test.com.net'))

def is_email_correct(email):

    check = re.match(r"[a-zA-Z._]{1}[a-zA-Z._0-9]+@[a-zA-Z]+\.[a-z]{2}[a-z]*", email)
    if check: return email
    return False
print(is_email_correct("Ima.Fool@iana.org"))
