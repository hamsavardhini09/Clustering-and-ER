# -*- coding: utf-8 -*-
"""
@author Hamsavardhini
"""
import os
import platform
import subprocess
import config
import shutil

def load_data(path):
    # clear_data_path()
    os.chdir(path)
    if platform.system() == 'Windows':
        loadQuery = "Neo4jImport.bat --into " + config.neo4j_data_Path + " --nodes surfaceform_uri.csv --nodes url.csv --nodes name.csv --relationships url_surfaceform_rel.csv,name_surfaceform_rel.csv --skip-duplicate-nodes true"
    elif platform.system() == 'Linux':
        loadQuery = "Neo4jImport.sh"

    p = subprocess.Popen(config.Neo4jPath + loadQuery, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    # print p.returncode

def clear_data_path():
    shutil.rmtree(config.neo4j_data_Path)

load_data("E:\JSON_results\Dheepan")