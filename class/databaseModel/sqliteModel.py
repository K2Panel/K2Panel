#coding: utf-8
#-------------------------------------------------------------------
# K2Panel
#-------------------------------------------------------------------
# Copyright (c) 2015-2099 K2Panel(binarjoinanalyticnl.nl) All rights reserved.
#-------------------------------------------------------------------
# Author: hwliang <hwl@binarjoinanalyticnl.nl>
#-------------------------------------------------------------------

#------------------------------
# sqlite模型
#------------------------------
import os,sys,re,json,shutil,psutil,time
from databaseModel.base import databaseBase
import public


class main(databaseBase):

    def get_list(self,args):

        return []