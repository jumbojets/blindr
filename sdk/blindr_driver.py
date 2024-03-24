from blindr_config import BlindrConfig
from blindr_client import MyAPIClient
from libblindr import hash_spend_constraint

my_config = BlindrConfig(base_url="http://127.0.0.1:5000", api_key="")
my_client = MyAPIClient(my_config)

# my_client.create_new_session("constraint1")
# print(my_client.restart_session_with_hash("constraint1"))

# print(my_client.sign_message("message1", "public_value1", "public_key1", "constraint1"))

constraint = """{
	"auth": [
		["password", "hello123"],
		["What is your mothers maiden name", "Duke"],
    ["What is your favorite ice cream flavor", "chocolate"]
    ],
    "withdrawal_limit" : 10
}"""

message = """{
	"sender": "asdfasdf",
	"receiver": "asdfasdf",
	"amount": 100
}"""


try:
	current_session = my_client.create_new_session(constraint)

	# current_session = my_client.restart_session_with_hash(constraint)

	signature = my_client.sign_message(message, current_session['public_value'], current_session['public_key'], constraint)
except:
	print(my_client.delete_key(constraint))



