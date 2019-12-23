infinity = 1000000  #Infinity value is a set to a large number and is used as the default distance from source for each node
invalid_node = -1   #Invaild node value is used to represent a node that doesnt exist in the network and is used as the default previous node for each node

class Node:                     #Node class is used to represent each of the nodes in the network
    previous = invalid_node     #Previous variable keeps record of the previously visited node before coming to the current node
    distfromsource = infinity   #Distfromsource variable keeps record of the nodes total distance from the starting node
    visited = False             #Visited flag keeps track of whether the node has been visited or not

class Dijkstra:                             #Dijkstra class holds all of the functions and variables for Dijkstra's Algorithm
    def __init__(self):                     #__init__ is the constructor for the class and is used to initialise the class
        self.startnode = 0                  #Startnode variable is used to store the starting node in the network
        self.endnode = 0                    #Endnode variable is used to store the end node in the network
        self.network = []                   #Network list is used to record information about the network such as the weights of the edges connecting each node
        self.network_populated = False      #Network_populated flag is used to tell if the network list has been populated
        self.nodetable = []                 #Nodetable list is used to record information about each node and is populated with objects of the Node class
        self.nodetable_populated = False    #Nodetable_populated flag is used to tell if the nodetable list has been populated
        self.route = []                     #Route list holds the final shortest path that Dijkstra's Algorithm finds
        self.route_populated = False        #Route_populated flag is used to tell if the start and end nodes have been parsed from route.txt
        self.currentnode = 0                #Currentnode variable is used to store the node that the algorithm is currently on in the network

    def populate_network(self, filename):                   #Function to populate the network list using a file with the filename being passed in as a parameter
        try:                                                #Try to open the specified file for reading
            networkfile = open(filename, "r")
        except IOError:                                     #Catch the exception IOError, display an error message and return
            print "Network file does not exist!"
            return
        for line in networkfile:                            #For each line in the file, create a list of values using the comma to tell when to each value begins, each line represents a node in the network
            self.network.append(map(int, line.split(',')))
        self.network_populated = True                       #Set the network_populated flag to true because the file has been read
        networkfile.close()                                 #Close the file at the end of the function

    def populate_node_table(self):                          #Function to populate the nodetable
        if not self.network_populated:                      #if the network_populated flag is false, display a message and return
            print "Network not populated!"
            return
        for node in self.network:                           #for each node in the network, add an object of Node to the nodetable for each node
            self.nodetable.append(Node())
        self.nodetable[self.startnode].distfromsource = 0   #Set the starting node's distance from source to 0
        self.nodetable[self.startnode].visited = True       #Set the starting node's visited flag to true
        self.nodetable_populated = True                     #Set the nodetable_populated flag is set to true as the nodetable has been populated

    def parse_route(self, filename):                #Function to parse the start and end nodes from a file with the filename being passed in as a parameter
        routefileinfo = []                              #Variable to temporarily hold the data from the file
        try:                                        #Try to open the specified file for reading
            routefile = open(filename, "r")
        except IOError:                             #Catch the exception IOError, display an error message and return
            print "Route file does not exist"
            return
        for line in routefile:                      #For each line in the file, create a list of values using the > symbol to tell when to each value begins
            routefileinfo.append(line.split(">"))
        self.startnode = ord(routefileinfo[0][0])-65    #The first value represents the starting node
        self.endnode = ord(routefileinfo[0][1])-65      #The second value represents the end node
        self.route_populated = True                 #Route_populated flag is set to true because the file has been parse correctly

    def return_near_neighbour(self):                                    #Function is used to determine the nearest neighbours of the current node
        nearestneighbours = []                                          #Nearestneighbours list is used to hold the nearest neighbours of the current node
        for index, edge in enumerate(self.network[self.currentnode]):   #For each edge in the row of network that corresponds to the current node, if the edge is greater than 0 and the potential neighbour is unvisited, append the node to the nearest neighbours list
            if edge > 0 and not self.nodetable[index].visited:
                nearestneighbours.append(index)
        return nearestneighbours                                        #Return the list of nearest neighbours

    def calculate_tentative(self):                                                                              #Function is used to calculate the tentative distances of the nearest neighbours
        nearestunvisitednodes = self.return_near_neighbour()                                                    #The return_near_neighbour function is called and returns a list of nearest neighbours
        for index in nearestunvisitednodes:                                                                     #For each neighbour in the list, calculate the distance from the starting node to the near neighbour
            distance = self.nodetable[self.currentnode].distfromsource + self.network[self.currentnode][index]
            if distance < self.nodetable[index].distfromsource:                                                 #If the newly calculated distance is less than the existing distance from source, record the new distance and set the previous node equal to the current node
                self.nodetable[index].distfromsource = distance
                self.nodetable[index].previous = self.currentnode

    def determine_next_node(self):                                              #Function is used to determine the next node to move to in the network
        shortestdistance = infinity                                             #The shortest distance is temporarily set to infinity
        nextnodeindex = invalid_node                                            #The next node is temporarily set to invalid node
        for index, node in enumerate(self.nodetable):                           #for each node in nodetable, if the node's distance from source is less than shortest distance and the node is unvisited, set shortest distance to that nodes distance from source and set next node index to the index of that node
            if (node.distfromsource < shortestdistance) and not node.visited:
                shortestdistance = node.distfromsource
                nextnodeindex = index
        self.currentnode = nextnodeindex                                        #Move to the node that has the shortest distance from source and is unvisited

    def calculate_shortest_path(self):                                                                                  #Function is used to calculate the shortest path across the network
        if self.network_populated is False:                                                                             #If the network_populated flag is false, call the populate_network function
            self.populate_network("network.txt")
        if self.route_populated is False:                                                                               #If the route_populated flag is false, call the parse_route function
            self.parse_route("route.txt")
        if self.nodetable_populated is False:                                                                           #If the nodetable_populated flag is false, call the populate_node_table function
            self.populate_node_table()
        self.currentnode = self.startnode                                                                               #Set the current node equal to the starting node
        while (not all(node.visited is True for node in self.nodetable)) and (self.currentnode is not invalid_node):    #While there are unvisited nodes and the current node is not invalid, set the current node to visited, calculate the tentative distances of near neighbours and determine the next node
            self.nodetable[self.currentnode].visited = True
            self.calculate_tentative()
            self.determine_next_node()

    def return_shortest_path(self):                                                         #Function is used to return the shortest path and the distance of that path
        self.calculate_shortest_path()                                                      #The calculate_shortest_path function is called
        self.currentnode = self.endnode                                                     #current node is set to the end node
        while self.nodetable[self.currentnode].previous is not invalid_node:                #While the current node's previous node is not invalid, append the current node to the path and change the current node to the previous node
            self.route.append(self.currentnode)
            self.currentnode = self.nodetable[self.currentnode].previous
        self.route.append(self.startnode)                                                   #Append the starting node to the path
        self.route = self.route[::-1]                                                       #Reverse the list so that it is in the correct order
        return self.route, self.nodetable[self.route[len(self.route)-1]].distfromsource     #Return the shortest path, and the distance of the shortest path

class MaxFlow(Dijkstra):            #MaxFlox class holds all of the functions and variables for max flow, class also inherits from Dijkstra class
    def __init__(self):             #__init__ is the constructor for the class and is used to initialise the class
        Dijkstra.__init__(self)     #Constructor for the Dijkstra class is called
        self.original_network = []  #Original_network variable is used to hold a version of the network at the start of the max flow algorithm

    def populate_network(self, filename):           #Function to populate the network list using a file with the filename being passed in as a parameter
        Dijkstra.populate_network(self, filename)   #Calls the Dijkstra version of the populate_network function, passing in the filename
        self.original_network = self.network[:]     #A copy of the network is made and stored in original network
        for index, node in enumerate(self.network): #A copy of each row of network is made and stored in the corresponding row of original network
            self.original_network[index] = node[:]

    def return_near_neighbour(self):                                    #Function is used to determine the nearest neighbours of the current node
        nearestneighbours = []                                          #Nearestneighbours list is used to hold the nearest neighbours of the current node
        for index, edge in enumerate(self.network[self.currentnode]):   #For each edge in the row of network that corresponds to the current node, if the edge is greater than 0 and the potential neighbour is unvisited, append the node to the nearest neighbours list
            if edge > 0 and not self.nodetable[index].visited:
                nearestneighbours.append(index)
        return nearestneighbours                                        #Return the list of nearest neighbours

    def return_bottleneck_flow(self):                                               #Function to determine the bottleneck flow of a given path
        bottleneck = infinity                                                       #Bottleneck is temporarily set to infinity
        for node in self.route:                                                     #For each node in the path, if the previous node is not invalid and the distance between the current and previous nodes is less than the bottleneck, the bottleneck is set to that distance
            if self.nodetable[node].previous is not invalid_node:
                if self.network[self.nodetable[node].previous][node] < bottleneck:
                    bottleneck = self.network[self.nodetable[node].previous][node]
        return bottleneck                                                           #Return the bottleneck

    def remove_flow_capacity(self):                                                                                             #Function is used to remove the flow capacity from the network
        flow = self.return_bottleneck_flow()                                                                                    #The flow is equal to the bottleneck which is found by calling the return_bottleneck_flow
        for node in self.route:                                                                                                 #For each node in the path, if the previous node is not invalid, the flow is removed from each edge in the path but the flow is also added in the opposite direction
            if self.nodetable[node].previous is not invalid_node:
                self.network[self.nodetable[node].previous][node] = self.network[self.nodetable[node].previous][node] - flow
                self.network[node][self.nodetable[node].previous] = self.network[node][self.nodetable[node].previous] + flow
        return self.route, flow                                                                                                 #Return the path and the flow value

    def return_max_flow(self):                                      #Function is used to calculate the max flow across the network
        maxflow = 0                                                 #Max flow is initally set to 0
        paths = []                                                  #A list of paths is created to record each path used
        pathexists = True                                           #Path exists flag is used to keep the while loop running
        while (pathexists):                                         #While a path exists, get the path and the distance, add the flow capacity to max flow, append the path used to the paths list, reset the nodetable and delete the path found
            route, distant = self.return_shortest_path()
            if distant is 0:                                        #If no path is found, set pathexists to false, this ends the loop
                pathexists = False
            else:
                path, flow = self.remove_flow_capacity()
                paths.append(path)
                paths[len(paths)-1] = self.route[:]
                maxflow = maxflow + flow

                for node in self.nodetable:
                    node.previous = invalid_node
                    node.distfromsource = infinity
                    node.visited = False
                self.nodetable[self.startnode].distfromsource = 0
                self.nodetable[self.startnode].visited = True

                del self.route[:]

        return  maxflow, paths                                      #Return the max flow value and the list of paths used


if __name__ == '__main__':
        Algorithm1 = Dijkstra()
        route, dist = Algorithm1.return_shortest_path()
        print "Dijkstra"
        print "Shortest Path: ", route
        print "Distance: ", dist

        print ""

        Algorithm2 = MaxFlow()
        maxflow, paths = Algorithm2.return_max_flow()
        print "Max Flow"
        print "Max Flow Value: ", maxflow
        print "Paths Used: ", paths
