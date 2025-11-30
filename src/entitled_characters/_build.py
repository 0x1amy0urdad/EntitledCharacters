from __future__ import annotations


import os
import os.path
import sys

from . import context


from bg3moddinglib import bg3_modding_env, game_files, run_build_procedures

DUMMY_SIZE = 23456789
DUMMY_HASH = 'd0ac7015f1afd547fba98c2432c10868'

files: game_files
ctx: context.context

def get_game_files() -> game_files:
    global files
    return files

def get_mod_env() -> bg3_modding_env:
    global ctx
    return ctx.env

def get_resources_path(ctx: context.context) -> str:
    try:
        return getattr(sys, '_MEIPASS')
    except:
        return os.path.join(ctx.root_path, 'resources', 'entitled_characters')

def build_mod(
        mod_version: tuple[int, int, int, int],
        mod_name: str | None = None,
        mod_uuid: str | None = None,
        bg3_data_path: str | None = None
) -> None:
    global files, ctx
    ctx = context.create_context(mod_name = mod_name, mod_uuid = mod_uuid, bg3_data_path = bg3_data_path)
    files = ctx.files
    resources_path = get_resources_path(ctx)
    ctx.env.cleanup_output()

    files.create_meta_lsx(
        context.MOD_NAME,
        context.MOD_DISPLAY_NAME,
        context.MOD_DESCRIPTION,
        context.MOD_UUID,
        context.AUTHOR,
        context.MOD_PUBLISH_HANDLE,
        mod_version,
        DUMMY_SIZE,
        DUMMY_HASH)

    files.copy_mod_logo(resources_path, 'entitled_characters.png')
    files.copy_osiris_goals(os.path.join(resources_path, 'osiris'))
    run_build_procedures()
    files.build(verbose = True)
