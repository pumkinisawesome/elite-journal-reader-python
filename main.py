import sys
from journal import FileMonitor


def main():
    journal_directory = (
        "data/"
        if len(sys.argv) == 2 and sys.argv[1] == "debug"
        else "/Users/jamiebland/Library/Containers/com.isaacmarovitz.Whisky/Bottles/28D7A8F3-A0F3-4F3B-9207-9A8C7C7C7BCC/drive_c/users/crossover/Saved Games/Frontier Developments/Elite Dangerous/"
    )
    journal_reader = FileMonitor(journal_directory)
    journal_reader.start()


if __name__ == "__main__":
    main()
