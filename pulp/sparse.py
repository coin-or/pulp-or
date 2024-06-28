# Sparse : Python basic dictionary sparse matrix

# Copyright (c) 2007, Stuart Mitchell (s.mitchell@auckland.ac.nz)
# $Id: sparse.py 1704 2007-12-20 21:56:14Z smit023 $

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
sparse this module provides basic pure python sparse matrix implementation
notably this allows the sparse matrix to be output in various formats
"""

from typing import TypeVar, Dict, List, Tuple, Any

_VT = TypeVar("_VT")


class Matrix(Dict[Tuple[int, int], _VT]):
    """This is a dictionary based sparse matrix class"""

    rows: List[int]
    cols: List[int]
    rowdict: Dict[int, Dict[Any, Any]]
    coldict: Dict[int, Dict[Any, Any]]

    def __init__(self, rows: List[int], cols: List[int]):
        """initialises the class by creating a matrix that will have the given
        rows and columns
        """
        self.rows = rows
        self.cols = cols
        self.rowdict = {row: {} for row in rows}
        self.coldict = {col: {} for col in cols}

    def add(
        self,
        row: int,
        col: int,
        item: _VT,
        colcheck: bool = False,
        rowcheck: bool = False,
    ):
        if not (rowcheck and row not in self.rows):
            if not (colcheck and col not in self.cols):
                self.__setitem__((row, col), item)
                self.rowdict[row][col] = item
                self.coldict[col][row] = item
            else:
                print(self.cols)
                raise RuntimeError(f"col {col} is not in the matrix columns")
        else:
            raise RuntimeError(f"row {row} is not in the matrix rows")

    def addcol(self, col: int, rowitems: Dict[int, _VT]):
        """adds a column"""
        if col in self.cols:
            for row, item in rowitems.items():
                self.add(row, col, item, colcheck=False)
        else:
            raise RuntimeError("col is not in the matrix columns")

    def get(self, k: Tuple[int, int], d: _VT) -> _VT:  # type: ignore
        return dict.get(self, k, d)  # type: ignore

    def col_based_arrays(
        self,
    ) -> Tuple[int, List[int], List[int], List[int], List[_VT]]:
        numEls = len(self)
        elemBase: List[_VT] = []
        startsBase: List[int] = []
        indBase: List[int] = []
        lenBase: List[int] = []
        for _, col in enumerate(self.cols):
            startsBase.append(len(elemBase))
            elemBase.extend(list(self.coldict[col].values()))
            indBase.extend(list(self.coldict[col].keys()))
            lenBase.append(len(elemBase) - startsBase[-1])
        startsBase.append(len(elemBase))
        return numEls, startsBase, lenBase, indBase, elemBase


if __name__ == "__main__":
    """unit test"""
    rows = list(range(10))
    cols = list(range(50, 60))
    mat: Matrix[str] = Matrix(rows, cols)
    mat.add(1, 52, "item")
    mat.add(2, 54, "stuff")
    print(mat.col_based_arrays())
