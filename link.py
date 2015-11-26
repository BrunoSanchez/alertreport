
""" Utils for linked lists in a OOP.
You might wonder why printList and printBackward are functions and not methods
in the Node class.
The reason is that we want to use None to represent the empty list and it is
not legal to invoke a method on None.
This limitation makes it awkward to write list-manipulating
code in a clean object-oriented style."""


class Node:
    def __init__(self, cargo=None, next=None):
        self.cargo = cargo
        self.next = next

    def __str__(self):
        return str(self.cargo)

    def printBackward(self):
        if self.next is not None:
            tail = self.next
            tail.printBackward()
        print self.cargo,


def printList(node):
    while node:
        print node,
        node = node.next
    print


def printBackward(list):
    if list is None:
        return
    head = list
    tail = list.next
    printBackward(tail)
    print head,


class LinkedList:
    def __init__(self):
        self.length = 0
        self.head = None

    def printBackward(self):
        print "[",
        if self.head is not None:
            self.head.printBackward()
        print "]",

    def addFirst(self, cargo):
        node = Node(cargo)
        node.next = self.head
        self.head = node
        self.length = self.length + 1

