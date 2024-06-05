
read_int = lambda : int(file.readline())
read_list = lambda : str(file.readline()).removesuffix("\n").split(" ")
read_str = lambda : str(file.readline()).replace("\n","").replace(" ","")

file = open("DFA_tests","r")

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
    
            self.transition_table[tr[0]][tr[1]] = tr[2]
    
    
        self.start_state = read_str()
        self.n_final_state= read_int()
        self.final_state = read_list()
        self.n_test_case = read_int()
    
    def find_state(self,state,query):
        # print(state,query)
        if (state is None):
            return None
        if len(query)==1:
            try:
                return self.transition_table[state][query]
            except: 
                None,
        try:
            return self.find_state(self.transition_table[state][query[0]],query[1:])
        except: 
            return self.find_state(None,None)

        
    def run_machine(self): 
        print(f"start_state = {self.start_state}")
        print (f"final state(s) = {self.final_state}")
        print(f"transition table = {self.transition_table}\n\n")
        for t in range(self.n_test_case):
            query = read_str()

            answer = "No"
            if self.find_state(self.start_state,query) in self.final_state:
                answer = "Yes"

            print(f"string = {query} , machine answer = {answer}")
        print("___________________\n\n")
    

for i in range(machine_number):
    print(f"machine {i}:")
    machine = Machine()
    machine.run_machine()
    file.readline()



