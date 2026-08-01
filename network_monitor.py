"""
==========================================================
Veo 3 Storyboard Station
network_monitor.py
----------------------------------------------------------
Monitor Google Flow Network Response
==========================================================
"""

import asyncio

import config


class NetworkMonitor:

    def __init__(self):
        self.page = None
        self.asset_name = None

    async def attach(self, page):

        self.page = page
        self.page.on("response", self.on_response)

    async def on_response(self, response):

        try:
            if response.request.method != "POST":
                return

            if not any(
                    endpoint in response.url
                    for endpoint in config.NETWORK_ENDPOINTS.values()
            ):
                return

            data = await response.json()

            workflows = data.get("workflows")

            if not workflows:
                return

            metadata = workflows[0].get("metadata", {})

            self.asset_name = metadata.get("displayName")

            if self.asset_name:
                print(f"Asset Name : {self.asset_name}")

        except Exception as e:

            print(f"Network Error : {e}")

    async def wait_file_name(self, timeout=120):

        start = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - start < timeout:

            if self.asset_name:

                name = self.asset_name
                self.asset_name = None

                return name

            await asyncio.sleep(1)

        return None