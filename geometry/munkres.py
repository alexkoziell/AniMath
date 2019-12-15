import numpy as np

class MunkresAssignment():

    def __init__(self, pairWiseDist, N):
        
        self.N = N
        """
        STEP 1:
        Subtract minimum of every row from itself,
        likewise for every column.
        """        
        self.costMatrix = pairWiseDist # Abstract awaaaay 0_¬
        self.costMatrix = self.costMatrix - np.reshape(self.costMatrix.min(axis=1), (N, 1)) # subtract minimum of every row
        self.costMatrix = self.costMatrix - self.costMatrix.min(axis=0)                     # and minimum of every column
        print(self.costMatrix)

        """
        STEP 2:
        Find a minimal set of lines that cover all zeros.
        """
        self.coverZeros()

        """
        STEP 3:
        Create additional zeros if the number of covering lines
        is less than the desired number of pairs.
        """
        while self.numLines < N:
            self.createZeros()
            self.coverZeros()

        """
        STEP 4:
        Return an optimal pairing of row with column indices.
        """
        self.occupiedCols = [0] * N
        self.rowAssignment = [-1] * N # nonsense assignment to start
        print(self.assign(0))
        print(self.rowAssignment)
        




    def coverZeros(self):
        N = self.N
        costMatrix = self.costMatrix

        self.maxZeros = np.empty((N,N))
        maxZeros = self.maxZeros

        self.numLines = 0
        self.lines = np.zeros((N,N))
        lines = self.lines

        for n in range(N):
            for m in range(N):
                rowZeros = sum(x==0 for x in costMatrix[n,:])
                colZeros = sum(y==0 for y in costMatrix[:,m])
                maxZeros[n,m] = colZeros - rowZeros
        print(maxZeros)

        for n in range(N):
            for m in range(N):
                if costMatrix[n,m] == 0:
                    if lines[n,m] == 2: # colored twice already
                        pass
                    elif maxZeros[n,m] > 0 and lines[n,m] == 1: # correctly colored vertically
                        pass
                    elif maxZeros[n,m] < 0 and lines[n,m] == -1: # correctly colored horizontally
                        pass
                    else:
                        if maxZeros[n,m] > 0:
                            for i in range(N):
                                lines[i,m] = 2 if lines[i,m] == -1 or lines[i,m] == 2 else 1 # 2 for intersection cell
                        else:
                            for j in range(N):
                                lines[n,j] = 2 if lines[n,j] == 1 or lines[n,j] == 2 else -1
                        self.numLines += 1
        print(lines)
        print(self.numLines)

    def createZeros(self):
        N = self.N
        lines = self.lines
        
        # Find minimum uncovered value
        minUncoveredValue = 0
        for n in range(N):
            for m in range(N):
                if lines[n,m] == 0 and (self.costMatrix[n,m] < minUncoveredValue or minUncoveredValue == 0):
                    minUncoveredValue = self.costMatrix[n,m]

        # Subtract from all uncovered elements, and add to every doubly-colored elements
        for n in range(N):
            for m in range(N):
                if lines[n,m] == 0:
                    self.costMatrix[n,m] -= minUncoveredValue
                elif lines[n,m] == 2:
                    self.costMatrix[n,m] += minUncoveredValue
        print(self.costMatrix)

    def assign(self, row: int):
        if row == self.N-1:
            return True
        for col in range(self.N):
            if self.costMatrix[row,col] == 0 and self.occupiedCols[col] == 0:
                self.rowAssignment[row] = col
                self.occupiedCols[col] = 1
                if assign(row+1): # if the next rows are successfully assigned a row from each column
                    return True
                occupiedCols[col] = 0 # otherwise try a different column

            return False # if the row assignment failed, go back one row and try a different assignment.
