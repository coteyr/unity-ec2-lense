import logging
import optparse
import yaml
import subprocess
import glob
from os.path import expanduser
from datetime import datetime, timedelta


import gettext
from gettext import gettext as _
gettext.textdomain('ec2-info')

from singlet.lens import SingleScopeLens, IconViewCategory, ListViewCategory

from ec2_info import ec2_infoconfig

class Ec2InfoLens(SingleScopeLens):

    class Meta:
        name = 'ec2_info'
        description = 'EC2 Info Lens'
        search_hint = 'Search EC2 Info'
        icon = 'ec2-info.svg'
        search_on_blank = True

    # TODO: Add your categories
    #example_category = ListViewCategory("Examples", 'help')
    running_hosts_category = ListViewCategory("Running Hosts", 'network-server')
    stopped_hosts_category = ListViewCategory("Stopped Hosts", 'dialog-error')
    home = expanduser("~")
    api_list = []
    last_update = datetime.now() - timedelta(days=7)  # the first time is out of date so lets force it.

    def search(self, search, results):
        if self.last_update < datetime.now() - timedelta(minutes=5):  # update evey 5 mins
            self.last_update = datetime.now()  # cheap caching
            del self.api_list[0:len(self.api_list)]
            for match in glob.glob("%s/.ec2-info/*.conf" % self.home):
                print("Getting New Data from AWS")
                p = subprocess.Popen(["aws", "din", "--yaml", "--secrets-file=%s" % match], shell=False, stdout=subprocess.PIPE)
                result = p.stdout.read()
                name = match[self.home.__len__() + 11:-5]
                self.api_list.append((name, result))

        for item in self.api_list:
            #
            name = item[0]
            result = yaml.load(item[1])
            for reservation in result['reservationSet']:
                #print(reservation['instancesSet'])
                for instance in reservation['instancesSet']:
                    #print(instance)
                    instanceID = instance["instanceId"]
                    instanceState = instance["instanceState"]["name"]
                    try:
                        instanceIP = instance["ipAddress"]
                    except:
                        instanceIP = "No IP"
                    try:
                        instancePIP = instance["privateIpAddress"]
                    except:
                        instancePIP = "No Private IP"
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
                            results.append(instanceIP,
                                 'network-server',
                                 self.running_hosts_category,
                                 "plain/text",
                                 "%s: %s" % (name, instanceName),
                                 "%s : %s" % (instanceID, instanceIP),
                                 instancePIP)
                        else:
                            results.append(instanceIP,
                                 'dialog-error',
                                 self.stopped_hosts_category,
                                 "plain/text",
                                 "%s: %s" % (name, instanceName),
                                 instanceID,
                                 instancePIP)
        pass

    def handle_uri(self, scope, uri):
        if uri != "No IP":
            subprocess.Popen(["gnome-terminal", "--window", "-e", "ssh %s" % uri])
        return self.hide_dash_response()
