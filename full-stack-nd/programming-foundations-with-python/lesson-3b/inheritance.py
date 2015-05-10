class Parent(object):
    def __init__(self, last_name, eye_color):
        print "parent constructor called"
        self.last_name = last_name
        self.eye_color = eye_color

    def show_info(self):
        print "Last name: " + self.last_name
        print "Eye color: " + self.eye_color

class Child(Parent):
    def __init__(self, last_name, eye_color, num_toys):
        print "child constructor called"
        Parent.__init__(self, last_name, eye_color)
        self.num_toys = num_toys

    def show_info(self):
        Parent.show_info(self)
        print "Number of toys: " + str(self.num_toys)

# po = Parent('Smith', 'blue')
# print po.last_name

po = Parent('Cyrus', 'blue')

co = Child('Cyrus', 'blue', 5)
co.show_info()
