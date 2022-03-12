import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'library'))
import standard

def hello_world():
	print("hello, world")

hello_world()

print(2 + 4 + 3)

lst = ["one", "two", "three"]

print(standard.first(lst))
print(standard.rest(lst))
