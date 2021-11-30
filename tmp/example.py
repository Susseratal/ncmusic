def f1(value, formatter):
    print("f1 says", formatter(value))


def this_formatter(some_string):
    return some_string.upper()


def that_formatter(some_string):
    return some_string.lower()



demo_string = "Hello World"
f1(demo_string, this_formatter)
f1(demo_string, that_formatter)


##############################################################################################################
#                                                                                                            #
#   Initialises X, Y and Z to 0 as default values, but other paramaters could be passed in if necessary      #
#   def __init__(self, x=0, y=0, z=0):                                                                       #
#       self.x = x                                                                                           #
#       self.y = y                                                                                           #
#       self.z = z                                                                                           #
#   Information about writing a class, btw. this is an initialiser. it would help if I wrote these things    #
#                                                                                                            #
##############################################################################################################

