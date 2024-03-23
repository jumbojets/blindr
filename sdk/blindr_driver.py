from blindr_config import BlindrConfig
from blindr_client import MyAPIClient

my_config = BlindrConfig(base_url="http://127.0.0.1:5000", api_key="")
my_client = MyAPIClient(my_config)

# my_client.create_new_session("constraint1")
print(my_client.restart_session_with_hash("constraint1"))

print(my_client.sign_message("message1", "public_value1", "public_key1", "constraint1"))