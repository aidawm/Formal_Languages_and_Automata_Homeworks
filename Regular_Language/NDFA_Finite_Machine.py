
read_int = lambda : int(file.readline())
read_list = lambda : str(file.readline()).removesuffix("\n").split(" ")
read_str = lambda : str(file.readline()).replace("\n","").replace(" ","")

file = open("NDFA_tests","r")

machine_number = read_int()

class Machine: 

    
    def __init__(self) -> None:
        

        self.n_operators = read_int()
    
        self.operators = read_list()
    
        self.n_states = read_int()
    
        self.states = read_list()
    
        self.n_transitions = read_int()
    
        self.transition_table = dict()
    
        for t in range(self.n_transitions):
            tr= read_list()
            if (not tr[0] in self.transition_table.keys()):
                self.transition_table[tr[0]] = dict()
            if (not tr[1] in self.transition_table[tr[0]].keys()):
                self.transition_table[tr[0]][tr[1]] = list()

            
            self.transition_table[tr[0]][tr[1]].append(tr[2])

        for s in self.transition_table.keys():
            for o in self.transition_table[s].keys():
                self.transition_table[s][o] = tuple(self.transition_table[s][o])
    
    
        self.start_state = read_str()
        self.n_final_state= read_int()
        self.final_state = read_list()
        self.n_test_case = read_int()
    
    def next_state(self,states,op):
        result = list()

        if type(states) == str: 
            try:
                next = self.transition_table[states][op]
                for n in next:
                    result.append(n)

                return result
            except:
                return tuple()
            
        
        for s in states:
            try:
                next = self.transition_table[s][op]
                for n in next:
                    result.append(n)
            except:
                continue
        return tuple(result)

    def find_state(self,states,query):
        if (len(states) == 0 and type(states)== tuple):
            return tuple()
        
        if len(query)==1:
            return self.next_state(states,query)
        
    
        result = self.next_state(states,query[0])
        return self.find_state(result,query[1:])


        
    def run_machine(self): 
        print(f"start_state = {self.start_state}")
        if ("" in self.final_state):
            self.final_state.remove("")
        print (f"final state(s) = {self.final_state}")
        print(f"transition table = {self.transition_table}\n\n")
        for t in range(self.n_test_case):
            query = read_str()

            answer = "No"
            results = self.find_state(self.start_state,query)
            # print(results)
            for r in results:
                if r in self.final_state:
                    answer = "Yes"
                    break
# 
            print(f"string = {query} , machine answer = {answer}")
        print("___________________\n\n")
    

for i in range(machine_number):
    print(f"machine {i}:")
    machine = Machine()
    machine.run_machine()
    file.readline()



