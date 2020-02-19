class autoErr:
    __slots__ = ("val","err") # Root of all evil
    def __init__(self, val, err):
        self.val = val
        # INVARIANT: self.err >= 0
        self.err = abs(err)
    # Python has to ways to print a value:
    # str(x) calls __str__ if it exists, and is meant to be "pretty"
    # repr(x) calls __repr__ if it exists,
    #  and is supposed to be a valid expression for reproducing the value
    def __repr__(self):
        # Python f(ormat)-strings are nice
        # { ... } escapes an f-string, and puts in a value.
        return f"autoErr{(self.val,self.err)}"
    def __str__(self):
        return f"{self.val}±{self.err}"
    # Python uses "dunder methods" to implement operator overloading
    def __abs__(self):#abs(x) = x.__abs__
        return autoErr(abs(self.val), self.err)
    def __neg__(self): # (-x) = x.__neg__
        return autoErr(-self.val, self.err)
    def __add__(self, oth): # a+b = a.__add__(b)
        # I use this if pattern constantly to allow interaction with normal numbers
        if isinstance(oth, autoErr):
            return autoErr(self.val+oth.val, (self.err**2 + oth.err**2)**0.5)
        else:
            return autoErr(self.val+oth, self.err)
    def __sub__(self, oth): # a-b = a.__minus__(b)
        if isinstance(oth, autoErr):
            return autoErr(self.val-oth.val, (self.err**2 + oth.err**2)**0.5)
        else:
            return autoErr(self.val-oth, self.err)
    def __mul__(self, oth):  # a*b = a.__mul__(b)
        if isinstance(oth, autoErr):
            val = self.val * oth.val
            return autoErr(val, val*((self.err/self.val)**2 + (oth.err/oth.val)**2)**0.5)
        else:
            return autoErr(self.val*oth, abs(self.err*oth)) # abs to maintain invariant
    def __truediv__(self, oth): # a/b = a.__truediv__(b)
      # __div__ is deprecated, and exists purely for python 2 compatibility
        if isinstance(oth, autoErr):
            val = self.val / oth.val
            return autoErr(val, val*((self.err/self.val)**2 + (oth.err/oth.val)**2)**0.5)
        else:
            return autoErr(self.val/oth, abs(self.err/oth))
    def __pow__(self, oth): # a^b = a.__pow__(b)
        if isinstance(oth, autoErr):
            return NotImplemented
            # Let's not do this
            #l,u = oth.split()
            #l = self**l
            #u = self**u
            #ll, lu = l.split()
            #ul, uu = u.split()
            #return autoErr((uu+ll)/2, (uu-ll)/2)
        else:
            val = self.val**oth
            return autoErr(val, abs(val*oth*self.err/self.val))
    
    # When python tries to do a binary operation, such as a+b,
    # it checks both a.__add__(b) and b.__radd(a), and 
    # takes the first one to succeed.  This allows you to make
    # custom types compatible with a base type on both sides.
    # Otherwise, 2*autoErr(...) would be an error.
    
    def __radd__(self, oth): # a+b = b.__radd__(a)
        return self + oth
    def __rsub__(self, oth): # a-b = b.__rsub__(a)
        return -self + oth
    def __rmul__(self, oth): # a*b = b.__rmul__(a)
        return self * oth
    def __rtruediv__(self, oth): # a/b = b.__rtruediv__(a)
        return self**-1 * oth
    #def __rpow__(self, oth): 


    # These methods allow you to convert a autoErr into normal number types
    def __float__(self): # float(x) = x.__float__()
        return float(self.val)
    def __int__(self): # int(x) = x.__int__()
        return int(self.val)
    def __long__(self): # long(x) = x.__long__()
        return long(self.val)
    # The only non-dunder method, used for convenience
    def split(self):
        return (self.val - self.err, self.val + self.err)