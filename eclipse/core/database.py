import redis
from eclipse import config

# Establish a connection to Redis with the password
db = redis.StrictRedis.from_url(config.REDIS_URI)

def get_value(keyword):
    try:
        return db.get(keyword)
    except redis.exceptions.RedisError as e:
        print(f"Error retrieving value for '{keyword}': {e}")
        return None

def add_value(keyword, json_data):
    try:
        return db.set(keyword, json_data)
    except redis.exceptions.RedisError as e:
        print(f"Error adding value for '{keyword}': {e}")
        return False

def del_value(keyword):
    try:
        return db.delete(keyword)
    except redis.exceptions.RedisError as e:
        print(f"Error deleting value for '{keyword}': {e}")
        return False

def get_values():
    try:
        keys = db.keys('*')
        return [db.get(key) for key in keys]
    except redis.exceptions.RedisError as e:
        print(f"Error retrieving values: {e}")
        return []

def get_value_list(keywords):
    try:
        # Use the pipeline feature to efficiently retrieve multiple values
        with db.pipeline() as pipe:
            # Queue the get operations for each keyword
            for keyword in keywords:
                pipe.get(keyword)
            # Execute the pipeline to retrieve values for all keywords
            values = pipe.execute()
        return values
    except redis.exceptions.RedisError as e:
        print(f"Error retrieving values for {keywords}: {e}")
        return []

