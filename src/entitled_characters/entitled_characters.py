from __future__ import annotations

from ._build import get_game_files

import bg3moddinglib as bg3

_TITLES = {
    "EntitledCharacters_Shadowheart_Default": "Shadow-Eyed Maiden",
    "EntitledCharacters_Shadowheart_Revealed": "Cloistered Stray",
    "EntitledCharacters_Shadowheart_Selunite": "Gods' Favourite Princess",
    "EntitledCharacters_Shadowheart_DJ": "Lost Servant of Shar",
    "EntitledCharacters_Shadowheart_MS": "She Who Will Be Unclaimed",
    "EntitledCharacters_Durge_Default": "Haunted by Forgotten Past",
    "EntitledCharacters_Durge_Killed_Lover": "Love-Slayer",
    "EntitledCharacters_Durge_Slayer": "Slayer",
    "EntitledCharacters_Durge_Revealed": "Bhaalspawn",
    "EntitledCharacters_Durge_Resist": "Fate-Breaker",
    "EntitledCharacters_Durge_Embrace": "Self-Lost Slayer",
    "EntitledCharacters_Astarion_Default": "Silver-Tongued Rogue",
    "EntitledCharacters_Astarion_Revealed": "Sunwalking Vampire",
    "EntitledCharacters_Astarion_SA": "Truly Unbound",
    "EntitledCharacters_Astarion_AA": "Vampire Lord of Nothing Within",
    "EntitledCharacters_Laezel_Default": "Champion of the Lich Queen",
    "EntitledCharacters_Laezel_Orpheus": "Spark of Gith Rebellion",
    "EntitledCharacters_Wyll_Default": "Blade of Frontiers",
    "EntitledCharacters_Wyll_Devil": "Monster-Hunter of Frontiers",
    "EntitledCharacters_Wyll_Avernus": "Blade of Avernus",
    "EntitledCharacters_Wyll_Duke": "Proud Duke of Baldur's Gate",
    "EntitledCharacters_Gale_Default": "Prodigy of Waterdeep",
    "EntitledCharacters_Gale_Hunger": "Ailing Wizard",
    "EntitledCharacters_Gale_Revealed": "Bearer of Netherese Doom",
    "EntitledCharacters_Gale_Defused": "Mystra's Unwilling Martyr",
    "EntitledCharacters_Karlach_Default": "Heartfire Warrior",
    "EntitledCharacters_Karlach_1stUpgrade": "Tempered Warrior",
    "EntitledCharacters_Karlach_2ndUpgrade": "Warrior on Borrowed Time",
    "EntitledCharacters_Karlach_Illithid": "Snuffed Out Warrior",
    "EntitledCharacters_Halsin_Default": "Grove's Reluctant Keeper",
    "EntitledCharacters_Halsin_InParty": "Self-Invited Busybody",
    "EntitledCharacters_Tav_Default": "Protagonist of the Story",
    "EntitledCharacters_Tav_PartneredWithShadowheart": "Shadowhert's Beloved",
    "EntitledCharacters_Tav_WasPartneredWithShadowheart": "Shadowhert's Former Flame",
    "EntitledCharacters_Tav_PartneredWithLaezel": "Zhak Vo'n'ash Duj",
    "EntitledCharacters_Tav_WasPartneredWithLaezel": "Hshar'lak",
    "EntitledCharacters_Tav_PartneredWithAstarion": "Astarion's Emeregency Food Supply",
    "EntitledCharacters_Tav_WasPartneredWithAstarion": "Astarion's Priority Food Supply",
    "EntitledCharacters_Tav_PartneredWithGale": "Gale's Obsession",
    "EntitledCharacters_Tav_WasPartneredWithGale": "Gale's Former Obsession",
    "EntitledCharacters_Tav_PartneredWithWyll": "Wyll's Spouse-To-Be",
    "EntitledCharacters_Tav_WasPartneredWithWyll": "Wyll's Spouse-Not-To-Be",
    "EntitledCharacters_Tav_PartneredWithKarlach": "Karlach's Only Love",
    "EntitledCharacters_Tav_WasPartneredWithKarlach": "Karlach's Former Love",
    "EntitledCharacters_Tav_PartneredWithMinthara": "Minthara's Poison-Resistant Partner",
    "EntitledCharacters_Tav_WasPartneredWithMinthara": "Minthara's Not-So-Poison-Resistant Victim-To-Be",
    "EntitledCharacters_Tav_PartneredWithHalsin": "Beer Enjoyer",
    "EntitledCharacters_Tav_WasPartneredWithHalsin": "Beer Hater",
}

_TITLES_MAPPING = {
    "EntitledCharacters_Shadowheart_Default": "hb602610ag4885g4af2gb01dg444bd8332bae",
    "EntitledCharacters_Shadowheart_Revealed": "h356bb6cdgd2f4g4212gb697g30771c68d503",
    "EntitledCharacters_Shadowheart_Selunite": "h1e03cb60g4f6bg49f2g82a3g8bdf1f7634cf",
    "EntitledCharacters_Shadowheart_DJ": "hed286b7ag8364g40b0gb2b6g1260214f1bfb",
    "EntitledCharacters_Shadowheart_MS": "hf0076d7bg6a91g43e0g9c97g9156f185a0d9",
    "EntitledCharacters_Durge_Default": "h6b73fb8dg0c25g4dd2gb3c4g30197df2e3a9",
    "EntitledCharacters_Durge_Killed_Lover": "h8a47ace6g698fg467fg99c0ga86732fe0e6c",
    "EntitledCharacters_Durge_Slayer": "h8366a97bgb41bg474agba1dg79ed78ae366d",
    "EntitledCharacters_Durge_Revealed": "hf54846feg9d1ag44cbgaae4g6b1bf9bac66a",
    "EntitledCharacters_Durge_Resist": "h1b2d9d0eg092bg4a41ga32ag9f499f6e8541",
    "EntitledCharacters_Durge_Embrace": "h870806fbg043eg4e83g9046g0fd1f65635f1",
    "EntitledCharacters_Astarion_Default": "he594503ag9321g443bgab97gaa88b32e5880",
    "EntitledCharacters_Astarion_Revealed": "h270e744dg76a3g4d25g822dgdae5c1b43eea",
    "EntitledCharacters_Astarion_SA": "h02237406g80ecg4cc4ga37fg7471d497570d",
    "EntitledCharacters_Astarion_AA": "h0725f867gf66bg43f8ga175g171266c0abac",
    "EntitledCharacters_Laezel_Default": "h9e4390ceg6aa6g42dega84cg1883238c5196",
    "EntitledCharacters_Laezel_Orpheus": "h8682a8eege8e9g4075g9022gbb6db1c34f23",
    "EntitledCharacters_Wyll_Default": "hbe8f483egc17dg40a7g9bfegc0c7300092ac",
    "EntitledCharacters_Wyll_Devil": "h01de9db6ga8a4g45a2g85b1g4aec151e6dcd",
    "EntitledCharacters_Wyll_Avernus": "hf0671002g7be8g4169gb599g4201fb4f9863",
    "EntitledCharacters_Wyll_Duke": "h4d351649g4e86g4afeg8dd4g15f18b9481cd",
    "EntitledCharacters_Gale_Default": "hb335726fge32dg4c20ga95cg8a847ed94c74",
    "EntitledCharacters_Gale_Hunger": "h374dafb4gd487g451dg8b6dg44a02abe1934",
    "EntitledCharacters_Gale_Revealed": "h20fd2513g708dg4fb2gb586ged499eea5975",
    "EntitledCharacters_Gale_Defused": "he9348244g58e1g4510gaa5eg9ce16d88f6fb",
    "EntitledCharacters_Karlach_Default": "h96571c16g2352g401fg94beg61b8d23ac5d1",
    "EntitledCharacters_Karlach_1stUpgrade": "h48a28150g1ea3g4f6egad8bgd5a474c2e43c",
    "EntitledCharacters_Karlach_2ndUpgrade": "hf3fbe323g7578g4688gbe7bgb5a4fba9999d",
    "EntitledCharacters_Karlach_Illithid": "h78bf50ffg9941g4266g92b9g512de9d44202",
    "EntitledCharacters_Halsin_Default": "h77faec62g997eg4eebgb837g5af88b70fa23",
    "EntitledCharacters_Halsin_InParty": "hb16ae8aeg3b95g49dagb4fegdfcdb4c16a7e",
    "EntitledCharacters_Tav_Default": "he579eb91g0256g4befg8799g571b68ef703c",
    "EntitledCharacters_Tav_PartneredWithShadowheart": "he5d5ad2eg2e68g4571g97d5g13177f271b92",
    "EntitledCharacters_Tav_WasPartneredWithShadowheart": "ha4813386gcefcg4674g8653g491f1015e52e",
    "EntitledCharacters_Tav_PartneredWithLaezel": "h56907a1dg3695g485bg915bgc912a52c1f3e",
    "EntitledCharacters_Tav_WasPartneredWithLaezel": "hbc23c69eg1e7cg41cbgb82bgb7b45c30fa4a",
    "EntitledCharacters_Tav_PartneredWithAstarion": "h1934475dg706cg4511gb0d4g67e3f1ffbac3",
    "EntitledCharacters_Tav_WasPartneredWithAstarion": "h0810be71ge30cg4c56ga314gc4b1dbfecd06",
    "EntitledCharacters_Tav_PartneredWithGale": "h37947aa2g3d78g4c5dg9b76gdcef5ca4dcff",
    "EntitledCharacters_Tav_WasPartneredWithGale": "hcfb60bb0ga8bcg4c18gb630g7ec8108d3d7b",
    "EntitledCharacters_Tav_PartneredWithWyll": "he9b7a064g49abg4db6g80fag45700bdbbcb1",
    "EntitledCharacters_Tav_WasPartneredWithWyll": "h908706edgb270g412ag9059g494f61eb0f11",
    "EntitledCharacters_Tav_PartneredWithKarlach": "h9afc67b0gcc95g4709g943fg1df85040841c",
    "EntitledCharacters_Tav_WasPartneredWithKarlach": "h0c134f59gcb99g4f14ga412ge0c99d04d05d",
    "EntitledCharacters_Tav_PartneredWithMinthara": "h5fd5219eg6800g4a43g90cbg3fb7aee8fafe",
    "EntitledCharacters_Tav_WasPartneredWithMinthara": "h5e1d7838g5654g4860g864agca7087ca012a",
    "EntitledCharacters_Tav_PartneredWithHalsin": "h34aa1303g5dfdg4a6ag837cgbaf42f002f5a",
    "EntitledCharacters_Tav_WasPartneredWithHalsin": "h5ee85c96ge406g49bdg9b4egddb3482f33e0",
}

_TITLE_OVERRIDES = dict[str, str]()

def get_titles() -> dict[str, str]:
    return _TITLES.copy()

def override_title(title_key: str, title_value: str) -> None:
    _TITLE_OVERRIDES[title_key] = title_value

def get_title(title_key: str, default_value: str) -> str:
    if title_key in _TITLE_OVERRIDES:
        return _TITLE_OVERRIDES[title_key]
    return default_value

def create_titles() -> None:
    files = get_game_files()
    strings = bg3.string_keys.create_new(files, 'EntitledCharacters')

    for title_key, text_handle in _TITLES_MAPPING.items():
        strings.add_string_key(text_handle, title_key)

    content = dict[str, tuple[int, str]]()
    for title_key, title_val in _TITLES.items():
        handle = _TITLES_MAPPING[title_key]
        if title_key in _TITLE_OVERRIDES:
            content[handle] = (1, _TITLE_OVERRIDES[title_key])
        else:
            content[handle] = (1, title_val)

    loca = bg3.loca_object(files.add_new_file(files.get_loca_relative_path()))
    loca.add_lines(content)



bg3.add_build_procedure("create_titles", create_titles)
