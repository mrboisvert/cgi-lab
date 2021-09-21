import cgi, cgitb
import secret

form = cgi.FieldStorage()

username = form.getvalue("username")
password = form.getvalue("password")

if username==secret.username and password==secret.password:
    print("Set-Cookie: password=%s;" % password)
    print("Set-Cookie: username=%s;" % username)

print("Content-type:text/html\r\n\r\n")

print("<p>Username: %s </p>" % username)
print("<p>Password: %s </p>" % password)

