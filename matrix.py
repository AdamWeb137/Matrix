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
                output += str(self.get_val(y,x))+", "
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
                m.set_val(y, x, self.get_val(x,y))
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

    #for finding inverse
    @staticmethod
    def adj_matrix(size):
        start_sign = 1
        output_arr = []
        for y in range(size):
            curr_sign = start_sign
            for x in range(size):
                output_arr.append(curr_sign)
                curr_sign *= -1
            start_sign *= -1
        return Matrix(size, size, output_arr)

    def inverse(self):
        if(self.width != self.height):
            raise ValueError("Cannot find determinant of non square matrix")
        if(self.width == 1):
            return Matrix(1, 1, [1/self.get_val(0,0)])
        det = self.determinant()
        if(det == 0):
            return None
        adj = self.adjoint()
        adj.print_out()
        return (adj) * (1/det)

    #for testing
    def mult_by_inv(self):
        inv = self.inverse()
        if(inv):
            inv.print_out()
            (self*inv).print_out()
