
__author__ = 'Anisha'
import zipfile;
import sys
import os
import ansible.runner
import requests
import json

from ansible.playbook import PlayBook
from ansible.inventory import Inventory
from ansible import callbacks
from ansible import utils

zipfile_path= sys.argv[1]
proxy_server = sys.argv[2]
proxy_port = sys.argv[3]

def extract_files():
    fh = open(zipfile_path, 'rb')


    z = zipfile.ZipFile(fh)
    path = {"sample" : "sample"}

    for name in z.namelist():

        file_ext = os.path.splitext(os.path.basename(name))[1]
        print "-------------------------"
        if file_ext == ".yml":
            output_path = "ansible/"
            print output_path
            path ["playbook"] = output_path+name
            z.extract(name,output_path)
        elif os.path.basename(name) == "hosts":
            output_path = "ansible/"
            print output_path
            path ["hosts"] = output_path+name
            z.extract(name,output_path)
        else:
            print name
            z.extract(name)


    fh.close()
    return path


def runPlayBook(path):
    print path
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

    inven = Inventory(host_list=path["hosts"]);
    groups = inven.get_groups();
    for group in groups:
        # print group.get_variables()
        if group.name == "canary":
            hosts = inven.get_hosts(group.name)
            for host in hosts:
                host_ip = host.get_variables()['ansible_ssh_host']
                url = 'http://'+proxy_server+':'+proxy_port
                payload = {'host': host_ip}
                headers = {'content-type': 'application/json'}
                # data = json.dumps(payload)
                print payload
                print url
                # response = requests.post(url, data=payload, headers=headers)
                # print host_vars['ansible_ssh_host']


    pb = PlayBook(inventory=inven,playbook=path["playbook"],stats=stats,callbacks=playbook_cb,runner_callbacks=runner_cb,)
    pb.run()


def main():
    path = extract_files()
    print "yo"
    runPlayBook(path)

if __name__ == "__main__":
    main()
