import copy

class Matrix:
    def __init__(self, height, width, arr=[], fill=False):
        self.height = height
        self.width = width
        self.arr = arr
        if(len(arr) != self.height*self.width):
            if(not fill):
                raise ValueError("Not enough items in the matrix")
            for i in range(self.width*self.height-(len(arr))):
                self.arr.append(0)

    def get_i(self, y, x):
        return self.width*y + x

    def get_val(self, y, x):
        return self.arr[self.get_i(y,x)]

    def set_val(self, y, x, val):
        self.arr[self.get_i(y,x)] = val

    def print_out(self):
        print(str(self.height) + " x " + str(self.width))
        print("----")
        for y in range(self.height):
            output = ""
            for x in range(self.width):
                output += str(round(self.get_val(y,x),2))+", "
            print(output)
        print("----")

    def __add__(self, m2):
        if (not isinstance(m2, Matrix)):
            raise TypeError("Can only add two matricies together")
        if (not(self.width == m2.width and self.height == m2.height)):
            raise ValueError("Can only add matricies of same dimensions")
        sum_arr = []
        for i in range(len(self.arr)):
            sum_arr.append(self.arr[i] + m2.arr[i])
        return Matrix(self.height, self.width, sum_arr)

    def __iadd__(self,m2):
        return self + m2

    def __sub__(self, m2):
        if (not isinstance(m2, Matrix)):
            raise TypeError("Can only add two matricies together")
        if (not(self.width == m2.width and self.height == m2.height)):
            raise ValueError("Can only add matricies of same dimensions")
        sum_arr = []
        for i in range(len(self.arr)):
            sum_arr.append(self.arr[i] - m2.arr[i])
        return Matrix(self.height, self.width, sum_arr)

    def __isub__(self,m2):
        return self - m2

    def scale(self, s):
        scale_arr = []
        for i in range(len(self.arr)):
            scale_arr.append(self.arr[i]*s) 
        return Matrix(self.height, self.width, scale_arr)

    def multiply(self, m2):
        if (not isinstance(m2, Matrix)):
            raise TypeError("Can only multiply two matricies together")
        if(self.width != m2.height):
            raise ValueError("Can only multiply matricies with same column and row size")
        mult_arr = []
        for y in range(self.height):
            for x in range(m2.width):
                total = 0
                for i in range(self.width):
                    total += self.get_val(y, i) * m2.get_val(i, x)
                mult_arr.append(total)
        return Matrix(self.height, m2.width, mult_arr)

    def __neg__(self):
        return self.scale(-1)

    def __abs__(self):
        abs_arr = []
        for i in self.arr:
            abs_arr.append(abs(self.arr[i]))
        return Matrix(self.height, self.width, abs_arr)

    def __mul__(self, m2):
        if isinstance(m2, Matrix):
            return self.multiply(m2)
        else:
            return self.scale(m2)

    def __imul__(self, m2):
        return self * m2

    #returns identity matrix of diagonal length "size"
    @staticmethod
    def identity(size):
        arr = []
        for y in range(size):
            for x in range(size):
                if x == y:
                    arr.append(1)
                else:
                    arr.append(0)
        return Matrix(size, size, arr)

    def transpose(self):
        m = Matrix(self.width, self.height, [], True)
        for y in range(self.height):
            for x in range(self.width):
                m.set_val(x, y, self.get_val(y,x))
        return m

    #used for determining inverse
    def minor(self, row, column):
        arr = []
        for y in range(self.height):
            for x in range(self.width):
                if(x != column and y != row):
                    arr.append(self.get_val(y,x))
        if(len(arr) > 1):
            return Matrix(self.height-1, self.width-1, arr)
        elif(len(arr) == 1):
            return arr[0]

    def determinant(self):
        if(self.width != self.height):
            raise ValueError("Cannot find determinant of non square matrix")
        if(self.width == 2):
            return (self.get_val(0,0)*self.get_val(1,1)) - (self.get_val(0,1)*self.get_val(1,0))
        det_sum = 0
        sign = 1
        for x in range(self.width):
            det_sum += sign * self.get_val(0,x) * self.minor(0,x).determinant()
            sign *= -1
        return det_sum

    def cofactor(self,row,column):
        minor = self.minor(row, column)
        if(isinstance(minor, Matrix)):
            return minor.determinant() * (-1)**(row+column)
        return minor * (-1)**(row+column)

    def adjoint(self):
        arr = []
        for y in range(self.height):
            for x in range(self.width):
                arr.append(self.cofactor(y,x))
        return Matrix(self.height, self.width, arr).transpose()

    def inverse(self):
        if(self.width != self.height):
            raise ValueError("Cannot find determinant of non square matrix")
        if(self.width == 1):
            return Matrix(1, 1, [1/self.get_val(0,0)])
        det = self.determinant()
        if(det == 0):
            return None
        adj = self.adjoint()
        return (adj) * (1/float(det))

    def __truediv__(self, m2):
        if isinstance(m2, Matrix):
            inv = m2.inverse()
            if(inv):
                return self * inv
            return None
        else:
            return self.scale(float(1/m2))

    def __div__(self, m2):
        return self.__truediv__(m2)

    def __idiv__(self, m2):
        return self / m2

    def trace(self):
        if(self.width != self.height):
            raise ValueError("Cannot find trace of non square matrix")
        t = 0
        for x in range(self.width):
            t += self.get_val(x,x)
        return t

    #for testing
    def mult_by_inv(self):
        inv = self.inverse()
        if(inv):
            inv.print_out()
            (self*inv).print_out()
        else:
            print("det is 0")

    def __pow__(self, p:int):
        if(self.width != self.height):
            raise ValueError("Can only raise square matrix to power")
        if(p == 0):
            return Matrix.identity(self.width)
        if(p < 0):
            inv = self.inverse()
            if(inv):
                m = inv
                for i in range(abs(p)-1):
                    m *= inv
                return m
            return None
        m = self
        for i in range(p-1):
            m *= self
        return m

    def swap_rows(self,r1,r2):
        for x in range(self.width):
            i1 = self.get_i(r1, x)
            i2 = self.get_i(r2, x)
            self.arr[i1], self.arr[i2] = self.arr[i2], self.arr[i1]

    #taken from wikipedia page for rref
    def rref(self):
        reduced = copy.deepcopy(self)
        lead = 0
        for y in range(reduced.height):
            if reduced.width <= lead:
                return reduced
            i = y
            while reduced.get_val(i,lead) == 0:
                i += 1
                if i == reduced.height:
                    i = y
                    lead += 1
                    if reduced.width == lead:
                        return reduced

            if i != y:
                reduced.swap_rows(i, y)

            lv = float(reduced.get_val(y, lead))
            for x in range(reduced.width):
                index = reduced.get_i(y,x)
                reduced.arr[index] /= lv
            
            for i in range(reduced.height):
                if i != y:
                    lv = reduced.get_val(i,lead)
                    for x in range(reduced.width):
                        index = reduced.get_i(i, x)
                        reduced.arr[index] -= lv * reduced.get_val(y,x)
            lead += 1
        return reduced

    def get_row(self, r):
        row = []
        for x in range(self.width):
            row.append(self.get_val(r,x))
        return row

    def get_column(self, c):
        col = []
        for y in range(self.height):
            col.append(self.get_val(y,c))
        return col

    #takes in an augmented matrix representing a linear equation and does rref and then takes the last column and returns it as an array
    def solution(self):
        reduced = self.rref()
        return reduced.get_column(self.width-1)