"""
==========================================================
Veo 3 Storyboard Station
scenario_runner.py
"""
import asyncio

import config
from function import build_scene, command_to_prompt
from google_flow import GoogleFlow
from network_monitor import NetworkMonitor
from asset_manager import AssetManager

_running = False


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
                command_to_prompt(scene["command"]),
                config.STATUS_RUNNING,
                "none"
            )
            await google.clear_prompt()

            command = scene["command"]
            command = asset.resolve_command(command)

            await google.input_prompt(command)

            await google.click_generate()

            asset_name = await network.wait_file_name()
            asset.add_asset(
                scene["scene_id"],
                asset_name
            )

            if asset_name is None:
                raise Exception("Generate timeout")

            ui.update_row_ui(
                scene["scene_id"],
                command_to_prompt(scene["command"]),
                config.STATUS_DONE,
                asset_name
            )
            await asyncio.sleep(config.GENERATE_WAIT_TIME)

        except Exception as e:

            print(e)

            ui.update_row_ui(
                scene["scene_id"],
                command_to_prompt(scene["command"]),
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