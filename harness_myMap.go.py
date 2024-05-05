import subprocess
import re
res = subprocess.run(["python3", "adventure.py", "myMap.map"],
                     stdin = open("tester/myMap.go.in"),
                     capture_output = True)
expected = open("tester/myMap.go.out").read()

# print("aaa",res.stdout.decode().split("\n")[0])
# print("bbb",expected.split("\n")[0])

res_list = res.stdout.decode().split("\n")
exp_list = expected.split("\n")
# print("res:",res_list)
# print("exp:",exp_list)
for i in range(len(res_list)):
    if not res_list[i] == exp_list[i]:
        print("res:", res_list[i])
        print("exp:", exp_list[i])

assert expected == res.stdout.decode()


