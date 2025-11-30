from __future__ import annotations

import json
import logging
import os
import sys
import traceback
import wx
import wx.lib.scrolledpanel as scrolled

from typing import cast

logger: logging.Logger

from entitled_characters import build_mod, get_mod_env, get_titles, override_title

# Configure logging once at app startup
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s [%(levelname)s] %(message)s',
    handlers = [
        logging.FileHandler('entitled_characters.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('entitled_characters')


APP_NAME = 'Entitled Characters Generator'

DESCRIPTIONS = {
    "EntitledCharacters_Shadowheart_Default": "Shadowheart's initial title",
    "EntitledCharacters_Shadowheart_Revealed": "Shadowheart's title after Tav learned about her worship",
    "EntitledCharacters_Shadowheart_Selunite": "Selunite Shadowheart's title",
    "EntitledCharacters_Shadowheart_DJ": "DJ Shadowheart's title",
    "EntitledCharacters_Shadowheart_MS": "Mother Superior Shadowheart's title",
    "EntitledCharacters_Durge_Default": "Dark Urge's initial title",
    "EntitledCharacters_Durge_Killed_Lover": "Dark Urge's title after they killed their lover",
    "EntitledCharacters_Durge_Slayer": "Dark Urge's title after they got the slayer form",
    "EntitledCharacters_Durge_Revealed": "Dark Urge's title after they learned about their past",
    "EntitledCharacters_Durge_Resist": "Dark Urge's title after they rejected Bhaal",
    "EntitledCharacters_Durge_Embrace": "Dark Urge's title after they accepted Bhaal",
    "EntitledCharacters_Astarion_Default": "Astarion's initial title",
    "EntitledCharacters_Astarion_Revealed": "Astarion's title after he revealed his nature",
    "EntitledCharacters_Astarion_SA": "Spawn Astarion's title",
    "EntitledCharacters_Astarion_AA": "Ascended Astarion's title",
    "EntitledCharacters_Laezel_Default": "Lae'zel's title if she is on Vlaakith path",
    "EntitledCharacters_Laezel_Orpheus": "Lae'zel's title if she is on Orpheus path",
    "EntitledCharacters_Wyll_Default": "Wyll's initial title",
    "EntitledCharacters_Wyll_Devil": "Wyll's title after Mizora turned him into a cambion",
    "EntitledCharacters_Wyll_Avernus": "Wyll's title after he decided to become the Blade of Avernus",
    "EntitledCharacters_Wyll_Duke": "Wyll's title after he decided to become the Grand Duke",
    "EntitledCharacters_Gale_Default": "Gale's initial title",
    "EntitledCharacters_Gale_Hunger": "Gale's title after he asked for a magical item",
    "EntitledCharacters_Gale_Revealed": "Gale's title after he explained what is the cause of his condition",
    "EntitledCharacters_Gale_Defused": "Gale's title after Elminster defused the nuke",
    "EntitledCharacters_Karlach_Default": "Karlach's initial title",
    "EntitledCharacters_Karlach_1stUpgrade": "Karlach's title after the 1st upgrade",
    "EntitledCharacters_Karlach_2ndUpgrade": "Karlach's title after the 2nd upgrade",
    "EntitledCharacters_Karlach_Illithid": "Karlach's title after she is turned into an illithid",
    "EntitledCharacters_Halsin_Default": "Halsin's initial title",
    "EntitledCharacters_Halsin_InParty": "Halsin's title after he forced himself into the party",
    "EntitledCharacters_Tav_Default": "Tav's initial title",
    "EntitledCharacters_Tav_PartneredWithShadowheart": "Tav's title if they are partnered with Shadowheart",
    "EntitledCharacters_Tav_WasPartneredWithShadowheart": "Tav's title if they broke up with Shadowheart",
    "EntitledCharacters_Tav_PartneredWithLaezel": "Tav's title if they are partnered with Lae'zel",
    "EntitledCharacters_Tav_WasPartneredWithLaezel": "Tav's title if they broke up with Lae'zel",
    "EntitledCharacters_Tav_PartneredWithAstarion": "Tav's title if they are partnered with Astarion",
    "EntitledCharacters_Tav_WasPartneredWithAstarion": "Tav's title if they broke up with Astarion",
    "EntitledCharacters_Tav_PartneredWithGale": "Tav's title if they are partnered with Gale",
    "EntitledCharacters_Tav_WasPartneredWithGale": "Tav's title if they broke up with Gale",
    "EntitledCharacters_Tav_PartneredWithWyll": "Tav's title if they are partnered with Wyll",
    "EntitledCharacters_Tav_WasPartneredWithWyll": "Tav's title if they broke up with Wyll",
    "EntitledCharacters_Tav_PartneredWithKarlach": "Tav's title if they are partnered with Karlach",
    "EntitledCharacters_Tav_WasPartneredWithKarlach": "Tav's title if they broke up with Karlach",
    "EntitledCharacters_Tav_PartneredWithMinthara": "Tav's title if they are partnered with Minthara",
    "EntitledCharacters_Tav_WasPartneredWithMinthara": "Tav's title if they broke up with Minthara",
    "EntitledCharacters_Tav_PartneredWithHalsin": "Tav's title if they are partnered with Halsin",
    "EntitledCharacters_Tav_WasPartneredWithHalsin": "Tav's title if they broke up with Halsin",
}


def find_bg3_bin_path() -> str | None:
    for env_var_name in ('ProgramFiles(x86)', 'ProgramW6432', 'ProgramFiles'):
        program_files_path = os.getenv(env_var_name)
        if program_files_path:
            logger.info(f'Program Files path = {program_files_path}')
            bg3_path = os.path.join(program_files_path, 'Steam', 'steamapps', 'common', 'Baldurs Gate 3', 'bin', 'bg3.exe')
            logger.info(f'Looking for BG3 at {bg3_path}')
            if os.path.isfile(bg3_path):
                logger.info(f'Successfully found BG3 at {bg3_path}')
                return bg3_path
    drives = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for drive in drives:
        steam_library_path = f'{drive}:\\SteamLibrary'
        if os.path.exists(steam_library_path):
            bg3_path = os.path.join(steam_library_path, 'steamapps', 'common', 'Baldurs Gate 3', 'bin', 'bg3.exe')
            if os.path.isdir(bg3_path):
                logger.info(f'Successfully found BG3 at {bg3_path}')
                return bg3_path
    logger.warning('Failed to locate BG3 location')
    return None

def find_bg3_appdata_path() -> str | None:
    local_appdata_path = os.getenv('LOCALAPPDATA')
    if local_appdata_path:
        bg3_appdata_path = os.path.join(local_appdata_path, 'Larian Studios', "Baldur's Gate 3")
        if os.path.isdir(bg3_appdata_path):
            logger.info(f'Successfully found BG3 app data at {bg3_appdata_path}')
            return bg3_appdata_path
    logger.warning('Failed to locate BG3 app data')
    return None

def open_bg3_exe(w: MainWindow) -> str:
    with wx.FileDialog(w, 'Locate bg3.exe on your PC', wildcard = 'bg3.exe|bg3.exe', style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as d:
        if d.ShowModal() == wx.ID_CANCEL:
            return ""
        return d.GetPath()

class config:
    __env_root_path: str = ""
    __bg3_exe_path: str = ""
    __bg3_appdata_path: str = ""
    __window_width: int = 640
    __window_height: int = 768

    def __init__(self) -> None:
        self.__bg3_exe_path = ""
        local_appdata_path = os.getenv('LOCALAPPDATA')
        if local_appdata_path:
            self.__env_root_path = os.path.join(local_appdata_path, 'entitled_characters')
        else:
            logger.warning(f'LOCALAPPDATA is not defined, will fall back to the current directory')
            self.__env_root_path = os.path.abspath(os.curdir)
        logger.info(f'Config file path: {self.config_file_path}')
        if self.config_exists:
            self.load_config()

    @property
    def env_root_path(self) -> str:
        return self.__env_root_path

    @property
    def bg3_exe_path(self) -> str:
        return self.__bg3_exe_path

    @bg3_exe_path.setter
    def bg3_exe_path(self, val: str) -> None:
        self.__bg3_exe_path = val

    @property
    def bg3_appdata_path(self) -> str:
        return self.__bg3_appdata_path

    @bg3_appdata_path.setter
    def bg3_appdata_path(self, val: str) -> None:
        self.__bg3_appdata_path = val

    @property
    def window_width(self) -> int:
        return self.__window_width

    @window_width.setter
    def window_width(self, val: int) -> None:
        self.__window_width = val

    @property
    def window_height(self) -> int:
        return self.__window_height

    @window_height.setter
    def window_height(self, val: int) -> None:
        self.__window_height = val

    @property
    def config_file_path(self) -> str:
        return os.path.join(self.__env_root_path, 'entitled_characters.json')

    @property
    def config_exists(self) -> bool:
        return self.config_file_path != "" and os.path.isfile(self.config_file_path)

    def load_config(self) -> None:
        with open(self.config_file_path, 'rt') as f:
            logger.info(f'Loading configuration from {self.config_file_path}')
            cfg = cast(dict, json.load(f))
            if 'bg3_exe_path' in cfg:
                self.__bg3_exe_path = cast(str, cfg['bg3_exe_path'])
                logger.info(f'Configuration: bg3_exe_path = {self.__bg3_exe_path}')
            if 'bg3_appdata_path' in cfg:
                self.__bg3_appdata_path = cast(str, cfg['bg3_appdata_path'])
                logger.info(f'Configuration: bg3_appdata_path = {self.__bg3_appdata_path}')
            if 'window_width' in cfg:
                self.__window_width = int(cfg['window_width'])
                logger.info(f'Configuration: window_width = {self.__window_width}')
            if 'window_height' in cfg:
                self.__window_height = int(cfg['window_height'])
                logger.info(f'Configuration: window_height = {self.__window_height}')

    def save_config(self) -> None:
        os.makedirs(os.path.dirname(self.config_file_path), exist_ok = True)
        with open(self.config_file_path, 'wt') as f:
            cfg = dict()
            if self.__bg3_exe_path:
                cfg['bg3_exe_path'] = self.__bg3_exe_path
            if self.__bg3_appdata_path:
                cfg['bg3_appdata_path'] = self.__bg3_appdata_path
            cfg['window_width'] = self.__window_width
            cfg['window_height'] = self.__window_height
            f.write(json.dumps(cfg))
            logger.info(f'Saved configuration to {self.config_file_path}')

class PleaseWait(wx.Frame):
    __panel: wx.Panel
    __sizer : wx.BoxSizer | None
    __status_label : wx.StaticText

    def __init__(self, parent: wx.Frame, message: str):
        super().__init__(
            parent,
            style = wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.STAY_ON_TOP | wx.NO_BORDER
        )
        
        # Main panel
        self.__panel = wx.Panel(self)
        self.__panel.SetBackgroundColour(wx.Colour(40, 40, 40))
        
        # Label for status text
        self.__status_label = wx.StaticText(self.__panel, label = message)
        self.__status_label.SetForegroundColour(wx.WHITE)
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.__status_label.SetFont(font)
        
        # Layout
        self.__sizer = wx.BoxSizer(wx.VERTICAL)
        self.__sizer.Add(self.__status_label, 0, wx.ALIGN_CENTER | wx.ALL, 50)
        
        self.__panel.SetSizer(self.__sizer)
        self.__sizer.Fit(self)

    def show(self) -> None:
        self.CentreOnParent()
        self.Show()
        
    def hide(self) -> None:
        self.Hide()

class MainWindow(wx.Frame):
    __app: wx.App
    __config: config
    __widgets: dict[str, wx.TextCtrl]
    __main_panel: scrolled.ScrolledPanel
    __main_sizer: wx.BoxSizer
    __button_id: int
    __please_wait: PleaseWait
    __bg3_data_path: str

    def __init__(self, cfg: config, app: wx.App, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(None, *args, **kwargs)

        self.__bg3_data_path = os.path.join(os.path.dirname(os.path.dirname(cfg.bg3_exe_path)), 'Data')
        logger.info(f'self.__bg3_data_path = {self.__bg3_data_path}')

        self.SetMinSize(wx.Size(640, 480))
        self.SetSize(cfg.window_width, cfg.window_height)
    
        self.__app = app
        self.__config = cfg
        self.__widgets = dict[int, str]()

        self.__main_panel = scrolled.ScrolledPanel(self, style = wx.BORDER_RAISED)
        self.__main_sizer = wx.BoxSizer(wx.VERTICAL)

        for title_key, title_value in get_titles().items():
            txt_ctl = wx.TextCtrl(self.__main_panel, value = title_value, style = wx.TE_PROCESS_ENTER)
            self.__widgets[title_key] = txt_ctl
            description = DESCRIPTIONS[title_key] if title_key in DESCRIPTIONS else title_key
            self.__main_sizer.Add(wx.StaticText(self.__main_panel, label = description), proportion = 1, flag = wx.EXPAND | wx.TOP, border = 10)
            self.__main_sizer.Add(txt_ctl, proportion = 1, flag = wx.EXPAND)
            self.__main_sizer.Add(wx.StaticLine(self.__main_panel))

        self.__button_id = wx.NewId()
        self.__main_sizer.Add(wx.Button(self.__main_panel, self.__button_id, label = 'Generate EntitledCharacters pak'), proportion = 1, flag = wx.CENTER | wx.TOP, border = 20)

        self.__main_panel.SetSizer(self.__main_sizer)
        self.__main_panel.SetupScrolling(False, True)

        self.__please_wait = PleaseWait(self, "Please wait...")

        self.Bind(wx.EVT_BUTTON, self.on_create_pak)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_create_pak(self, event: wx.CommandEvent) -> None:
        try:
            try:
                self.__please_wait.show()
                self.__app.Yield()
                self.__app.Yield()
                self.__app.Yield()

                titles = get_titles()
                for k in titles:
                    txt_ctl = self.__widgets[k]
                    title = txt_ctl.GetLineText(0)
                    if title != titles[k]:
                        override_title(k, title)
                        logger.info(f'override: {k} -> {title}')

                build_mod((1, 0, 0, 0), bg3_data_path = self.__bg3_data_path)
                self.__please_wait.hide()
                wx.MessageBox(f'Successfully finished building the pak file. Press OK to exit.', caption = APP_NAME, style = wx.ICON_INFORMATION | wx.OK | wx.CENTER, parent = self)
                os.startfile(get_mod_env().output_path)
            except BaseException as exc:
                self.__please_wait.hide()
                wx.MessageBox(f'Failed to build the pak file. Please check the log file for errors.', caption = APP_NAME, style = wx.ICON_HAND | wx.OK | wx.CENTER, parent = self)
                raise RuntimeError from exc
        finally:
            self.__please_wait.hide()
        self.Close()

    def on_size(self, event: wx.Event) -> None:
        self.__window_size = self.GetSize()
        self.__config.window_width = self.__window_size.width
        self.__config.window_height = self.__window_size.height
        event.Skip()

    def on_close(self, event: wx.Event) -> None:
        self.__config.save_config()
        event.Skip()


def main() -> int:
    app = wx.App()
    try:
        cfg = config()
        os.makedirs(cfg.env_root_path, exist_ok = True)
        os.chdir(cfg.env_root_path)
        with open('.mod.root', 'w') as f:
            f.write('.mod.root')

        if not os.path.exists(cfg.bg3_exe_path):
            p = find_bg3_bin_path()
            if p is not None:
                cfg.bg3_exe_path = p

        w = MainWindow(cfg, app, title = APP_NAME)

        if not os.path.exists(cfg.bg3_exe_path):
            cfg.bg3_exe_path = open_bg3_exe(w)

        cfg.save_config()

        w.Show()
        app.MainLoop()
    except:
        exc_str = traceback.format_exc()
        sys.stderr.write(exc_str)
        if logger is not None:
            logger.fatal(exc_str)
            logger.info(f'{APP_NAME} has crashed')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())