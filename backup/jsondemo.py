import json

example_js = [{ "client_register_1" : "Passed" },{ "client_login_1" : "Passed" },{ "client_login_2" : "Failed" },{ "multiple_client_login_1" : "Failed" }]
with open("testJs.json", "w") as f:
    json.dump(example_js, f)