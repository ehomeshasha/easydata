#!/usr/bin/env python
import os, sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "easydata.settings")
    from django.core.management import execute_from_command_line
    import easydata.startup as startup
    startup.run()
    execute_from_command_line(sys.argv)
