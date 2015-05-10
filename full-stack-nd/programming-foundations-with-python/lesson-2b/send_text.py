from twilio import rest
import send_text_vars as vars
# Your Account Sid and Auth Token from twilio.com/user/account
client = rest.TwilioRestClient(vars.account_sid, vars.auth_token)
message = client.messages.create(
    body="Hiya",
    to=vars.to_number, # Replace with your phone number
    from_=vars.from_number) # Replace with your Twilio number
print message.sid

