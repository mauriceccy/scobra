import os

folders = ["analysis", "classes", "io", "manipulation"]
reqs = {}

for v in folders:
    os.system(os.path.join("pipreqs scobra",v,""))
    with open(os.path.join("scobra",v,"requirements.txt"),'r') as req_file:
        line = req_file.readline()
        while(line != ""):
            name, version = line.split("==")
            version = version.rstrip("\n")
            if name in reqs:
                if reqs[name] < version:
                    line = req_file.readline()
                    continue
            reqs[name] = version
            line = req_file.readline()

    os.system(os.path.join("rm scobra",v,"requirements.txt"))
req_file.append("xlrd>=1.0.0")
req_file.append("xlwt>=1.0.0")
with open("requirements.txt", "w") as req_file:
    for n in reqs:
        req_file.write(n+">="+reqs[n]+"\n")
        
