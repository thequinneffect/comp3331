# Suppose this is foo.py.

class SomeClass():
    def __init__(self, num):
        self.num = num

aClass = SomeClass(1)
bClass = SomeClass(2)
cClass = SomeClass(3)

originalDict = {
    "a" : aClass,
    "b" : bClass,
    "c" : cClass
}

print(originalDict)
for key in originalDict:
    print(originalDict[key].num)

originalDict["a2"] = aClass

print(originalDict)
for key in originalDict:
    print(originalDict[key].num)

originalDict["a2"].num = 2

print(originalDict)
for key in originalDict:
    print(originalDict[key].num)

print(originalDict["a"] == originalDict["a2"])
print(originalDict["a"] == originalDict["b"])
print(originalDict["b"] == originalDict["a2"])

print(originalDict["a"].num == originalDict["b"].num)
print(originalDict["b"].num == originalDict["a2"].num)