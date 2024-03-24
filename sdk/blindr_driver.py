from blindr_config import BlindrConfig
from blindr_client import MyAPIClient


my_config = BlindrConfig(base_url="http://127.0.0.1:5000", api_key="")
my_client = MyAPIClient(my_config)


constraint = """{
	"auth": [
		["password", "hello123"],
		["What is your mothers maiden name", "Duke"],
    ["What is your favorite ice cream flavor", "chocolate"]
    ],
    "withdrawal_limit" : 10
}"""

message = """{
	"sender": "1FWu4Z9NoBWnguurBCdXpmM2xuiog6kbdy",
	"receiver": "3C3nZhpVjjDGo7vGzBCTJkKfYzCGWGLWsq",
	"amount": 100
}"""

try:
	signature = my_client.create_session_and_sign(message, constraint)
	print(f"signature is {signature}")
	if my_client.delete_key(constraint):
		print("Deleted key")

except:
	if my_client.delete_key(constraint):
		print("Deleted key")








constraint = """{
	"auth": [
		["password", "james duke123"],
		["What is your mothers maiden name", "Duke"],
    ["What is your favorite ice cream flavor", "chocolate"]
    ],
    "withdrawal_limit" : 10
}"""

message = """{
	"sender": "1FWu4Z9NoBWnguurBCdXpmM2xuiog6kbdy",
	"receiver": "3C3nZhpVjjDGo7vGzBCTJkKfYzCGWGLWsq",
	"amount": 100
}"""


try:
	
	current_session = my_client.create_or_restart_session(constraint)

	# current_session = my_client.restart_session_with_hash(constraint)

	signature = my_client.sign_message(message, current_session['public_value'], current_session['public_key'], constraint)
	print(f"signature is {signature}")
	if my_client.delete_key(constraint):
		print("Deleted key")

except:
	if my_client.delete_key(constraint):
		print("Deleted key")



