import ABS
import re

class StorageDevice:
    def __init__(self,block_count,block_size):
        self.block_count = block_count
        self.__block_size = block_size
        
        
        self.__available_blocks = list(range(block_count))
        self.__used_blocks = []
        
    @property
    def available_block_count(self):
        return self.__available_blocks
    
    @property
    def used_block_count(self):
        return self.__used_blocks
    
    @property
    def total_block_count(self):
        return f"available blocks: {self.__available_blocks} \n 
                 used blocks: {self.__used_blocks}"
    
    @property
    def block_size(self):
        return self.__block_size
    
    def allocate(self,block_count):
        if len(self.__available_blocks) < block_count:
            raise RuntimeError
        else: 
            self.__available_blocks.remove(len(block_count))
            self.__used_blocks.append(len(block_count))
            return self.__available_blocks
        
    def free(self,blocks):
        if not all(block in self.__used_blocks for block in blocks):
            raise RuntimeError("Some blocks to be freed are not currently used")

        for block in blocks:
            self.__used_blocks.remove(block)
            self.__available_blocks.add(block)
        
class Entity(ABS):
    def __init__(self,name,storage):
        if not Entity.is_valid_name(name):
            raise RuntimeError
        
        self.__name = name
        self.__storage = StorageDevice
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self,new_name):
        if not Entity.is_valid_name(new_name):
            raise RuntimeError
        else:
            self.__name = new_name 
        
    @property
    def storage(self):
        return self.__storage
        
    @property
    def size_in_blocks():
        ...
    
    @property
    def size_in_bytes(self):
        return Entity.size_in_blocks * StorageDevice.block_size
    
    @staticmethod
    def is_valid_name(name):
        if len(name) <= 16 and len(name) >= 1:
            if re.match(r'^[A-Za-z0-9.]+$', name):
                return True
        else:
            return False 
    
    def clear():
        ...

        

class File(Entity):
    def __init__(self, storage, name):
        super().__init__(storage, name)
        self.__size_in_blocks = 0
        
    def grow(self,block_count):
        self.__size_in_blocks += block_count
        StorageDevice.allocate(block_count) 
        
    @property
    def size_in_blocks(self):
        return self.__size_in_blocks
    
    @property
    def size_in_bytes(self):
        return self.__size_in_blocks * StorageDevice.block_size
    
    def clear(self):
        self.__size_in_blocks = 0
        StorageDevice.free(StorageDevice.used_block_count)


class Directory(Entity):
    def __init__(self, name, storage):
        super().__init__(name, storage)
        self.__children = []
        
    @property
    def size_in_blocks(self):
        return sum(child.size_in_blocks for child in self.__children)
    
    def add(self,entity):
        self.children.append(entity)
    
    def clear(self):
        for child in self.__children:
            child.clear()
        self.__children.clear()
