"""
Veo 3 Storyboard Station
prompt_builder.py
"""
import config

# ==========================================================
# List
# ==========================================================

def normalize_list(value):

    if not value:
        return []

    if isinstance(value,list):
        return [str(item).strip() for item in value if str(item).strip()]

    value = str(value).replace("\n",",").replace(";",",")

    return [item.strip() for item in value.split(",") if item.strip()]


# ==========================================================
# Prompt
# ==========================================================

def replace_placeholder(prompt,index,asset_list):

    return prompt.replace(
        f"{{{index}}}",
        ", ".join(asset_list)
    )


def build_prompt(template,prompt_core,character_list,reference_list):

    prompt = template.replace(
        "{0}",
        prompt_core
    ) if template else prompt_core

    prompt = replace_placeholder(
        prompt,
        1,
        character_list
    )

    prompt = replace_placeholder(
        prompt,
        2,
        reference_list
    )

    return prompt.strip()


def build_filename(final_prompt):

    return final_prompt[:20].strip()