# Run Me!
# 1. Copy the code for Person, Parent and Child into a new file.
# 2. Change the code so everyone has a first name and a last name.
# 3. Ensure that everyone in the family has the same last name
# 4. Add a method to display the full name of the person.
# 5. Notice that when you set the spouse of a Parent, the spouse is also set as
#    the spouse of the spouse. So, you only have to set the spose for oe of them.
#    Make the 'parent' argument of Child work the same way: for each of the
#    parents of the child, ensure that the child is set as a child of the parent.
#    Then you can remove the '.ad_child' calls. 
# 6. Write a function, print_family, that takes just one parent, and prints out
#    the entire family.
class Person:
    """Person represents a person in our system."""

     # This is the initializer, it gets run when we create a new object
    def __init__(self, name: str, age: int):
        """Initializes a new Person object."""
        self.name = name
        self.age = age

    def say_hello(self, message: str):
        """Prints a greeting to the console."""
        print(f"Hello, my name is {self.name} and I am {self.age} years old. {message}")
        
        
class Parent(Person):
    """Parent represents a parent in our system."""

    def __init__(self, name: str, age: int, spouse=None):
        """Initializes a new Parent object."""
        super().__init__(name, age) # Call Person.__init__ to initialize the name and age attributes
        self.children = []
        
        # Set our spose but also set the spouse's spouse to us
        if spouse:
            self.spouse = spouse
            spouse.spouse = self
        
        self.spouse = None

    def add_child(self, child: Person):
        """Adds a child to the parent's list of children."""
        self.children.append(child)
        

    def say_hello(self, message: str):
        """Prints a greeting to the console."""
        
        super().say_hello(message)
        if self.spouse:
            print(f"My spouse is {self.spouse.name}")
            
        print(f"I have {len(self.children)} children.")

        if len(self.children) > 0:
            print("Their names are:")
            for child in self.children:
                print(f"  {child.name} {child.age}")
                
                
class Child(Person):
    """Child represents a child in our system."""

    def __init__(self, name: str, age: int, parents: list):
        """Initializes a new Child object."""
        super().__init__(name, age)  # Call Person.__init__ to initialize the name and age attributes
        self.parents = parents

    def say_hello(self, message: str):
        """Prints a greeting to the console."""
        super().say_hello(message)
        print(f"My parents are {', '.join([parent.name for parent in self.parents])}")
        
        
# Now lets make a family
mom = Parent("Alice", 35)
dad = Parent("Bob", 40, mom)

charlie = Child("Charlie", 10, [mom, dad])
dahlia = Child("Dahlia", 8, [mom, dad])

# Connect the children to the parents
mom.add_child(charlie)
mom.add_child(dahlia)
dad.add_child(charlie)
dad.add_child(dahlia)


mom.say_hello("Hello!") # Call the say_hello method of the mom object
print()
dahlia.say_hello("Yo!")