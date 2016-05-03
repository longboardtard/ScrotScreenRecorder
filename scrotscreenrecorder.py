from __future__ import print_function, division
from textwrap import dedent
from fabric.operations import prompt, local
from time import sleep, strftime
from os import getcwd, mkdir, chdir
from os.path import exists
__author__ = 'Richard Primera'
__email__ = "rprimera at urbe.edu.ve"
"""
Copyright 2014 Richard Primera

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the:
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""


class ScrotScreenRecorder(object):

    def __init__(self):
        self.quality = None
        self.interval = None
        self.percentage = None
        self.duration = None
        self.label = None
        self.workdir = None
        self.stop_requested = False

    def store_settings(self, quality, interval, label, percentage, duration, workdir):
        """
        This method allows you to register the settings within the instance object
        allowing the user to query the settings being used for the recording
        """
        self.quality = quality
        self.interval = interval
        self.percentage = percentage
        self.label = label
        self.duration = duration
        self.workdir = workdir

    def record(self, quality=75, interval=1, percentage=0, duration=None, label=None, workdir=getcwd()):
        """
        -quality: An integer in range 1-100
        -interval: Take a screenshot every 'interval' seconds
        -percentage: Percentage size of each accompanying thumbnail. Defaults to 0%
            meaning no thumbnails are generated
        -duration: Record for 'duration' seconds. Defaults to none
        -label: Folder label
        -workdir: Where to create folder 'label' to store captures. Defaults to
            cwd so you can either specify a different path in which to create
            the directory 'label', or leave blank and use the current one
        """
        date = strftime("%Y%m%d-%H%M%S")
        command = "/usr/bin/scrot --quality {} --thumb {}".format(quality, percentage)

        # Performing some checks
        if percentage <= 0 or percentage >= 100:
            print("No thumbnails will be generated")
            command = "/usr/bin/scrot --quality {}".format(quality)

        print("Setting up label")
        if label is None:
            label = "scrot-record-{}".format(date)
        else:
            label = "{}-{}".format(label, date)

        full_path = "{}/{}".format(workdir, label)

        if not exists(full_path):
            print("Path doesn't exist. Creating it...: {}".format(full_path))
            mkdir(full_path)
            chdir(full_path)

        if duration is None:
            print("No duration specified, defaulting to 60 seconds")
            duration = 60

        self.store_settings(quality, interval, percentage, duration, label, workdir)

        for k in xrange(0, int(duration*interval**-1), 1):
            if self.stop_requested:
                print("Stopped")
                break
            else:
                print("Screenshot {}".format(k))
                local(command)
                sleep(interval)

    def record_interactive(self):
        """Start recording by interactively initializing the variables"""
        quality = prompt("Quality [1-100]: ", default=75, validate=int)
        interval = prompt("Interval [seconds]: ", default=1, validate=float)
        percentage = prompt("Thumbnail percentage [%]: ", default=0, validate=int)
        duration = prompt("Duration [seconds]: ", default=60, validate=int)
        label = prompt("Label [folder-name]: ", default=None, validate=str)
        workdir = prompt("Workdir [alternative-parent-directory]: ", default=getcwd())

        self.record(quality, interval, percentage, duration, label, workdir)

    def stop(self):
        self.stop_requested = True


"""
Example usage:
a = ScrotScreenRecorder()
a.store_settings(quality=75, interval=1, percentage=0, duration=None, label=None, workdir=os.getcwd())
a.record_interactive()
a.stop()
"""
