"""
==========================================================
Veo 3 Storyboard Station
google_flow.py
----------------------------------------------------------
Google Flow Controller
==========================================================
"""
import asyncio
from playwright.async_api import async_playwright
import config


class GoogleFlow:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.page = None
        self.output_id = None


# ==========================================================
# Browser
# ==========================================================

    async def connect(self):

        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.connect_over_cdp(
            config.CDP_URL
        )

        if not self.browser.contexts:
            raise RuntimeError("Không tìm thấy Browser Context.")

        pages = self.browser.contexts[0].pages

        self.page = None

        for page in pages:

            if (
                "flow" in page.url
                or "veo" in page.url
                or "labs.google" in page.url
            ):
                self.page = page
                break

        if self.page is None:
            self.page = pages[-1]

        print(f"Connected : {self.page.url}")

        self.page.on("response", self.handle_network_response)


    async def close(self):

        try:
            self.page.remove_listener(
                "response",
                self.handle_network_response
            )
        except Exception:
            pass

        if self.browser:
            await self.browser.close()

        if self.playwright:
            await self.playwright.stop()


# ==========================================================
# Network
# ==========================================================

    async def handle_network_response(self,response):

        if config.SELECTORS["api_asset_endpoint_keyword"] not in response.url:
            return

        try:

            if response.status != 200:
                return

            data = await response.json()

            self.output_id = (
                data.get("displayName")
                or data.get("asset",{}).get("displayName")
            )

        except Exception:
            pass


# ==========================================================
# Prompt
# ==========================================================

    async def clear_prompt(self):

        await self.page.click(
            config.SELECTORS["main_prompt_area"]
        )

        await self.page.keyboard.press("Control+A")

        await self.page.keyboard.press("Backspace")

        await asyncio.sleep(config.NORMAL_DELAY)


# ==========================================================
# Asset
# ==========================================================

    async def inject_assets(self,keyword_list):

        if not keyword_list:
            return

        if isinstance(keyword_list,list):
            keyword_list = ",".join(keyword_list)

        for keyword in keyword_list.split(","):

            keyword = keyword.strip()

            if not keyword:
                continue

            print(f"Inject : {keyword}")

            await self.page.keyboard.type("@")

            await asyncio.sleep(2)

            await self.page.keyboard.insert_text(keyword)

            await asyncio.sleep(config.LONG_DELAY)

            await self.page.keyboard.press("Tab")

            await asyncio.sleep(config.NORMAL_DELAY)

            await self.page.keyboard.press("Enter")

            await asyncio.sleep(config.SHORT_DELAY)

            await self.page.keyboard.press("Escape")

            await asyncio.sleep(config.SHORT_DELAY)

            await self.clear_prompt()


    async def inject_character(self,character_list):

        await self.inject_assets(
            character_list
        )


    async def inject_reference(self,reference_list):

        await self.inject_assets(
            reference_list
        )


# ==========================================================
# Generate
# ==========================================================

    async def input_prompt(self, final_prompt):
        print(final_prompt)

        try:
            # 1. Xác định ô nhập liệu dựa trên selector từ file cấu hình
            prompt_selector = config.SELECTORS["main_prompt_area"]

            # 2. Chờ cho đến khi ô nhập liệu xuất hiện và sẵn sàng trên màn hình
            await self.page.wait_for_selector(prompt_selector, state="visible", timeout=5000)

            # 3. Sử dụng hàm fill của đối tượng page để "dán" (paste) toàn bộ văn bản lập tức
            await self.page.fill(prompt_selector, final_prompt)

            # 4. Giữ lại khoảng dừng ngắn để giao diện kịp cập nhật dữ liệu
            await asyncio.sleep(config.NORMAL_DELAY)

        except Exception as e:
            print(f"Lỗi khi nhập prompt: {e}")

    async def click_generate(self):

        self.output_id = None

        await self.page.keyboard.press(
            "Control+Enter"
        )

        print("Generate")

