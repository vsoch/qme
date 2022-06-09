"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.utils.file import mkdir_p

import configparser
import logging
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))

bot = logging.getLogger("qme.main.config")


class Config:
    def __init__(self, config_dir=None, load=True):
        """Make sure the config file exists, along with the QueueMe Home.
        If it doesn't exist, create it. Return the full path to the config
        file to store with the Queue and load the config.
        """
        from qme.defaults import QME_HOME

        QME_HOME = config_dir or QME_HOME
        if not os.path.exists(QME_HOME):
            bot.info(f"Creating QueueMe home at {QME_HOME}.")
            mkdir_p(QME_HOME)

        # Configfile is based in QME_HOME
        self.configfile = os.path.join(QME_HOME, "config.ini")

        # If the config file doesn't exist, generate it
        if not os.path.exists(self.configfile):
            default_config = os.path.join(here, "config.ini")
            shutil.copyfile(default_config, self.configfile)

        # Load the config file if wanted
        if load and self.configfile:
            self.read()

    def get(self, section, key):
        """A wrapper to config.get to directly interact with the self.config"""
        return self.config.get(section, key)

    def update(self, section, key, value, save=False):
        """update client secrets will update the data structure for a particular
        authentication. This should only be used for a (quasi permanent) token
        or similar. The secrets file, if found, is updated and saved by default.
        """
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value

        # If save is true (to persist settings)
        if save:
            self.save()

    def save(self):
        """save configuration back to it's original file"""
        with open(self.configfile, "w") as configfile:
            self.config.write(configfile)

    def read(self, configfile=None):
        """read in configuration file. By default use self.configfile."""
        configfile = configfile or self.configfile
        config = configparser.ConfigParser()
        config.read(configfile)
        self.config = config
