import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)



def detection(username, camera, name_of_person):
    r.publish(f"{username}:{camera}", name_of_person)

def get_detection(username, camera):
    return r.get(f"{username}:{camera}")

