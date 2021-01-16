import shelve
import string
import random
import json

def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def main():
    emp = {
        "name":"user-name",
        "email":"test@abc.com",
        "pass":"123abc"
    }
    db = shelve.open('database','c')
    for i in range(10):
        db[id_generator(32)] = emp
        # db['emp'][str(i)] = "hola"

    credentials = {
        "email":"test@abc.com"
    }
    for k in db:
        # datastore = json.load(db[k])
        if(db[k].get("email") == credentials["email"]):
            print ("Account already exists")
            break


    print(len(db))
    

    # @param:k is the key
    for k in db:
        print(k)
        print(db[k])
    db.close()


main()