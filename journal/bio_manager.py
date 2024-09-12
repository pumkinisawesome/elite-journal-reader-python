import json
import tkinter as tk
from .status import Status


class BioManager:
    def __init__(self, display):
        self.display = display
        self.root = display.root
        self.bio_label = tk.Label(self.root)
        self.bio_label.pack(anchor=tk.NW)

        self.colony_distance_by_genus = {
            "Aleoida": 150,
            "Bacterium": 500,
            "Cactoida": 300,
            "Clypeus": 150,
            "Concha": 150,
            "Electricae": 1000,
            "Fonticulua": 500,
            "Frutexa": 150,
            "Fumerola": 100,
            "Fungoida": 300,
            "Osseus": 800,
            "Recepta": 150,
            "Stratum": 500,
            "Tubus": 800,
            "Tussock": 200,
            "Crystalline Shards": 100,
            "Brain Tree": 100,
            "Anemone": 100,
            "Sinuous Tubers": 100,
            "Amphora Plant": 100,
            "Bark Mounds": 100,
        }

        self.english_genus_by_identifier = {
            "$Codex_Ent_Aleoids_Genus_Name;": "Aleoida",
            "$Codex_Ent_Bacterial_Genus_Name;": "Bacterium",
            "$Codex_Ent_Cactoid_Genus_Name;": "Cactoida",
            "$Codex_Ent_Clepeus_Genus_Name;;": "Clypeus",  # Fun misspelling of the identifier discovered in the journals
            "$Codex_Ent_Clypeus_Genus_Name;": "Clypeus",
            "$Codex_Ent_Conchas_Genus_Name;": "Concha",
            "$Codex_Ent_Electricae_Genus_Name;": "Electricae",
            "$Codex_Ent_Fonticulus_Genus_Name;": "Fonticulua",
            "$Codex_Ent_Shrubs_Genus_Name;": "Frutexa",
            "$Codex_Ent_Fumerolas_Genus_Name;": "Fumerola",
            "$Codex_Ent_Fungoids_Genus_Name;": "Fungoida",
            "$Codex_Ent_Osseus_Genus_Name;": "Osseus",
            "$Codex_Ent_Recepta_Genus_Name;": "Recepta",
            "$Codex_Ent_Stratum_Genus_Name;": "Stratum",
            "$Codex_Ent_Tubus_Genus_Name;": "Tubus",
            "$Codex_Ent_Tussocks_Genus_Name;": "Tussock",
            "$Codex_Ent_Ground_Struct_Ice_Name;": "Crystalline Shards",
            "$Codex_Ent_Brancae_Name;": "Brain Trees",
            "$Codex_Ent_Seed_Name;": "Brain Tree",  # Misspelling? :shrug: 'Seed' also seems to refer to peduncle thin.
            "$Codex_Ent_Sphere_Name;": "Anemone",
            "$Codex_Ent_Tube_Name;": "Sinuous Tubers",
            "$Codex_Ent_Vents_Name;": "Amphora Plant",
            "$Codex_Ent_Cone_Name;": "Bark Mounds",
        }

        # dictionary of all discovered bio this session in this format:
        #     system_body_id: {
        #         body_name,
        #         bio_total,
        #         species_found {}
        #     }
        self.bio_planets_file_path = "data/bio/bio_planets.json"
        with open(self.bio_planets_file_path, "r") as f:
            Status().bio_planets = json.load(f)

        # Periodically save bio_planets to a file
        self.bio_planets_save_loop()

    def bio_planets_save_loop(self):
        # print("saving bio data")
        with open(self.bio_planets_file_path, "w", encoding="utf-8") as f:
            json.dump(Status().bio_planets, f, ensure_ascii=False, indent=4)

        self.root.after(15000, self.bio_planets_save_loop)

    def update_bio_data(self, entry):
        if entry.get("event") == "SAASignalsFound":
            system_body_id = f"{entry.get('SystemAddress')}-{entry.get('BodyID')}"

            if system_body_id not in Status().bio_planets:
                bio_signals = [
                    signal
                    for signal in entry.get("Signals")
                    if signal.get("Type") == "$SAA_SignalType_Biological;"
                ]

                if bio_signals:
                    Status().bio_planets[system_body_id] = {
                        "body_name": entry.get("BodyName"),
                        "bio_total": len(bio_signals),
                        "species_found": {},
                    }

        elif entry.get("event") == "ScanOrganic":
            system_body_id = f"{entry.get('SystemAddress')}-{entry.get('BodyID')}"

            if system_body_id not in Status().bio_planets:
                # Unlikely to ever happen, but just in case, create a new planet entry
                Status().bio_planets[system_body_id] = {
                    "body_name": entry.get("BodyName"),
                    "bio_total": 0,
                    "species_found": [],
                }
            bio_planet = Status().bio_planets[system_body_id]
            if entry.get("Species_Localised"):
                if entry.get("ScanType") == "Log" or entry.get("ScanType") == "Sample":
                    if entry.get("Species_Localised") not in bio_planet.species_found:
                        bio_planet.species_found.append(
                            {
                                "genus": self.english_genus_by_identifier[
                                    entry.get(
                                        "Species_Localised",
                                        entry.get("Genus_Localised"),
                                    )
                                ],
                                "Analysed": False,
                            }
                        )
                elif entry.get("ScanType") == "Analyse":
                    if (
                        bio_planet.species_found[entry.get("Species_Localised")].get(
                            "Analysed"
                        )
                        == False
                    ):
                        bio_planet.species_found[entry.get("Species_Localised")].update(
                            {"Analysed": True}
                        )
                    self.reset_sampler_status()
        elif (
            entry.get("event") == "LeaveBody"
            or entry.get("event") == "FSDJump"
            or entry.get("event") == "Shutdown"
        ):
            self.reset_sampler_status()

    def reset_sampler_status(self):
        self.bio_label[
            "text"
        ] = f"""~~~ Bio Manager Status ~~~
Latitude:  {Status().get_attribute("latitude")}
Longitude: {Status().get_attribute("longitude")}
"""
        # print(self.bio_planets)
