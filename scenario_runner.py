"""
==========================================================
Veo 3 Storyboard Station
scenario_runner.py
----------------------------------------------------------
==========================================================
"""
import config
from function import build_scene
from google_flow import GoogleFlow

_running = False


# ==========================================================
# Scenario
# ==========================================================

async def run_scenario(ui,scenario_type):

    global _running

    _running = True

    google = GoogleFlow()

    await google.connect()

    scene_list = build_scene(scenario_type)

    for scene in scene_list:

        if not _running:
            break

        try:

            ui.update_row_ui(
                scene["scene_id"],
                config.STATUS_RUNNING,
                scene["file_name"]
            )

            await google.clear_prompt()

            await google.inject_character(
                scene["character_list"]
            )

            await google.inject_reference(
                scene["reference_list"]
            )

            await google.input_prompt(
                scene["final_prompt"]
            )

            await google.click_generate()

            output_id = await google.wait_generate_finish()

            scene["output_id"] = output_id

            ui.update_row_ui(
                scene["scene_id"],
                config.STATUS_DONE,
                scene["file_name"]
            )

        except Exception as e:

            print(e)

            ui.update_row_ui(
                scene["scene_id"],
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