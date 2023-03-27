
def indexes(iterable, obj):
    result = []
    for index, elem in enumerate(iterable):
        if elem == obj:
            yield index
name = "abcabcabc"


res = indexes(name, "a")

print(res)