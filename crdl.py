#!/usr/bin/python3

import json
import subprocess
import argparse

if __name__ == '__main__' :
    # Initialize the parser
    parser = argparse.ArgumentParser(
        description="Copr build results downloader tool"
    )

    # Commandline arguments
    parser.add_argument('--user_name', help='Username for fedora copr')
    parser.add_argument('--repo_name', help='Copr Repository name')
    parser.add_argument('--pkg_name', help="Name of the package")
    parser.add_argument('--build_id', help='Build Id')
    parser.add_argument('--chroot_name', help="Name of the chroot")

    args = parser.parse_args()

    # Repo url
    copr_result_url = "https://download.copr.fedorainfracloud.org/results"
    repo_url = copr_result_url+'/'+args.user_name+'/'+args.repo_name+'/'+args.chroot_name

    # Download result file
    resultsFile = "results.json"
    full_url = repo_url+'/'+args.build_id+'-'+args.pkg_name+'/'+resultsFile
    if subprocess.run(["wget", "--continue", full_url]).returncode != 0 :
                    raise SystemExit('Unable to download results.json file')
    
    # Download results
    with open(resultsFile,'r') as f :
        results = json.load(f)
        for pkg in results['packages'] :
            if not "debuginfo" in pkg['name'] :
                if pkg['arch'] != 'src' :
                    full_url = repo_url+'/'+args.build_id+'-'+args.pkg_name+'/'+pkg['name']+'-'+pkg['version']+'-'+pkg['release']+'.'+pkg['arch']+'.'+'rpm'
                    if subprocess.run(["wget", "--continue", full_url]).returncode != 0 :
                        break
