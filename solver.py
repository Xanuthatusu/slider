#
# CS1410 Slider Puzzle Solver
# by Russ Ross
# March 2011
# 

import heapq

class SliderSolver:
    def __init__(self, size):
        self.size = size
        self.moves = []

    def is_goal(self, board, hole):
        if hole != self.size ** 2 - 1:
            return False
        for i in range(self.size ** 2 - 1):
            if board[i] != i:
                return False
        return True

    def score(self, board, hole, history):
        n = 0
        for i in range(self.size ** 2):
            if i != hole and board[i] != i:
                diffx = abs(i % self.size - board[i] % self.size)
                diffy = abs(i / self.size - board[i] / self.size)
                n += diffx ** 2 + diffy ** 2
        return n + len(history)

    def nextCandidate(self, board, hole, history, dx, dy):
        # compute the location of the new hole
        newhole = hole + dx + self.size * dy

        # perform the swap and compute the new board
        newboard = list(board)
        (newboard[hole], newboard[newhole]) = \
            (newboard[newhole], newboard[hole])
        newboard = tuple(newboard)

        # record the new history
        newhistory = list(history)
        newhistory.append(newhole)

        return (newboard, newhole, newhistory)

    def search(self, board, hole):
        board = tuple(board)

        # q stores: (score, board, hole, history = [move1, move2, ...])
        q = [(self.score(board, hole, []), board, hole, [])]
        depth = 0
        seen = set([board])

        while True:
            (priority, board, hole, history) = heapq.heappop(q)

            if self.is_goal(board, hole):
                print 'solution is', len(history), 'steps long'
                return history

            # generate new candidates
            for (dx, dy) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                (x, y) = (hole % self.size, hole / self.size)

                # only consider legal moves
                if 0 <= x + dx < self.size and 0 <= y + dy < self.size:
                    # generate the new candidate board
                    (newboard, newhole, newhistory) = \
                        self.nextCandidate(board, hole, history, dx, dy)

                    # ignore if we have seen this board before
                    if newboard not in seen:
                        seen.add(newboard)

                        # add it to the priority queue of candidates
                        heapq.heappush(q,
                                (self.score(newboard, newhole, newhistory),
                                 newboard, newhole, newhistory))

    # return the next move to make in solving the puzzle
    def solve(self, board, hole):
        if len(self.moves) == 0:
            # is the board already solved?
            if self.is_goal(board, hole):
                return None

            # get the list of moves leading to the solution
            self.moves = self.search(board, hole)

        return self.moves.pop(0)

    def reset(self):
        self.moves = []

if __name__ == '__main__':
    print 'This module should be loaded and used by slider.py'
