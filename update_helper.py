#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Update Helper

Handle tar.gz update files

requires utarfile module
>>> import upip
>>> upip.install('micropython-utarfile')

Create tar.gz file with this command
$ tar -c -b 4 -f tarFileName.tar.gz -v someTarFolder/
or use create_tar.sh

Micropython usage:
>>> import UpdateHelper
>>> name = 'folder.tar.gz'
>>> UpdateHelper.extract_tar(name=name)

Check extracted content:
>>> with open('/someTarFolder/some-file.txt', 'r') as f:
>>>     print(f.read())
"""

import os
import uos
import utarfile
import upip


class UpdateHelper(object):
    """docstring for UpdateHelper"""
    def __init__(self):
        pass

    @staticmethod
    def extract_tar(name: str, prefix: str = '/') -> None:
        # t is an iteration and can only be used once
        t = utarfile.TarFile(name=name)

        for i in t:
            # print(i, i.type, i.name, i.size)

            if i.type != utarfile.DIRTYPE:
                print("Extracting: {}".format(i.name))
                upip._makedirs(i.name)

                # https://github.com/micropython/micropython-lib/blob/3c383f6d2864a4b39bbe4ceb2ae8f29b519c9afe/micropython/upip/upip.py#L68
                f = t.extractfile(i)

                outfname = '/{}'.format(i.name)
                print('Saving {} as {}'.format(i.name, outfname))
                upip.save_file(outfname, f)

    def perform_update(update_file: str = 'update.tar.gz') -> bool:
        update_result = False

        if update_file in os.listdir('/'):
            UpdateHelper.extract_tar(name=update_file)

            # perform cleanup
            try:
                uos.remove(update_file)
                print('Removed: {}'.format(update_file))
                update_result = True
            except Exception as e:
                if e.errno != errno.ENOENT:
                    print('Error {} on file {}'.format(e, update_file))
                else:
                    print('Failed to remove {} becaus: {}'.
                          format(update_file, e))

        return update_result
