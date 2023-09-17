import requests
from urllib.parse import quote


from config.definitions import OCTOPARSE_PWD, OCTOPARSE_USER

base_url = 'https://dataapi.octoparse.com/'

# Deprecated: api pricing too high


def get_access_token():
    data = {
        'username': OCTOPARSE_USER,
        'password': OCTOPARSE_PWD,
        'grant_type': 'password'
    }
    path = 'token'
    access_token_r = requests.post(base_url + path, data=data).json()
    return access_token_r.get('access_token')


def get_group_id(token):
    path = 'api/TaskGroup'
    r = requests.get(base_url + path, headers={'Authorization': 'bearer ' + token}).json()
    return r['data'][0].get('taskGroupId')


def get_task_ids(token, group_id):
    path = f'api/Task?taskGroupId={group_id}'
    r = requests.get(base_url + path, headers={'Authorization': 'bearer ' + token}).json()
    return r['data']


def get_task_status(token, task_ids):
    path = 'api/task/GetTaskStatusByIdList'
    task_ids_list = [el['taskId'] for el in task_ids]
    print(task_ids_list)
    data = {
      "taskIdList": task_ids_list
    }
    r = requests.post(base_url + path, data=data, headers={'Authorization': 'bearer ' + token}).json()
    return r


if __name__ == '__main__':
    access_token = get_access_token()
    group_id = get_group_id(access_token)
    task_ids = get_task_ids(access_token, group_id)
    task_statuses = get_task_status(access_token, task_ids)
    print(task_statuses)
    