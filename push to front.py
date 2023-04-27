
class Edge:
    def __init__(self, flow, capacity, u, v):
        self.flow = flow
        self.capacity = capacity
        self.u = u
        self.v = v

class Vertex:
    def __init__(self, h, e_flow):
        self.h = h
        self.e_flow = e_flow


class Graph:
    def __init__(self, V,disable_prints=False):
        self.V = V
        self.edges = []
        self.ver = []
        for i in range(V):
            self.ver.append(Vertex(0, 0))
        self.disable_prints = disable_prints
    
    def add_edge(self, u, v, capacity):
        self.edges.append(Edge(0, capacity, u, v))


    def preflow(self, s):
        self.ver[s].h = len(self.ver)

        for i in range(len(self.edges)):
            if self.edges[i].u == s:
                self.edges[i].flow = self.edges[i].capacity

                self.ver[self.edges[i].v].e_flow += self.edges[i].flow

                
                self.edges.append(Edge(-self.edges[i].flow, 0, self.edges[i].v, s))
				



    def update_reverse_edge_flow(self, i, flow):
            
        u = self.edges[i].v
        v = self.edges[i].u

        for j in range(0, len(self.edges)):
            if self.edges[j].v == v and self.edges[j].u == u:
                self.edges[j].flow -= flow
                return

        
        e = Edge(0, flow, u, v)
        self.edges.append(e)


    def print_push(self,u,v,residual_cap,state):
        if self.disable_prints:
            return
        print(state,'Pushing:')
        print('Source Vertex:',u,'Height:',self.ver[u].h,'Excess flow:',self.ver[u].e_flow,end=' -> ')
        print('Dest Vertex:',v,'Height:',self.ver[v].h,'Excess flow:',self.ver[v].e_flow,end='~')
        print('Residual Capacity:',residual_cap)

    def print_relabel(self,u,state):
        if self.disable_prints:
            return
        print(state,'Relabling:')
        if state=='Before':
            print('Source Vertex:',u,'Height:',self.ver[u].h,'Excess flow:',self.ver[u].e_flow,end=' ')
            print('Residual Neighbors:',end=' ')
            for i in range(0, len(self.edges)):
                if self.edges[i].u == u:
                    if self.edges[i].flow != self.edges[i].capacity:
                        print(self.edges[i].v,end=',')
            print()

                   
                   
            
        else:
            print('Source Vertex:',u,'Height:',self.ver[u].h)
       
        

    def push(self, u):
        for i in range(0, len(self.edges)):
            if self.edges[i].u == u:
                if self.edges[i].flow == self.edges[i].capacity:
                    continue

               
                if self.ver[u].h > self.ver[self.edges[i].v].h:
                        self.print_push(u,v,self.edges[i].capacity - self.edges[i].flow,'Before')
                        flow = min(self.edges[i].capacity - self.edges[i].flow, self.ver[u].e_flow)
                        self.ver[u].e_flow -= flow
                        self.ver[self.edges[i].v].e_flow += flow
                        self.edges[i].flow += flow
                        self.update_reverse_edge_flow(i, flow)
                        self.print_push(u,v,self.edges[i].capacity - self.edges[i].flow,'After')
                        return True

        return False
	
	
    def relabel(self, u):
        mh = float('inf')
        self.print_relabel(u,'Before')
        for i in range(len(self.edges)):
            if self.edges[i].u == u:
                if self.edges[i].flow == self.edges[i].capacity:
                    continue

                if self.ver[self.edges[i].v].h < mh:
                    mh = self.ver[self.edges[i].v].h
                    self.ver[u].h = mh + 1

        self.print_relabel(u,'After')
        
        if not self.disable_prints:
            self.print_residual()
            proceed = input()


    def print_residual(self):
        print('\nResidual Graph')
        for u in range(self.V):
            ver = self.ver[u]
            print('Vertex:',u,'Height:',ver.h,'Excess Flow:',ver.e_flow)
            residual_edges = 0
            for i in range(0, len(self.edges)):
                if self.edges[i].u == u:
                    if self.edges[i].flow == self.edges[i].capacity:
                        continue
                    else:
                        if residual_edges==0:
                            print('Residual Edges:')
                        residual_cap = self.edges[i].capacity - self.edges[i].flow
                        print('Dest Vertex:',self.edges[i].v,'Residual Capacity:',residual_cap)
                        residual_edges+=1

            if residual_edges==0:
                print('No residual edges')

            print()
        


    def discharge(self,u):
        while self.ver[u].e_flow > 0 :
            if self.push(u) == False:
                self.relabel(u)
            

    def push_relabel(self,source,sink):
        self.preflow(source)
        l = []
        for vertex in range(self.V):
            if vertex!=source and vertex!=sink:
                
                l.append(vertex)


    
        i = 0
        
        while i<self.V-2:
            u = l[i]
            old_h = self.ver[u].h
            self.discharge(u)
            if self.ver[u].h >  old_h:
                l.remove(u)
                l.insert(0,u)
                i=-1
                
            i+=1

        return self.ver[sink].e_flow
        

    def print_flows(self):
        for i in range(0, len(self.edges)):
            if self.edges[i].flow>0:
                print('Source:',self.edges[i].u,'Dest:',self.edges[i].v,'Flow:',self.edges[i].flow)
        
    
    

	



f=open('input.txt')
lines=f.readlines()
n = int(lines[0])
g = Graph(n,True)
for line in lines[1:]:
    u,v,c = map(int,line.split())
    g.add_edge(u,v,c)
    


f.close()

print()
print("Maximum flow is ", g.push_relabel(0, n-1))
g.print_flows()


