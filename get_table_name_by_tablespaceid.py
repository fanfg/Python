#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# author：fanfugui

import os
import sys
import operator

INNODB_PAGE_SIZE = 1024 * 16  # InnoDB Page 16K

def get_tabelspaceid_by_ibdfile(fil,tablespaceid):
    fil = file(fil, 'rb')
    table_name = fil.name.split('/')[-1].split('.')[0]
    page_count = os.path.getsize(fil.name) / (INNODB_PAGE_SIZE)
    page = fil.read(INNODB_PAGE_SIZE)
    #每个page的第34-37 4个字节标识tablespace_id
    table_spaceid=int(page[34:38].encode('hex'), 16)
    if tablespaceid==table_spaceid:
        print("{0} tablespaceid {1}".format(fil,table_spaceid))
        return True
    else:
        return False

if __name__ == "__main__":
    base_dir = "/opt/local/mysql/var"
    tablespaceid=int(sys.argv[1])
    print("looking for table_name by table_space_id {0}".format(tablespaceid))
    #遍历目录
    for list in os.listdir(base_dir):
        db_dir=base_dir+'/'+list
        if os.path.isdir(db_dir):
            g_file = os.walk(db_dir)
            files = next(g_file)[2]
            #遍历ibd文件
            for file_name in files:
                if file_name.endswith('ibd'):
                    if get_tabelspaceid_by_ibdfile(db_dir + '/' + file_name,tablespaceid):
                        sys.exit(0)
