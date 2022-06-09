Dict = {}

Dict.update({tuple((0.9, 1.0)) : lambda d: d <=20})
Dict.update({tuple((0.7, 0.8)) : lambda d: d <=15})
Dict.update({tuple((0.5, 0.6)) : lambda d: d <=10})
Dict.update({tuple((0.2, 0.4)) : lambda d: d <=7})
Dict.update({tuple((0.0, 0.1)) : lambda d: d <=3})

# print(Dict)
tr = 0.6
# print(type(tr))
delt = 12

# if tr in Dict.keys:
#     print("yes")
# else:
#     print("no")
res = None
bol = None
for idx, ele in enumerate(Dict.keys()):
    if ele[0] <= tr  and tr <= ele[1]:
        res = idx
        x = Dict[ele]
        bol = x(delt)
        break

print("index ", res)

print("decision ", bol)