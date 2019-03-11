#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 14:27:05 2019

@author: gparkes
"""
import numpy as np
from . import utils


__all__ = ["init_ai_random","init_ai_random2", "init_ai_nearest","init_ai_nearest2",
           "ai_random", "ai_nearest", "ai_nearest_with_hp"]

############## AI FUNCTIONS ##############################

def init_ai_random(units):
    """
    Given a list of units, get each unit to randomly select an enemy.
    """
    republics = [u for u in units if (u.allegiance_int_ == 0) and u.alive_]
    ciss = [u for u in units if (u.allegiance_int_ == 1) and u.alive_]

    rng = np.random.choice(len(ciss), len(republics))
    for rnd,ru in zip(rng, republics):
        # select a unit from cis
        ru.target_ = ciss[rnd]
    rng = np.random.choice(len(republics), len(ciss))
    for rnd,cu in zip(rng, ciss):
        cu.target_ = republics[rnd]
    return


def init_ai_random2(army, allegiance):
    """
    Given an Allegiance vector, assign a unit to the selected unit (index)

    Returns an array
    """
    N = army.index_range_[1]-army.index_range_[0]
    # find targets based on any not matched to the selected unit.
    targets = np.argwhere(allegiance != allegiance[army.index_range_[0]]).T[0]
    return np.random.choice(targets, size=(N,))


def init_ai_nearest(units):
    """
    Given a list of units, get each unit to select the nearest enemy.
    """
    republics = [u for u in units if (u.allegiance_int_ == 0) and u.alive_]
    ciss = [u for u in units if (u.allegiance_int_ == 1) and u.alive_]

    # for each republic unit, calculate the magnitude from all other units, and assign.
    for r in republics:
        mags = [utils.magnitude(r.pos_ - u.pos_) for u in ciss]
        r.target_ = ciss[np.argmin(mags)]
    # repeat for CIS
    for c in ciss:
        mags = [utils.magnitude(c.pos_ - u.pos_) for u in republics]
        c.target_ = republics[np.argmin(mags)]
    return

def init_ai_nearest2(army, allegiance, pos):
    """
    Given an Allegiance vector, assign a unit to the selected unit
    based on euclidean distance (index)

    Returns an array
    """
    allg = allegiance[army.index_range_[0]]
    i,j = army.index_range_

    pass

    return


def ai_random(units, selected_unit):
    """
    This AI algorithm works by giving the 'selected_unit' a new target at random.
    """
    # assign a new target
    alive_enemies = [u for u in units if
                     (u.allegiance_int_ != selected_unit.allegiance_int_)
                     and (u.alive_)]
    # if this list is empty, return False, else return True
    if len(alive_enemies) > 0:
        # generate rng, select one
        selected_unit.target_ = alive_enemies[np.random.randint(len(alive_enemies))]
        return True
    else:
        return False


def ai_nearest(units, selected_unit):
    """
    This AI algorithm works by giving the 'selected_unit' a new target based solely
    on nearest location.
    """
    # assign from enemy pool
    alive_enemies = [u for u in units if
                     (u.allegiance_int_ != selected_unit.allegiance_int_)
                     and u.alive_]
    if len(alive_enemies) > 0:
        # calculate mag distances.
        mags = [utils.magnitude(selected_unit.pos_ - u.pos_) for u in alive_enemies]
        # choose min dist.
        selected_unit.target_ = alive_enemies[np.argmin(mags)]
        return True
    else:
        return False


def ai_nearest_with_hp(units, selected_unit):
    """
    This AI algorithm works by giving the 'selected_unit' a new target based
    on a balance between nearest location AND the lowest HP.
    """
    # assign from enemy pool
    alive_enemies = [u for u in units if
                     (u.allegiance_int_ != selected_unit.allegiance_int_)
                     and u.alive_]
    if len(alive_enemies) > 0:
        # calculate mag distances.
        mags = np.asarray([utils.magnitude(selected_unit.pos_ - u.pos_) for u in alive_enemies])
        # hps
        hps = np.asarray([u.curr_hp_ for u in alive_enemies])
        # optimize between magnitude and HP
        # choose min optimal.
        selected_unit.target_ = alive_enemies[np.argmin(mags + (.5*hps))]
        return True
    else:
        return False

