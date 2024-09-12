import os
import time
import json
from .journal_display import JournalDisplay


class FileMonitor:
    def __init__(self, journal_directory):
        self.display = JournalDisplay()
        # self.parser = JournalParser()
        self.journal_directory = journal_directory
        self.set_latest_journal_file()
        self.journal_file = open(self.journal_file_path, "r")
        self.journal_last_modified_time = None
        self.file_position = 0

    def start(self):
        self.monitor_file()
        self.set_latest_journal_file()
        self.display.run()

    def monitor_file(self):
        current_time = os.path.getmtime(self.journal_file_path)
        if (
            self.journal_last_modified_time is None
            or current_time > self.journal_last_modified_time
        ):
            self.journal_last_modified_time = current_time
            self.update_journal_data()
        self.display.root.after(1000, self.monitor_file)

    def set_latest_journal_file(self):
        files = os.listdir(self.journal_directory)
        journal_files = [
            f for f in files if f.endswith(".log") and f.startswith("Journal.")
        ]
        # add path to files
        files = [os.path.join(self.journal_directory, f) for f in journal_files]
        new_journal_file_path = max(files, key=os.path.getctime)
        if (
            not hasattr(self, "journal_file_path")
            or self.journal_file_path != new_journal_file_path
        ):
            self.journal_file_path = new_journal_file_path
            self.journal_file = open(self.journal_file_path, "r")
            self.file_position = 0
            print(f"New journal file: {self.journal_file_path}")
        self.display.root.after(10000, self.set_latest_journal_file)

    def update_journal_data(self):
        self.journal_file.seek(self.file_position)
        new_data = [json.loads(line.rstrip()) for line in self.journal_file]

        for entry in new_data:
            entry_type = entry.get("event")
            if entry_type in [
                "Commander",
                "ClearSavedGame",
                "NewCommander",
                "Loadout",
                "LoadGame",
                "Location",
                "FSDJump",
                "Scan",
            ]:
                self.display.update_data(entry)

            if self.display.is_odyssey_loaded and entry_type in [
                "SAASignalsFound",
                "ScanOrganic",
                "LeaveBody",
                "FSDJump",
                "Shutdown",
            ]:
                self.display.update_bio_data(entry)
            # if (
            #     entry_type == "Commander"
            #     or entry_type == "ClearSavedGame"
            #     or entry_type == "NewCommander"
            # ):
            #     self.display.update_commander_name(entry)
            # if entry_type == "Loadout" or entry_type == "LoadGame":
            #     self.display.update_ship_info(entry)
            # if entry_type == "Location" or entry_type == "FSDJump":
            #     self.display.update_system_info(entry)

        self.file_position = self.journal_file.tell()
