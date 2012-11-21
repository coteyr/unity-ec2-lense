import logging
import optparse
import yaml
import subprocess
import glob

from os.path import expanduser
from datetime import datetime, timedelta


import locale
from locale import gettext as _
locale.textdomain('ec2-info')

from singlet.lens import SingleScopeLens, IconViewCategory, ListViewCategory

from ec2_info import ec2_infoconfig

class Ec2InfoLens(SingleScopeLens):

    class Meta:
        name = 'ec2_info'
        description = 'EC2 Info Lens'
        search_hint = 'Search EC2 Info'
        icon = 'ec2-info.svg'
        search_on_blank = True
    # I tried to use standard icons that made sense
    running_hosts_category = ListViewCategory("Running Hosts", 'network-server')
    stopped_hosts_category = ListViewCategory("Stopped Hosts", 'dialog-error')
    home = expanduser("~")  # perhaps not the best, but seems like it would work to get the home directory.
    api_list = []  # for storing api get results to not log the snot out of unity.
    last_update = datetime.now() - timedelta(days=7)  # the first time is out of date so lets force it.

    def search(self, search, results):
        if self.last_update < datetime.now() - timedelta(minutes=5):  # update evey 5 mins
            self.last_update = datetime.now()  # cheap caching
            del self.api_list[0:len(self.api_list)]  # clear refrences too, because I don't know what's happening behind the curtian
            for match in glob.glob("%s/.ec2-info/*.conf" % self.home):
                print("Getting New Data from AWS")
                p = subprocess.Popen(["aws", "din", "--yaml", "--secrets-file=%s" % match], shell=False, stdout=subprocess.PIPE)
                result = p.stdout.read()  # decided on this as the best method, but there is always communicate
                name = match[self.home.__len__() + 11:-5]  # name derived from config file
                self.api_list.append((name, result))

        for item in self.api_list:
            name = item[0]
            result = yaml.load(item[1])
            for reservation in result['reservationSet']:
                for instance in reservation['instancesSet']:
                    instanceID = instance["instanceId"]
                    instanceState = instance["instanceState"]["name"]
                    # These horrid try blocks are the best I could come up with. I could DRY it a bit, but honestly that
                    # seems like more problem then just doing this. It's important to note that were recursing the stored
                    # cached data instead of getting new data. This helps with quickly searching.
                    # Though the cache has to be read every time a key is pressed. I can't find a way around that
                    # using singlet
                    try:
                        instanceIP = instance["ipAddress"]
                    except:
                        instanceIP = "No IP"
                    try:
                        instancePIP = instance["privateIpAddress"]
                    except:
                        instancePIP = "No Private IP"
                    try:
                        instacePlatform = instance["platform"]
                    except:
                        instacePlatform = "linux"
                    try:
                        for tag in instance["tagSet"]:
                            if tag["key"] == "Name":
                                instanceName = tag["value"]
                    except:
                        instanceName = "Unknown"
                    if instanceName == None:
                        instanceName = "Unknown"
                    if search in instanceName or search in name:
                        if instanceState == "running":
                            results.append("%s:%s" % (instacePlatform, instanceIP),
                                 'network-server',
                                 self.running_hosts_category,
                                 "plain/text",
                                 "%s: %s" % (name, instanceName),
                                 "%s : %s" % (instanceID, instanceIP),
                                 instancePIP)
                        else:
                            results.append("%s:%s" % (instacePlatform, instanceIP),
                                 'dialog-error',
                                 self.stopped_hosts_category,
                                 "plain/text",
                                 "%s: %s" % (name, instanceName),
                                 instanceID,
                                 instancePIP)
        pass

    def handle_uri(self, scope, uri):
        # not a real URI but it works
        ip = uri.partition(':')[2]
        platform = uri.partition(':')[0]
        print(platform)
        print(ip)
        if ip != "No IP":  # skip the offline hosts
            if platform != "windows":
                subprocess.Popen(["gnome-terminal", "--window", "-e", "ssh %s" % ip])
            else:
                subprocess.Popen(["remmina", "-n", "-s", ip, "-t", "rdp"])
        return self.hide_dash_response()
