from os import walk, path
from json import loads
from nptdms import TdmsFile

root = "/home/mettekou/Nextcloud/Documenten/references/work/tremec/ProdData/Solenoid_Loggings"

def parse_report(pseudo_json):
    for bench in path.join([root, ""]):
        for directory, directories, files in walk():
            with open()
