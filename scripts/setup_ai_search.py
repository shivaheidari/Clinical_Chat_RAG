import json

with open("confings/azure_keys.json") as f:
    keys = json.load(f)

print(keys["STORAGE_ACCOUNT_NAME"])
print(keys["STORAGE_ACCOUNT_KEY"])