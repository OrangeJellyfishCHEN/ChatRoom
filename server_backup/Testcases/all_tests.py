import os
import json
os.system("sh all_tests.sh")
f = open("testcases.txt", "r")
tests = f.readlines()
i = 0
while i < len(tests):
    tests[i] = int(tests[i])
    i += 1
t1 = {}
if tests[0] == 0:
    t1["register and login test"] = "Passed"
else:
    t1["register and login test"] = "Failed"
t2 = {}
if tests[1] == 0:
    t2["create channels test"] = "Passed"
else:
    t2["create channels test"] = "Failed"
t3 = {}
if tests[2] == 0:
    t3["join channels and channels test"] = "Passed"
else:
    t3["join channels and channels test"] = "Failed"
t4 = {}
if tests[3] == 0:
    t4["say test"] = "Passed"
else:
    t4["say test"] = "Failed"
t5 = {}
if tests[4] == 0:
    t5["multiple clients test"] = "Passed"
else:
    t5["multiple clients test"] = "Failed"
result = [t1, t2, t3, t4, t5]
with open("all_test_result.json", "w") as f:
    json.dump(result, f)