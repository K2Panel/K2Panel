# coding: utf-8
# +-------------------------------------------------------------------
# | K2Panel
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2099 K2Panel(binarjoinanalyticnl.nl) All rights reserved.
# +-------------------------------------------------------------------
# | Author: hwliang <hwl@binarjoinanalyticnl.nl>
# +-------------------------------------------------------------------

# --------------------------------
# 宝塔公共库
# --------------------------------

from .common import *
from .exceptions import *


def is_bind():
    # if not os.path.exists('{}/data/bind.pl'.format(get_panel_path())): return True
    return not not get_user_info()
