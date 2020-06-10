import looker_sdk


sdk = looker_sdk.init31()  # or init40() for v4.0 API
# and away you go
my_user = sdk.me()
new_user = looker_sdk.models.WriteUser(first_name="Jane", last_name="Doe")
created_user = sdk.create_user(body=new_user)
print(created_user)
