# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 20:11:03 2023

@author: Anthony
"""
from copy import deepcopy
from itertools import product


def delta_filter(indices):
    "filtering the delta of indices"
    if len(indices) != 2:
        return False
    index_1, index_2 = indices
    return (index_1[0] + index_2[0] == 0 and
            index_1[1] + index_2[1] == 0)


INDICES_DELTA = list(product((-1, 0, 1), (-1, 0, 1)))
INDICES_PAIRS = set(filter(delta_filter, map(
    frozenset, product(INDICES_DELTA, INDICES_DELTA))))
LEN_TICTACTOE = 3
PLAYERS = {1: 'X', -1: 'O', 0: ' '}


def _number_to_string(turn):
    return PLAYERS[turn]


def _generate_tictactoe(coordinate):
    "return indices of tictactoe"
    ind_row, ind_col = coordinate
    indices_tictactoe = []
    for delta_1, delta_2 in INDICES_PAIRS:
        indices_tictactoe.append({
            coordinate,
            (ind_row + delta_1[0], ind_col + delta_1[1]),
            (ind_row + delta_2[0], ind_col + delta_2[1]),
        })
    return indices_tictactoe


class Node:
    """
    node of the game tree

    params
    ------
    data : nested list or None,
        the current status of board, giving None will return a empty borad
    turn : 1 or -1,
        the current player of this state
    parent : Node or None,
        the parent node of this node, None means a root node

    attributes
    ----------
    terminated : bool,
        whether this node is a terminal state
    winner : 1, 0 or -1,
        the winner of this state, 0 means no winners
    children : tuple of Node,
        child nodes of this node

    """

    def __init__(self, data=None, turn=1, parent=None):
        self._set_data(data)
        self.turn = turn
        self.parent = parent
        self.children = ()

        self.__get_coordinates()
        self.__check_winner()
        self.__check_terminated()
        self.__get_name()

    def _set_data(self, data):
        if data is None:
            data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.data = data

    @property
    def winner(self):
        "the winner of this state, 0 means no winners"
        return self.__winner

    @property
    def terminated(self):
        "whether this state is a terminal state"
        return self.__terminated

    def __repr__(self):
        return self._name

    def __hash__(self):
        return hash(self._name)

    def __get_name(self):
        self._name = '\n'.join([' '.join(map(_number_to_string, r))
                                for r in self.data]) + '\n'

    def __get_coordinates(self):
        self.coordinates = {}
        for ind_row, row in enumerate(self.data):
            for ind_col, element in enumerate(row):
                self.coordinates[element] = (
                    self.coordinates.get(element, set()) |
                    {(ind_row, ind_col)})

    def __check_winner(self):
        "check if there is a winner"
        self.__winner = 0
        for player, coordinates in self.coordinates.items():
            if player == 0:
                continue
            if len(coordinates) < LEN_TICTACTOE:
                continue
            for coordinate in coordinates:
                for ind_tictactoe in _generate_tictactoe(coordinate):
                    if len(ind_tictactoe & coordinates) == LEN_TICTACTOE:
                        self.__winner = player
                        return

    def __check_terminated(self):
        self.__terminated = False

        # tic-tac-toe!
        if self.winner:
            self.__terminated = True

        # board fulled
        else:
            for row in self.data:
                if 0 in row:
                    self.__terminated = False
                    return

    def expand(self):
        "get and return a tuple of child nodes"
        if self.terminated:
            self.children = ()
            return self.children

        children = []
        for ind_row, ind_col in self.coordinates.get(0, set()):
            data = deepcopy(self.data)
            data[ind_row][ind_col] = self.turn
            node = type(self)(data, -self.turn, parent=self)
            children.append(node)
        self.children = tuple(children)
        return self.children