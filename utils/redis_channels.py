import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)



def set_detection(username, camera, name_of_person):
    r.set(f"{username}:{camera}", name_of_person)

def get_detection(username, camera):
    result = r.get(f"{username}:{camera}")
    return result.decode('utf-8')

