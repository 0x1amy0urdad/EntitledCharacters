from bg3moddinglib import context

MOD_NAME = 'EntitledCharacters'
MOD_UUID = '6957a5e5-66fb-7399-13d2-150dcc08bb0f'
MOD_DISPLAY_NAME = 'Entitled Characters'
AUTHOR = 'Stan'
MOD_DESCRIPTION = "Characters are entitled to have titles."

MOD_DIR = MOD_NAME + '_' + MOD_UUID
MOD_PUBLISH_HANDLE = 5456950


def create_context(bg3_data_path: str | None = None) -> context:
    return context(MOD_NAME, MOD_UUID, "entitled_characters", bg3_data_path = bg3_data_path)
