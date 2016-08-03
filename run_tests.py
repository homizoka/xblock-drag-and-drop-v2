#!/usr/bin/env python
"""
Run tests for the Drag and Drop V2 XBlock.

This script is required to run our selenium tests inside the xblock-sdk workbench
because the workbench SDK's settings file is not inside any python module.
"""

import logging
import os
import sys
import workbench

if __name__ == "__main__":
    # Find the location of the XBlock SDK. Note: it must be installed in development mode.
    # ('python setup.py develop' or 'pip install -e')
    xblock_sdk_dir = os.path.dirname(os.path.dirname(workbench.__file__))
    sys.path.append(xblock_sdk_dir)

    # Use the workbench settings file:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    # Configure a range of ports in case the default port of 8081 is in use
    os.environ.setdefault("DJANGO_LIVE_TEST_SERVER_ADDRESS", "localhost:8081-8099")

    # Silence too verbose Django logging
    logging.disable(logging.DEBUG)

    def disable_native_firefox_events(firefox_profile):
        """
        If using Firefox, patch bok_choy to use synthetic events, which are much more reliable
        See https://bugs.launchpad.net/selenium-simple-test/+bug/1242364
        """
        firefox_profile.native_events_enabled = False
    from bok_choy.browser import FIREFOX_PROFILE_CUSTOMIZERS
    FIREFOX_PROFILE_CUSTOMIZERS.append(disable_native_firefox_events)

    try:
        os.mkdir('var')
    except OSError:
        # The var dir may already exist.
        pass

    from django.core.management import execute_from_command_line
    args = sys.argv[1:]
    paths = [arg for arg in args if arg[0] != '-']
    if not paths:
        paths = ["tests/"]
    options = [arg for arg in args if arg not in paths]
    execute_from_command_line([sys.argv[0], "test"] + paths + options)
