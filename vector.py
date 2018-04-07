import sys
from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    ATTEMPTED_ZERO_DIVIDE = 'An attempt was made to divide by zero'
    ATTEMPTED_CROSS_PRODUCT_WO3DINPUTS = 'Cannot perform cross product without 3D input vectors'

    def __init__(self, coordinates):
        try: 
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')
    
    ## print coordinates
    def print(self):
        print ('coordinates: ')
        for x in self.coordinates:
            print(x)

    ## +, -, scalar multiply
    def plus(self, v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    ## magnitude, normalization
    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return Decimal(sqrt(sum(coordinates_squared)))

    def normalized(self):
        try:
            magnitude = self.magnitude();
            return self.times_scalar(Decimal('1.0')/magnitude)

        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
    
    def zero(self):
        return self.magnitude() == 0

    ## dot/inner product, get angle between 2 vectors (radians, degrees)
    @staticmethod
    def dot(first, second):
        result = 0
        if first.zero() or second.zero():
            result = 0
        else:
            #products = [one * two for one,two in zip(first.coordinates, second.coordinates)]
            #result = sum(products)
            result = sum([x*y for x,y in zip(first.coordinates, second.coordinates)])
        return result

    @staticmethod
    def angle_rads(first, second):
        try:
            #numerator = Vector.dot(first, second)
            #denominator = first.magnitude() * second.magnitude()
            u1 = first.normalized()
            u2 = second.normalized()
            dotted = Vector.dot(u1, u2)
            if (dotted <-1):
                error = abs(dotted-(-1))
                if (error < 0.00001):
                    dotted = -1
            elif (dotted > 1):
                error = dotted-1
                if error < 0.00001:
                    dotted = 1

            result = acos(dotted)

            #arg = numerator/denominator
            #result = acos(arg)
        except ZeroDivisionError:
            raise Exception(self.ATTEMPTED_ZERO_DIVIDE + ' in angle_rads()')
        return result
    
    @staticmethod
    def angle_degrees(first, second, tolerance=1e-10):
        result = Vector.angle_rads(first, second)
        return result * 180/pi # convert to degrees and return

    @staticmethod
    def orthagonal(first, second):
        result = False
        if first.zero() or second.zero():
            result = True
        else:
            result = abs(Vector.dot(first, second)) < tolerance
        return result
    
    @staticmethod
    def parallel(first, second): # return true if supplied vectors are parallel
        parallel = False
        if first.zero() or second.zero():
            parallel = True
        else:
            angle = Vector.angle_degrees(first, second)
            parallel = angle == 0 or angle == 180

        return parallel

    # projection functions
    @staticmethod 
    def v_parallel(v, b): # return the (2D?) projection of v onto b a.k.a. v"
        try:
            b_normalized = b.normalized()
            u = Vector.dot(v, b_normalized)
            return b_normalized.times_scalar(u)
        except Exception as e:
            if str(e) == self.CANNON_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLELL_COMPONENT_MSG)
            else:
                raise e

    @staticmethod
    def v_perp(v, b): # return the vector orthagonal to v" 
        try:
            vee = v
            return vee.minus(Vector.v_parallel(v, b))
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLELL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGANAL_COMPONENT_MSG)
            else:
                raise e

    # cross product, area of parallelogram defined by 2 vectors, area of triangle defined by 2 vectors
    @staticmethod
    def cross(v, w):
        # todo: assert v.dimension == 3 && w.dimension == 3
        a1 = v.coordinates[0]
        a2 = v.coordinates[1]
        a3 = v.coordinates[2]
        b1 = w.coordinates[0]
        b2 = w.coordinates[1]
        b3 = w.coordinates[2]
        x = a2 * b3 - a3 * b2
        y = a3 * b1 - a1 * b3
        z = a1 * b2 - a2 * b1
        return Vector([x,y,z])
    
    @staticmethod
    def area_of_parallellogram(v, w):
        return Vector.cross(v,w).magnitude()

    @staticmethod
    def area_of_triangle_with(v,w):
        return Vector.area_of_parallellogram()/Decimal ('2.0')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

def main():
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
    print ("#0, v cross w") # debug print template
    v = Vector(['1.0', '0.0', '0.0'])
    w = Vector(['0.0', '1.0', '0.0'])
    Vector.cross(v,w).print()

    print ("#1, v cross w") # debug print template
    v = Vector(['8.462', '7.893', '-8.187'])
    w = Vector(['6.984', '-5.975', '4.778'])
    Vector.cross(v,w).print()

    print ("#2 area of parallellogram spanned by v & w") # debug print template
    v = Vector(['-8.987', '-9.838', '5.031'])
    w = Vector(['-4.268', '-1.861', '-8.866'])
    print (Vector.cross(v,w).magnitude())

    print ("#3 area of triangle spanned by v & w") # debug print template
    v = Vector(['1.5', '9.547', '3.691'])
    w = Vector(['-6.007', '0.124', '5.772'])
    print (Decimal(0.5) * Vector.cross(v,w).magnitude())

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
    