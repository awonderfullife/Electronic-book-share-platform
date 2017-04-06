def wrap(n):
    from random import randint
    return {"name": "level" + str(n),
            "children": [
                {"name": "haha", "size": randint(1, 5)} if n == 0 else wrap(n - 1)
                for i in range(randint(1, 10))
                ]
            }

with open("test.json", "w") as f:
    from json import dumps
    f.write(dumps(wrap(3)))
