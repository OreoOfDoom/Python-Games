# Run Me!

class Person:
    """Person represents a person in our system."""

     # This is the initializer, it gets run when we create a new object
    def __init__(a2, name: str, age: int):
        """Initializes a new Person object."""
        a2.name = name
        a2.age = age

    def say_hello(a2, message: str):
        """Prints a greeting to the console."""
        print(f"Hello, my name is {a2.name} and I am {a2.age} years old. {message}")
        
        
class Parent(Person):
    """Parent represents a parent in our system."""

    def __init__(a2, name: str, age: int, spouse=None):
        """Initializes a new Parent object."""
        super().__init__(name, age) # Call Person.__init__ to initialize the name and age attributes
        a2.children = []
        
        # Set our spose but also set the spouse's spouse to us
        if spouse:
            a2.spouse = spouse
            spouse.spouse = a2
        
        a2.spouse = None

    def add_child(a2, child: Person):
        """Adds a child to the parent's list of children."""
        a2.children.append(child)
        

    def say_hello(a2, message: str):
        """Prints a greeting to the console."""
        
        super().say_hello(message)
        if a2.spouse:
            print(f"My spouse is {a2.spouse.name}")
            
        print(f"I have {len(a2.children)} children.")

        if len(a2.children) > 0:
            print("Their names are:")
            for child in a2.children:
                print(f"  {child.name} {child.age}")
                
                
class Child(Person):
    """Child represents a child in our system."""

    def __init__(a2, name: str, age: int, parents: list):
        """Initializes a new Child object."""
        super().__init__(name, age)  # Call Person.__init__ to initialize the name and age attributes
        a2.parents = parents

    def say_hello(a2, message: str):
        """Prints a greeting to the console."""
        super().say_hello(message)
        print(f"My parents are {', '.join([parent.name for parent in a2.parents])}")
        
        
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