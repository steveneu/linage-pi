from decimal import Decimal, getcontext
from vector import Vector

getcontext().prec = 30

class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)
        self.set_basepoint()

    # instructor implementation for coincident
    # def __eq__(self, ell):
    #     if not self.is_parallel_to(ell):
    #         return False
    #     x0 = self.basepoint
    #     y0 = ell.basepoint
    #     basepoint_difference = x0.minus

    def __eq__(self, ell):

        if self.normal_vector.is_zero():
            if not ell.normal_vector.is_zero():
                return False
            else:
                diff = self.constant_term - ell.constant_term
                return MyDecimal(diff).is_near_zero()
        elif ell.normal_vector.is_zero():
            return False

        if not self.is_parallel_to(ell):
            return False
        x0=self.basepoint
        y0=ell.basepoint
        basepoint_difference = x0.minus(y0)

        n = self.normal_vector
        return basepoint_difference.is_orthogonal_to(n)

    def is_parallel_to(self, ell):
        n1 = self.normal_vector
        n2 = ell.normal_vector

        return n1.is_parallel_to(n2)

    def intersection_with(self, ell):
        try:
            A, B = self.normal_vector.coordinates
            C, D = ell.normal_vector.coordinates
            k1 = self.constant_term
            k2 = ell.constant_term

            x_numerator = D*k1 - B*k2
            y_numerator = -C*k1 + A*k2
            one_over_denom = Decimal('1')/(A*D - B*C)

            return Vector([x_numerator, y_numerator]).times_scalar(one_over_denom)

        except ZeroDivisionError:
            if self==ell:
                return self
            else:
                return None

    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/Decimal(initial_coefficient)
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    # return a point on line as a vector when x=1 and y=1
    def get_point_on_line(self):
        # solve for y when x=1
        y = (self.constant_term - Decimal(self.normal_vector[0]))/Decimal(self.normal_vector[1])
        return [1, y]

    def __str__(self):
        num_decimal_places = 3
        n = self.normal_vector

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output
        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                        for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    @staticmethod
    def parallel(first, second):
        v1 = Vector(first.normal_vector)
        v2 = Vector(second.normal_vector)
        return Vector.parallel(v1, v2)

    @staticmethod # return true if supplied lines are coincident (parallel & overlapping)
    def coincident(first, second):
        result = False
        parallel_lines = Line.parallel(first, second)
        if parallel_lines:
            # todo: handle lines that are vertical or horizontal (A=0 or B=0)
            ptline1 = first.get_point_on_line()
            ptline2 = second.get_point_on_line()
            if ptline1[0] == ptline2[0] and ptline1[1] == ptline2[1]:
                result = True
            else:
                v0 = Vector( [ptline2[0]-ptline1[0], ptline2[1]-ptline1[1]] )
                v1 = Vector(first.normal_vector)
                v2 = Vector(second.normal_vector)
                first_orthogonal = Vector.orthagonal(v0, v1)
                second_orthogonal = Vector.orthagonal(v0, v2)
                if first_orthogonal and second_orthogonal:
                    result = True
        else:
            result = parallel_lines
        return result

    @staticmethod
    def intersection(first, second):
        if not Line.parallel(first, second):
            A = Decimal(first.normal_vector[0])
            B = Decimal(first.normal_vector[1])
            k1 = first.constant_term
            C = Decimal(second.normal_vector[0])
            D = Decimal(second.normal_vector[1])
            k2 = second.constant_term
            x = (D*k1-B*k2)/(A*D-B*C)
            y = (-C*k1 + A*k2)/(A*D-B*C)
            return tuple([Decimal(x), Decimal(y)])
        else:
            return False

    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

    ## ..............................................................

def printLineInfo(one, two):
    message = "line one: " + str(one) + " and line two: " + str(two)
    if Line.parallel(one, two):
        if Line.coincident(one, two):
            message += " are coincident"
        else:
            message += " are parallel"
    else:
        result = Line.intersection(one, two)
        if result == False:
            message += " do not intersect"
        else:
            message += " intersect at: " + str(result)
    print(message)

def main():
    print("hello")
    # lesson 3, #7 - coding functions for planes

    # lesson 3, #4 - coding functions for lines
    # A_one = Line([4.046, 2.836], 1.21)
    # A_two = Line([10.115, 7.09], 3.025)
    # printLineInfo(A_one, A_two)
    #
    # B_one = Line([7.204, 3.182], 8.68)
    # B_two = Line([8.172, 4.114], 9.883)
    # printLineInfo(B_one, B_two)
    #
    # C_one = Line([1.182, 5.562], 6.744)
    # C_two = Line([1.773, 8.343], 9.525)
    # printLineInfo(C_one, C_two)

    # test for lesson 2 #10
    #vone = Vector(['-7.579', '-7.88'])
    #vtwo = Vector(['-2.029', '9.97', '4.172'])
    #vthree = Vector(['-2.328', '-7.284', '-1.214'])
    #vfour = Vector(['2.118', '4.827'])

    #wone = Vector(['22.737', '23.64'])
    #wtwo = Vector(['-9.231', '-6.639', '-7.245'])
    #wthree = Vector(['-1.821', '1.072', '-2.94'])
    #wfour = Vector(['0','0'])

    #onep = Vector.parallel(vone, wone)
    #oneo = Vector.orthagonal(vone, wone)

    #twop = Vector.parallel(vtwo, wtwo)
    #twoo = Vector.orthagonal(vtwo, wtwo)

    #threep = Vector.parallel(vthree, wthree)
    #threeo = Vector.orthagonal(vthree, wthree)    

    #fourp = Vector.parallel(vfour, wfour)
    #fouro = Vector.orthagonal(vfour, wfour)

    ## lesson 2 #12, projections
    #vone = Vector(['3.039', '1.879']);
    #bone = Vector(['0.825', '2.036']);

    #vtwo = Vector(['-9.88', '-3.264', '-8.159']);
    #btwo = Vector(['-2.155', '-9.353', '-9.473']);

    #vthree = Vector(['3.009', '-6.172', '3.692', '-2.51']);
    #bthree = Vector(['6.404', '-9.144', '2.759', '8.718']);

    #result1 = Vector.v_parallel(vone, bone);
    #result2 = Vector.v_perp(vtwo, btwo);
    
    #result3perp = Vector.v_parallel(vthree, bthree)
    #result3parallel = Vector.v_perp(vthree, bthree)

    #print(result1)
    #print(result2)
    #print(result3perp)
    #print(result3parallel)

    # lesson #2, Quiz: coding cross products
    #print ("#0, v cross w") # debug print template
    #v = Vector(['1.0', '0.0', '0.0'])
    #w = Vector(['0.0', '1.0', '0.0'])
    #Vector.cross(v,w).print()

    #print ("#1, v cross w") # debug print template
    #v = Vector(['8.462', '7.893', '-8.187'])
    #w = Vector(['6.984', '-5.975', '4.778'])
    #Vector.cross(v,w).print()

    #print ("#2 area of parallellogram spanned by v & w") # debug print template
    #v = Vector(['-8.987', '-9.838', '5.031'])
    #w = Vector(['-4.268', '-1.861', '-8.866'])
    #print (Vector.cross(v,w).magnitude())

    #print ("#3 area of triangle spanned by v & w") # debug print template
    #v = Vector(['1.5', '9.547', '3.691'])
    #w = Vector(['-6.007', '0.124', '5.772'])
    #print (Decimal(0.5) * Vector.cross(v,w).magnitude())

main()

    # lesson 2, #8
    #onev = Vector([7.887, 4.138])
    #onew = Vector([-8.802, 6.776])
    #print(Vector.dot(onev, onew))

    #twov = Vector([-5.955, -4.904, -1.874])
    #twow = Vector([-4.496, -8.755, 7.103])
    #print(Vector.dot(twov, twow))
    
    #threev = Vector([3.183, -7.627])
    #threew = Vector([-2.668, 5.319])
    #print(Vector.angle_rads(threev, threew))

    #fourv = Vector([7.35, 0.221, 5.188])
    #fourw = Vector([2.751, 8.259, 3.985])
    #print(Vector.angle_degrees(fourv, fourw))