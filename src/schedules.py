from apscheduler.schedulers.asyncio import (
    AsyncIOScheduler,
)

from date_features import (
    get_current_date,
    get_maximum_date,
)
from db import (
    get_users_data,
    update_user,

)

sched = AsyncIOScheduler({'apscheduler.timezone': 'Europe/Moscow'})


async def job_function():
    users = get_users_data()
    print('smthng')
    if users:
        for user in users:
            if user['expire_date'] < str(get_current_date()):
                fields = ['subs_type', 'subs_title', 'user_type', 'expire_date']
                values = ['null', 'null', 'new', f'{get_maximum_date()}']
                update_user(user['chat_id'], fields, values)


sched.add_job(job_function, trigger='cron', minute='1')
