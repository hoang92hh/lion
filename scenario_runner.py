"""
==========================================================
Veo 3 Storyboard Station
scenario_runner.py
----------------------------------------------------------
==========================================================
"""
import asyncio

import config
from function import build_scene
from google_flow import GoogleFlow
from network_monitor import NetworkMonitor
from asset_manager import AssetManager

_running = False



# ==========================================================
# Scenario
# ==========================================================

async def run_scenario(ui,scenario_type):

    global _running
    _running = True

    google = GoogleFlow()
    network = NetworkMonitor()
    asset = AssetManager(scenario_type)

    await google.connect()
    await network.attach(google.page)


    scene_list = build_scene(scenario_type)

    for scene in scene_list:

        if not _running:
            break

        try:

            ui.update_row_ui(
                scene["scene_id"],
                scene["final_prompt"],
                config.STATUS_RUNNING,
                "none"
            )
            await google.clear_prompt()

            await google.inject_character(
                scene["character_list"]
            )

            # thay the reference-value tuong ung voi reference-key
            reference_list = asset.replace_reference(
                scene["reference_list"]
            )

            await google.inject_reference(
                reference_list
            )

            final_prompt = scene["final_prompt"]
            final_prompt = asset.replace_text(final_prompt)
            await google.input_prompt(final_prompt)

            await google.click_generate()

            asset_name = await network.wait_file_name()
            asset.add_asset(
                scene["scene_id"],
                asset_name
            )

            if asset_name is None:
                raise Exception("Generate timeout")

            print("asset_name :", asset_name)

            ui.update_row_ui(
                scene["scene_id"],
                scene["final_prompt"],
                config.STATUS_DONE,
                asset_name
            )
            await asyncio.sleep(config.LONG_DELAY)

        except Exception as e:

            print(e)

            ui.update_row_ui(
                scene["scene_id"],
                scene["final_prompt"],
                config.STATUS_ERROR,
                scene["file_name"]
            )

    await google.close()

    _running = False


# ==========================================================
# Stop
# ==========================================================

async def stop_scenario():

    global _running

    _running = False