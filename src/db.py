from redis import (
    Redis,
)

from config_parser import (
    db_host,
    db_port,
)

red = Redis(
    host=db_host,
    port=db_port,
    db=2
)


def insert_data(instances):
    with red.pipeline() as pline:
        for inst_id, inst in instances.items():
            pline.hmset(inst_id, inst)
        pline.execute()
    red.bgsave()
    print(red.keys())


def check_exists(user_id):
    return red.exists(f'user:{user_id}')


def get_user(user_id):
    user = red.hgetall(f'user:{user_id}')
    converted_user = {}
    for key, value in user.items():
        converted_user[key.decode('utf-8')] = value.decode('utf-8')
    return converted_user


def update_user(user_id, fields, values):
    for field, value in zip(fields, values):
        red.hset(f'user:{user_id}', field, value)


def delete_field(user_id, fields):
    for field in fields:
        red.hdel(f'user:{user_id}', field)


def add_expired_field(user_id, fields, values):
    for field, value in zip(fields, values):
        red.set(f'user:{user_id}', field, value)


def get_users_data():
    result = []
    for key in red.keys():
        key = key.decode('utf-8')
        result.append(get_user(key.split(':')[1]))
    return result


def field_exists(user_id, field):
    return red.hexists(f'user:{user_id}', field)
# print(red.keys())