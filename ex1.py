#Ofec Israel, 314025057, XXXXXXX
import hashlib

#choose the hash function
def hash_function(value):
#    return value
#    hashlib.sha256().update(value.encode())
    return hashlib.sha256(value.encode()).hexdigest()


class MerkleTree:
    """
    Represents a merkle tree
    """
    def __init__(self, strings):
        self.value = None
        self.left = None
        self.right = None
        self.build_tree(strings)

        
    def build_tree(self, strings):
        """
        Builds tree structure from list of strings
        """
        if len(strings) == 1:
            self.value = strings[0]
        else:
            median = int(len(strings) / 2)
            self.left = MerkleTree(strings[0:median])
            self.right = MerkleTree(strings[median : len(strings)])
            if self.left != None and self.right != None:   
                self.value = hash_function(self.left.value + self.right.value)
            
            
    def create_proof(self, node_value):
        """
        Creates a proof for a node
        """
        if self.value == node_value:
            return ""
        
        res = None
        if self.right != None:
            res = self.right.create_proof(node_value)
            if res != None and self.left != None:
                if res != "":
                    res += " "
                res += "l {}".format(self.left.value)
        
        if self.left != None and res == None:
            res = self.left.create_proof(node_value)
            if res != None and self.right != None:
                if res != "":
                    res += " "
                res += "r {}".format(self.right.value)
                    
        return res
        
        
    def check_proof(args):
        """
        Checks proof
        """
        res = args[0]
        for i in range(2, len(args)):
            if i % 2 == 1:
                continue
            if args[i] == "l":
                res = args[i+1] + res
            if args[i] == "r":
                res = res + args[i+1]
            res = hash_function(res)
        
        return res == args[1]
    

class HandleInput():
    def __init__(self):
        self.merkle_tree = None
        self.user_input = None
        self.stop = False
        self.tree_leaves = None
        
    def start(self):
        """
        Start getting input from user
        """
        actions = {1 : self.create_tree, 2 : self.create_proof, 3 : self.check_proof, 4 : self.set_hardness, 5 : self.quit}
        
        self.stop = False
        while not self.stop:
            self.user_input = input().split(" ")
            action_number = int(self.user_input[0])
            actions[action_number]()
        
    def create_tree(self):
        self.tree_leaves = self.user_input[1:]
        self.merkle_tree = MerkleTree(self.tree_leaves)
        print(self.merkle_tree.value)
    
    def create_proof(self):
        x = self.merkle_tree.create_proof(self.tree_leaves[int(self.user_input[1])])
        print(x)
    
    def check_proof(self):
        print(MerkleTree.check_proof(self.user_input[1:]))
    
    def set_hardness(self):
        # no merkle tree root
        if self.merkle_tree == None:
            return
        # get the hardness from user input
        hardness = int(self.user_input[1])
        value = self.merkle_tree.value
        
        i = 0
        while True:
            #hash the root plus a number
            res = str(hash_function(str(i) + value))
            counter = 0
            for j in res:
                if j == "0":
                    counter += 1
                else:
                    break
                if counter == hardness:
                    print("{} {}".format(i, res))
                    return
            i += 1
    
    def quit(self):
        self.stop = True

def main():
    HandleInput().start()


if __name__ == "__main__":
    main()