import aiohttp


# https://control.bot-hosting.net/account/api
# used api docs: https://dashflo.net/docs/api/pterodactyl/v1/
# max usage: 240 requests per minute
class Panel:
    def __init__(self, api_key, server_id=None):
        """
        Initialize Panel class.
        Args:
            api_key (str): Bot-Hosting.net API key (https://control.bot-hosting.net/account/api)
            server_id (str): Optional, server ID for which to retrieve resources. Defaults to None.
        """
        self.api_key = api_key
        self.server_id = server_id
        self.page = None
        self.urls = {
            "server_list": f"https://control.bot-hosting.net/api/client?page={self.page}",
            "permission_check": "https://control.bot-hosting.net/api/client/permissions",
            "account_check": "https://control.bot-hosting.net/api/client/account",
            "2fa": "https://control.bot-hosting.net/api/two-factor",
            "server_resources": f"https://control.bot-hosting.net/api/client/servers"
        }

    def _headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    async def get_serverlist(self, page=1):
        self.page = page
        url = self.urls["server_list"].format(self.page)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers(), timeout=6) as response:
                if response.status != 200:
                    return f"Status code: {response.status} : {await response.text()}"
                data = await response.json()
        
        serverinfo = {}
        for server in data['data']:
            uuid = server['attributes']['uuid']
            identifier = server['attributes']['identifier']
            name = server['attributes']['name']
            serverinfo[uuid] = {'identifier': identifier, 'name': name}
            serverinfo[identifier] = {'uuid': uuid, 'name': name}
            serverinfo[name] = {'uuid': uuid, 'identifier': identifier}

        return serverinfo


    async def get_server_uuid(self, identifier=None, name=None):
        if identifier is None and name is None:
            return "No provided Arguments!"
        findby = "name" if identifier is None else "identifier"
        server_list = await self.get_serverlist()
        if findby == "name":
            return server_list.get(name, {}).get('uuid')
        return server_list.get(identifier, {}).get('uuid')

    async def get_server_identifier(self, uuid=None, name=None):
            if uuid is None and name is None:
                return "No provided arguments!"
            findby = "uuid" if uuid else "name"
            server_list = await self.get_serverlist()
            key = uuid if findby == "uuid" else name
            return server_list.get(key, {}).get('identifier')

    async def get_server_name(self, uuid=None, identifier=None):
        if uuid is None and identifier is None:
            return "No provided arguments!"
        findby = "uuid" if uuid else "identifier"
        key = uuid if findby == "uuid" else identifier
        server_list = await self.get_serverlist()
        return server_list.get(key, {}).get('name')
        
    async def get_directory(self, server_id=None, directory: str = None):
        if directory is None:
            directory = '%2F'
        self.server_id = server_id
        url = f"https://control.bot-hosting.net/api/client/servers/{self.server_id}/files/list?directory={directory}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers(), timeout=6) as response:
                if response.status != 200:
                    return f"{response.status} : {await response.text()}"
                return await response.json()

    async def check_permissions(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.urls["permission_check"], headers=self._headers(), timeout=6) as response:
                if response.status != 200:
                    return f"{response.status} : {await response.text()}"
                return await response.json()

    async def check_account(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.urls["account_check"], headers=self._headers(), timeout=6) as response:
                if response.status != 200:
                    return f"{response.status} : {await response.text()}"
                return await response.json()
        
    async def get_2fa_code(self):
        """
        Generates a TOTP QR code image to allow the setup of 2FA
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.urls["2fa"], headers=self._headers(), timeout=6) as response:
                if response.status != 200:
                    return f"{response.status} : {await response.text()}"
                return await response.json()

    async def enable_2fa(self, totp_code):
        """
        Enables TOTP 2FA by sending a POST request to the provided URL.
        
        Args:
            totp_code (str): The Time-based One-Time Password (TOTP) generated from GET /account/two-factor or the get_2fa_code function.
        
        Returns:
            dict or str: The JSON response if successful, or an error message with the status code and content.
        """
        body = {"code": totp_code}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.urls["2fa"], headers=self._headers(), json=body, timeout=6) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 400:
                    return f"Invalid TOTP Token: {await response.text()}"
                return f"{response.status} : {await response.text()}"

        
    async def disable_2fa(self, password):
        """
        Enables TOTP 2FA by sending a POST request to the provided URL.
        
        Args:
            password (str): Existing Password | there is no info on how to get it lol
        
        Returns:
            bool or dict: true if successful, or an error message with the status code and content.
        
        Info:
            There is currently no way to obtain the password from the panel.
        """
        body = {"password": password}
        async with aiohttp.ClientSession() as session:
            async with session.delete(self.urls["2fa"], headers=self._headers(), json=body, timeout=6) as response:
                if response.status == 200:
                    return True
                elif response.status == 400:
                    return f"BadRequestHttpException: {await response.text()}"
                return f"{response.status} : {await response.text()}"
    
    async def get_server_resources(self, server_id):
        """
        Retrieves the current resource usage of a specified server.

        Parameters:
        server_id (str): The unique identifier of the server. If not provided, the server_id attribute of the Panel instance will be used.

        Returns:
        dict: A dictionary containing the formatted resource usage information. If an error occurs, it returns a dictionary with an "Error" key set to True.

        The returned dictionary has the following structure:
        {
            "Memory MB": "Memory usage GB",
            "Memory GB": "Memory usage in MB",
            "Network Inbound": "Inbound network traffic in MB",
            "Network Outbound": "Outbound network traffic in MB",
            "Disk Usage MB": "Disk usage in MB",
            "Disk GB": "Disk usage in GB"
        }
        Every value inside of the dictionary is currently a string
        """
        if self.server_id is None and server_id is None:
            return "No server ID provided!"
        
        url = f"{self.urls['server_resources']}/{server_id}/resources"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers(), timeout=6) as response:
                if response.status != 200:
                    return {
                        "Error": True,
                        "status_code": f"{response.status}",
                        "message": await response.text()
                    }
                data = await response.json()

        resources = data['attributes']['resources']
        memory_mb = resources['memory_bytes'] / (1024 * 1024)
        memory_gb = memory_mb / 1024
        network_rx_mb = resources['network_rx_bytes'] / (1024 * 1024)
        network_tx_mb = resources['network_tx_bytes'] / (1024 * 1024)
        disk_mb = resources['disk_bytes'] / (1024 * 1024)
        disk_gb = disk_mb / 1024

        return {
            "Memory MB": f"{memory_mb:.2f}",
            "Memory GB": f"{memory_gb:.2f}",
            "Network Inbound": f"{network_rx_mb:.2f}",
            "Network Outbound": f"{network_tx_mb:.2f}",
            "Disk Usage MB": f"{disk_mb:.2f}",
            "Disk Usage GB": f"{disk_gb:.2f}"
        }