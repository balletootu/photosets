#!/usr/bin/env python
# -*- coding: utf-8 -*-

import helper
import os

def main():
    for parent, dirnames, filenames in os.walk('/Users/eddie104/Documents/hongjie/photosets/imgs'):
        for dirname in dirnames:
            if '0baidu' in parent or '0error' in parent or '0upload' in parent or '0nas' in parent:
                continue
            if dirname.startswith('MetArt'):
                path = os.path.join(parent, dirname).replace(' ', '\ ')
                if os.path.exists('%s/aria2c.log' % path.replace('\ ', ' ')):
                    helper.runCmd('cd .. && mv %s /Users/eddie104/Documents/hongjie/photosets/imgs/0uploaded/MetArt/tmp.' % path, None)
                    continue
                print('start => %s' % path)
                helper.runCmd('cd %s && aria2c -i %s/url.txt' % (path, path))
                helper.runCmd('cd .. && mv %s /Users/eddie104/Documents/hongjie/photosets/imgs/0uploaded/MetArt/tmp/' % path, None)
                print('end => %s' % path)
if __name__ == '__main__':
    main()
