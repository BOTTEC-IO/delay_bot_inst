import os

import yaml

abspath = os.path.dirname(os.path.abspath(__file__))
config = yaml.load(open(abspath + "/config.yml", 'r'), Loader=yaml.BaseLoader)

token = config['token']
group_id = int(config['group_id'])
server_key = config['key']
server = config['server']
ts = config['ts']
