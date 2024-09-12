import tkinter as tk
import json
from .bio_manager import BioManager
from .status import Status


class JournalDisplay:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(JournalDisplay, cls).__new__(cls, *args, **kwargs)
            print("Creating JournalDisplay")

        return cls._instance

    def __init__(self):
        self.root = tk.Tk()
        self.commander_label = tk.Label(self.root)
        self.commander_label.pack(anchor=tk.NW)
        self.ship_label = tk.Label(self.root)
        self.ship_label.pack(anchor=tk.NW)
        self.system_label = tk.Label(self.root)
        self.system_label.pack(anchor=tk.NW)
        self.is_odyssey_loaded = False

    def enable_odyssey(self):
        self.is_odyssey_loaded = True
        self.bio_manager = BioManager(self)

        # # dictionary of all discovered bio this session in this format:
        # #     system_body_id: {
        # #         body_name,
        # #         bio_total,
        # #         species_found {}
        # #     }
        # self.bio_planets_file_path = "data/bio/bio_planets.json"
        # with open(self.bio_planets_file_path, "r") as f:
        #     self.bio_planets = json.load(f)

        # # Periodically save bio_planets to a file
        # self.bio_planets_save_loop()

    def update_data(self, entry):
        if entry.get("event") == "LoadGame" and entry.get("Odyssey"):
            self.enable_odyssey()
        Status().set_attribute("commander", entry.get("Name"))
        Status().set_attribute("player_id", entry.get("FID"))
        self.commander_label["text"] = (
            f"CMDR {Status().commander} (FID: {Status().player_id})"
        )

        Status().set_attribute("ship_loc", entry.get("Ship_Localised"))
        Status().set_attribute("ship_name", entry.get("ShipName"))
        Status().set_attribute("ship_id", entry.get("ShipID"))
        Status().set_attribute("ship_ident", entry.get("ShipIdent"))
        self.ship_label["text"] = (
            f"{Status().ship_loc}: {Status().ship_name} {Status().ship_ident}"
        )

        Status().set_attribute("system_name", entry.get("StarSystem"))
        self.system_label["text"] = f"System: {Status().system_name}"

    def update_bio_data(self, entry):
        self.bio_manager.update_bio_data(entry)

    def update_commander_name(self, entry):
        Status().set_attribute("commander", entry.get("Name"))
        Status().set_attribute("player_id", entry.get("FID"))
        self.commander_label["text"] = (
            f"CMDR {Status().commander} (FID: {Status().player_id})"
        )

    def update_ship_info(self, entry):
        # self.ship_loc = entry.get("Ship_Localised", getattr(self, "ship_loc", None))
        Status().set_attribute("ship_loc", entry.get("Ship_Localised"))
        Status().set_attribute("ship_name", entry.get("ShipName"))
        Status().set_attribute("ship_id", entry.get("ShipID"))
        Status().set_attribute("ship_ident", entry.get("ShipIdent"))
        self.ship_label["text"] = (
            f"{Status().ship_loc}: {Status().ship_name} {Status().ship_ident}"
        )

    def update_system_info(self, entry):
        Status().set_attribute("system_name", entry.get("StarSystem"))
        self.system_label["text"] = f"System: {Status().system_name}"

    # def bio_planets_save_loop(self):
    #     # print("saving bio data")
    #     with open(self.bio_planets_file_path, "w", encoding="utf-8") as f:
    #         json.dump(self.bio_planets, f, ensure_ascii=False, indent=4)

    #     self.root.after(15000, self.bio_planets_save_loop)

    def run(self):
        self.root.mainloop()

    def set_attribute(self, attribute, value):

        setattr(
            self,
            attribute,
            value if value is not None else getattr(self, attribute, None),
        )
