import pandas as pd
import os
import re
from dataclasses import dataclass, field

@dataclass
class Config:
    name_mapping: dict
    max_message_length: int

def load_data(dir='raw_data'):
    content = ''
    for file in os.listdir(rf'{dir}'):
        content += open(rf'{dir}/{file}', 'r').read()
    return content

def stats(data):
    user_pattern = r'[AP]M - (\w+): ' 
    users = re.findall(user_pattern, data)
    u_users = set(users)
    n_users = {user: data.count(f'M - {user}: ') for user in u_users}
    m_users = {user: re.findall(f'M - {user}: (.*)', data) for user in u_users}
    
    print(f'{len(u_users)} users identified:')
    print(f'\n{sum(n_users.values())} total messages identified.')
    for i, user in enumerate(u_users):
        print(f'{i+1}. {user}')
        print(f'\t{n_users[user]} messages.')
        print(f'\t{(sum([len(m) for m in m_users[user]]) / n_users[user]):.2f} words/message average.')

def process_data(data, config):
    prefix_pattern = r'(\d+/\d+/\d+, \d+:\d+[^:-]+ - )'

    data = re.sub(prefix_pattern, '', data)
    for name in config.name_mapping:
        data = re.sub(rf'^({name}): ', config.name_mapping[name] + ': ', data, flags=re.MULTILINE)
    data = re.sub(rf'\n', ' ', data)
    for name in config.name_mapping.values():
        data = re.sub(rf'({name}): ', '\n'+name + ': ', data, flags=re.MULTILINE)
    data = ''.join(list(filter(lambda x: '<Media omitted>' not in x and len(x) < config.max_message_length, data.split('\n'))))
    return data

def store_data(data, dir='processed_data'):
    with open(rf'{dir}/processed_data.txt', 'w') as f:
        f.write(data)

if __name__ == '__main__':
    data = load_data()
    config = Config()
    stats(data)
    data = process_data(data, config)
    store_data(data)

