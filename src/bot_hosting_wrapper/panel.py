import json
import requests


# https://control.bot-hosting.net/account/api
# max usage: 240 requests per minute
class Panel:
    def __init__(self, api_key, server_id=None):
        self.api_key = api_key
        self.server_id = server_id
        self.page = None
        self.urls = {
            "server_list": f"https://control.bot-hosting.net/api/client?page={self.page}"
        }

    def get_serverlist(self, page=1):
        self.page = page
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url=self.urls["server_list"], headers=headers)
        if response.status_code != 200:
            return f"Status code: {response.status_code} : {response.content}"
        data = json.loads(response.text)
        serverinfo = {}
        for server in data['data']:
            uuid = server['attributes']['uuid']
            identifier = server['attributes']['identifier']
            name = server['attributes']['name']
            serverinfo[uuid] = {'identifier': identifier, 'name': name}
            serverinfo[identifier] = {'uuid': uuid, 'name': name}
            serverinfo[name] = {'uuid': uuid, 'identifier': identifier}
        return serverinfo

    def get_server_uuid(self, identifier=None, name=None):
        if identifier is None and name is None:
            return "No provided Arguments!"
        findby = None
        if identifier is None:
            findby = "name"
        elif name is None:
            findby = "identifier"
        server_list = self.get_serverlist()
        if findby == "name":
            if name not in server_list:
                return None
            return server_list[name]['uuid']
        elif findby == "identifier":
            if identifier not in server_list:
                return None
            return server_list[identifier]['uuid']

    def get_server_identifier(self, uuid=None, name=None):
        if uuid is None and name is None:
            return "No provided arguments!"

        if uuid is not None:
            findby = "uuid"
        else:
            findby = "name"

        server_list = self.get_serverlist()

        if findby == "uuid":
            if uuid not in server_list:
                return None
            return server_list[uuid]['identifier']
        elif findby == "name":
            if name not in server_list:
                return None
            return server_list[name]['identifier']

    def get_server_name(self, uuid=None, identifier=None):
        if uuid is None and identifier is None:
            return "No provided arguments!"

        if uuid is not None:
            findby = "uuid"
        else:
            findby = "identifier"

        server_list = self.get_serverlist()

        if findby == "uuid":
            if uuid not in server_list:
                return None
            return server_list[uuid]['name']
        elif findby == "identifier":
            if identifier not in server_list:
                return None
            return server_list[identifier]['name']
    def get_directory(self, server_id=None, directory: str = None):
        if directory is None:
            directory = '%2F'

        self.server_id = server_id
        serverfiles_url = f"https://control.bot-hosting.net/api/client/servers/{self.server_id}/files/list?directory={directory}"
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "directory": directory
        }

        response = requests.get(url=serverfiles_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return f"{response.status_code} : {response.content}"
