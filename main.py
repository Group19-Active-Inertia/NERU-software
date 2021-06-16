from classes.login import Session

s = Session()
s.attemptLogin()

# Start CoAP server here

s.chooseSite()

# start rest of modules here
