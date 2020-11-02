#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 21:06:47 2020

@author: zorozed
"""
# In[setOfStacks]

class setOfStacks:
    def __init__(self, size):
        self.size = size
        self.arr = []
        self.nStack = 0
    def push(self, value):
        if self.nStack==0:
            self.arr.append([value])
            self.nStack += 1
        else:
            currentStack = self.nStack-1
            if len(self.arr[currentStack])==self.size:
                self.arr.append([value])
                self.nStack += 1
            else:
                self.arr[currentStack].append(value)
    def pop(self):
        if self.nStack==0:
            return False

        value = self.arr[self.nStack-1].pop()
        if len(self.arr[self.nStack-1])==0:
            self.nStack -= 1
            self.arr.pop()
            
        return value
    
    def popAt(self, index):
        if index >= self.nStack or index < 0:
            return -100000000
        
        return self.arr[index].pop()
        
    def printStack(self):
        print(self.arr)

s = setOfStacks(3)
s.push(1)
s.push(2)
s.push(3)
s.push(4)
s.push(5)
s.push(6)
s.push(7)
s.push(8)
s.push(9)
# In[Queue via Stacks]:


class MyQueue:
    def __init__(self):
        self.stack_1 = []
        self.stack_2 = []
    
    def push(self, value):
        self.stack_1.append(value)
    
    def front(self):
        if len(self.stack_2)==0:
            while len(self.stack_1) != 0:
                self.stack_2.append(self.stack_1.pop())
        if len(self.stack_2)==0:
            return -100000000000000
        return self.stack_2.pop()
    
# In[sort a stack ]:
        
class sortedStack:
    def __init__(self, arr):
        self.s1 = arr
        self.s2 = []
        
    def sort(self):
        while len(self.s1) > 0:
            
            ns1 = len(self.s1)
            ns2 = len(self.s2)
            
            if ns2 == 0 or self.s1[ns1-1] <= self.s2[ns2-1]:
                self.s2.append(self.s1.pop())  
            elif self.s1[ns1-1] > self.s2[ns2-1]:
                t = self.s1.pop()
                while len(self.s2) > 0  and t > self.s2[len(self.s2)-1]:
                    self.s1.append(self.s2.pop())
                self.s2.append(t)
                
    def getS1(self):
        return self.s1
    
    def getS2(self):
        return self.s2
# In[Animal Shelter]:
class Animal:
    def __init__(self, value):
        self.value = value
        self.next = None
    
        
class AnimalShelter:
    def __init__(self):
        self.head = None
        self.size = 0
        self.sizeDog = 0
        self.sizeCat = 0
        
    def enqueue(self, animal):
        if animal == 'd':
            self.sizeDog += 1
        else:
            self.sizeCat += 1
            
        if self.size == 0:
            self.head = Animal(animal)
            self.size += 1
        else:
            last = self.head
            while last.next != None:
                last = last.next
            last.next = Animal(animal)
            self.size += 1
            
    def dequeueAny(self):
        if self.size==0:
            return (False, -1)
        first = self.head
        if first.value == 'd':
            self.sizeDog -= 1
        else:
            self.sizeCat -= 1
        self.head = self.head.next
        return (True, first.value)
    
    def dequeueDog(self):
        if self.sizeDog==0:
            return (False, -1)
        print("size dog: ", self.sizeDog)
        current = self.head
        if current.value == 'd':
            self.head = self.head.next
            self.sizeDog -= 1
            self.size -= 1
            return (True, current.value)
            
        while current.value != 'd':
            prev = current
            current = current.next
        
        prev.next = current.next
        
        self.sizeDog -= 1
        self.size -= 1
        
        return (True, current.value)
    
    def dequeueCat(self):
        if self.sizeCat==0:
            return (False, -1)
        
        print("size dog: ", self.sizeCat)
        current = self.head
        if current.value == 'c':
            self.head = self.head.next
            self.sizeCat -= 1
            self.size -= 1
            return (True, current.value)
            
        while current.value != 'c':
            prev = current
            current = current.next
        
        prev.next = current.next
        
        self.sizeCat -= 1
        self.size -= 1
        
        return (True, current.value)
    
    def print(self):
        current = self.head
        if current is None:
            print("No animal in shelter")
            
        while current:
            print(current.value)
            current = current.next
            
# In[]:
shelter = AnimalShelter()
shelter.enqueue('c')
shelter.enqueue('c')
shelter.enqueue('d')
shelter.enqueue('c')
shelter.enqueue('d')
shelter.enqueue('c')
shelter.enqueue('d')
shelter.print()
print("any: " , shelter.dequeueAny())
print("dog: ", shelter.dequeueDog())
print("cat: ", shelter.dequeueCat())
print("any: " , shelter.dequeueAny())
print("dog: ", shelter.dequeueDog())
print("cat: ", shelter.dequeueCat())
print("any: " , shelter.dequeueAny())
print("dog: ", shelter.dequeueDog())
print("cat: ", shelter.dequeueCat())

        
            
            
        
    
            
        
        
                    
                             
                             

                
                
        
        
        
        
        
        
        
        
    
    
    
    