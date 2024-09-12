# Elite Journal Reader - Python

This project is an experiment into reading journal files from Elite Dangerous,
displaying relevent information, and live-updating as the journal file is
modified during play.

## Pseudocode information flow

1. `main` creates an instance of `FileMonitor`, and points it at the latest
   journal entry.
2. `FileMonitor` creates an instance of `JournalParser`, to
   parse each new line and return the data, and an instance of `JournalDisplay`,
   to display the data.
3. `main` commences the `FileMonitor`'s `monitor_file` method, which will load
   in the current contents of the journal file, and display the current
   up-to-date info. It will then periodically check for updates to the file, and
   update the display accordingly.