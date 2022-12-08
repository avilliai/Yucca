# -*- coding: utf-8 -*-
import time

import datetime
d1 = datetime.datetime.strptime('2022-12-05 15:12:54', '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime('2022-12-05 15:13:54', '%Y-%m-%d %H:%M:%S')
delta = d1 - d2
print(delta.seconds)

t = time.time()
print(int(t)-1670226402)
