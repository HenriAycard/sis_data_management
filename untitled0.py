#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 11:08:12 2019

@author: henriaycard
"""
from readFile import readFile
test = readFile('test.csv')
test.read()
test.readMail(2)
test.readLinkedin(5)
test.readEtablissement(9)
test.numberByEtablissement()
test.createFileMail()