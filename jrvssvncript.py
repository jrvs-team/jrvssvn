#!/usr/bin/env python

from src import check_branches as src_check_branches
from src import update_branches as src_update_branches
from src import checkout_branches as src_checkout_branches


def check_branches_validity():
    src_check_branches.check_svn_branches("c:/home", False)


def update_branches():
    src_update_branches.update_svn_branches("c:/home")


def checkout_branches():
    src_checkout_branches.checkout_svn_branches("c:/home")


def update_or_checkout_branches():
    pass


check_branches_validity()
# update_branches()
# checkout_branches()
