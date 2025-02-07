import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def notifications():
    pass

def detection(username, camera, name_of_person):
    r.publish(f"{username}:{camera}", name_of_person)

def get_detection(username, camera):
    return r.get(f"{username}:{camera}")