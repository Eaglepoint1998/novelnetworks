import collections;
from _operator import itemgetter
import community
import networkx as nx
from networkx.algorithms.centrality.communicability_alg import communicability
from flask import Flask, render_template, request, jsonify, make_response

class Network:
    def __init__(self):
        self.char1 = "";
        self.char2 = "";
        self.edge = 0;
class Table:
    def __init__(self):
        self.names = [];
        self.paragraphs = [];
                
    def findParagraphs(self, fileobject, n):
        builder = ""
        i =0        
        for line in fileobject:
            builder += line;
            if builder.count('\n\n') == n:                           
                    i+=1;
                    self.addToParaTable(i, builder)
                    builder = "";
        self.calcPageRank(table)               
    
    def calcPageRank(self, table):
        for row in table:
            if len(row.names) > 1:
                if row.names[0] in pageRank and row.names[1] in pageRank:
                    pageRank[row.names[0]] = pageRank[row.names[0]] + pageRank[row.names[1]]
                    pageRank.pop(row.names[1], None)
        
    def findWords(self, fileobject, count):
        builder = [] #makes 25 words
        i =0; #keeps number to be stored in table
        global dealt #lets the holder know not to overwrite the builder if a word was dealt with
        for line in fileobject:           
            built = False
            dealt = False
            holder = "" 
            temp = line.split(" ") #makes the line an array of words, normally size 15
            builder += temp #add this to builder
            if(len(builder) > count): #if its bigger than count
                i+=1
                holder = builder[count:len(builder)] #holder holds the excess
                builder = builder[0:count] #builder set to size count
                for word in builder:
                    builder = self.compareToTable(builder, count, word, i) #compares each word to table and returns word at 0 in holder if found
                    built = True
            if built == True and len(builder)>0 and dealt == False: #conditions to set builder to the excess
                builder = holder
               
        self.calcPageRank(table)
    
    def compareToTable(self, builder, count, word, i):         
        for row in table:                        
            for name in row.names:
                if word == name: #compares the word to all elements in the table
                    index = builder.index(word) #takes index of word
                    builder = builder[index:len(builder)] #cuts stuff before index
                    row.paragraphs.append(i) #adds the entry to the table
                    pageRank[name] += builder.count(name); #increases page rank
                    dealt = True;#lets holder know not to overwrite
                    return builder
        return builder
        
    def findSentences(self, fileobject, n):
        builder = "";
        holder = "";
        i =0;
        built = True
        for line in fileobject:
            builder += line;
            while builder.count('.') > 0:
                    
                if builder.count('.') == n:                           
                    i+=1;
                    self.addToParaTable(i, builder)
                    if built == False:
                        builder = str(holder)
                        if len(holder) != 0:
                            del holder[0]
                    else:
                        builder = ""
                    if builder.count('.') ==0:
                        built = True
                    
                elif builder.count('.') > n:
                    builder = builder.strip('\n')
                    parts = builder.split('.') 
                    parts = [s + '.' for s in parts]
                    del parts[len(parts)-1]
                    holder = parts[n:len(parts)]
                    builder = str(parts[0:n])
                    built = False 
                elif builder.count('.') < n:
                    break;           
        self.calcPageRank(table)
        
    def addToParaTable(self, i, builder):
        for row in table:
            for name in row.names:
                if name in builder:
                    row.paragraphs.append(i)
                    pageRank[name] += 1;
    
    def SetUp(self, fileobject1, fileobject2): 
        global table;
        global pageRank;   
        global headers;
        global booleans
        table = []
        names = []
        headers = []
        pageRank = {};
        booleans = {}
        i = 0;
        for name in fileobject1:
            if(i==0):
                headers = name.split(',')
                i+=1
            else:   
                name = name.strip();                              
                name = name.split(',')
                names.append(name[0])
                pageRank[name[0]] = 0
                booleans[name[0]] = name.pop()                 
                if name[1]!= "":
                    pageRank[name[1]] = 0
                    names.append(name[0])
                else:
                    del name[1]
                           
                row = Table();
                row.names = name;
                table.insert(i, row)
                i+=1;
        
    def processTable(self):
        global network;
        network = {};
        global G
        G= nx.Graph()
        for i in range(0,len(table)):#current row           
            for j in range(i+1, len(table)): #every other row                
                for para in range(0,len(table[i].paragraphs)): #paragraphs in current row
                    for para2 in range(0, len(table[j].paragraphs)): # paragraphs in every other row
                        if table[i].paragraphs[para] == table[j].paragraphs[para2]:
                            key = table[i].names[0] + "," + table[j].names[0]
                            if  key in network:
                                network[key] += 1                                
                            else:
                                network[key] = 1;                                
        network = collections.OrderedDict(sorted(network.items(), key = itemgetter(1), reverse = True))

    def makeNxGraph(self):
        global G
        G= nx.Graph()
        for key, value in network.items():
            term = str(key).split(",")
            
            if not G.has_node(term[0]):
                G.add_node(term[0])
            if not G.has_node(term[1]):
                G.add_node(term[1])          
            G.add_edge(term[0], term[1])
            G.edge[term[0]][term[1]]['weight'] = value;
        
    def writeCSV(self):
        outfile = open( 'edges.csv', 'w' )
        outfile.write("Source,Target,Weight\n" )
        for key, value in sorted(network.items()):
            outfile.write(str(key) + ',' + str(value) + '\n' )
        outfile2 = open('nodes.csv', 'w')
        outfile2.write("ID,Label\n")
        for indtable in table:
                outfile2.write(indtable.names[0] + "," + indtable.names[0] + "\n")

    
         
    def communityIdentify(self):
        global s_partition 
        partition = community.best_partition(G)
        s_partition = sorted(partition.items(), key = lambda x:x[1])

       
    def makeJSON(self):
        global info
        info = "";
        info+= "{\n \"info\": {\n\"nodes\": [\n"
        i = 0;
        num = len(s_partition)
        sorted_betweeness = []
        sorted_degree = []
        sorted_eigenvector = []
        sorted_closeness = []
        sorted_harmonic = []
        sorted_communicability =[]
        sorted_core = []
        sorted_degree1 = []
        sorted_partition = s_partition
        unadjusted_betweeness = []
        unadjusted_degree = []
        unadjusted_eigenvctor =[]
        unadjusted_closeness = []
        unadjusted_harmonic = []
        unadjusted_communicability = []
            
        G.remove_edges_from(G.selfloop_edges())
        for key, value in nx.betweenness_centrality(G).items():
            value1 = 1 + (value*100);
            temp1 = [key, value]
            temp = [key, value1]
            sorted_betweeness.append(temp1)
            unadjusted_betweeness.append(temp1)
        sorted_partition = sorted(sorted_partition)
        sorted_betweeness = sorted(sorted_betweeness)
        unadjusted_betweeness = sorted(unadjusted_betweeness)
    
        for key, value in nx.degree_centrality(G).items():
            value1 = 1 + (value*100);
            temp1 = [key, value]
            temp = [key, value1]
            sorted_degree.append(temp1)
            unadjusted_degree.append(temp1)
        sorted_degree = sorted(sorted_degree)
        unadjusted_degree = sorted(unadjusted_degree)   
        
        for key, value in nx.eigenvector_centrality(G).items():
            value1 = value*1000;
            temp1 = [key, value]
            temp = [key, value1]
            sorted_eigenvector.append(temp1)
            unadjusted_eigenvctor.append(temp1)
        sorted_eigenvector = sorted(sorted_eigenvector)
        unadjusted_eigenvector = sorted(unadjusted_eigenvctor)     
        
        for key, value in nx.closeness_centrality(G).items():
            value1 = (value*10);
            temp1 = [key, value]
            temp = [key, value1]
            sorted_eigenvector.append(temp1)
            unadjusted_eigenvctor.append(temp1)
        sorted_eigenvector = sorted(sorted_eigenvector) 
        
        for key, value in nx.harmonic_centrality(G).items():
            temp1 = [key, value]

            sorted_harmonic.append(temp1)
            unadjusted_eigenvctor.append(temp1)
        sorted_harmonic = sorted(sorted_harmonic)
        unadjusted_harmonic = sorted(unadjusted_eigenvctor)    
        
        for key, value in nx.communicability_centrality(G).items():
            temp1 = [key, value]
            sorted_communicability.append(temp1)
            unadjusted_eigenvctor.append(temp1)
        sorted_communicability = sorted(sorted_communicability)
        unadjusted_communicability = sorted(unadjusted_eigenvctor)    

        for key, value in nx.core_number(G).items():#list
            
            temp = [key, value]
            sorted_core.append(temp)
        sorted_core = sorted(sorted_core)
        
        for key, value in nx.degree(G).items():#list
            
            temp = [key, value]
            sorted_degree1.append(temp)
        sorted_degree1 = sorted(sorted_degree1)
        
        central_dict = {}
        unadjusted_dict = {}
        global importance 
        importance = {}
        
        for key, value in sorted_betweeness:
            central_dict[key] = []
            importance[key] = 0
            central_dict[key].append(value)
        
        for key, value in unadjusted_betweeness:
            unadjusted_dict[key] = []
            unadjusted_dict[key].append(value)

            
        for key, value in sorted_degree:
            central_dict[key].append(value)
            importance[key] += value
        
        for key, value in unadjusted_degree:
            unadjusted_dict[key].append(value)
        
        for key, value in sorted_eigenvector:
            central_dict[key].append(value)
            importance[key] + value
        
        for key, value in unadjusted_eigenvector:
            unadjusted_dict[key].append(value)
            
        for key, value in sorted_closeness:
            central_dict[key].append(value)
            importance[key] += value
        
        for key, value in unadjusted_closeness:
            unadjusted_dict[key].append(value)
        
        for key, value in sorted_harmonic:
            central_dict[key].append(value)
            importance[key] += value
        
        for key, value in unadjusted_harmonic:
            unadjusted_dict[key].append(value)
        
        for key, value in sorted_communicability:
            central_dict[key].append(value)
            importance[key] += value        
        
        for key, value in unadjusted_communicability:
            unadjusted_dict[key].append(value)
        
        for key, value in sorted_core:
            importance[key] += value
        
        for key, value in sorted_degree1:
            importance[key] += value
            
        averages ={}
        acc ={}
        totals = {}
        groups = []
        for key, value in sorted_partition:
            val1 = booleans[key]
            if val1 not in groups:
                groups.append(val1)
                acc[val1] = 0
                totals[val1] = 0
                
        for key, value in importance.items():
            val1 = booleans[key]
            for item in groups:
                if(val1 == item):
                    acc[item] += value
                    totals[item]+=1
        
        for key, value in acc.items():
            averages[key] = acc[key]/totals[key]
            
        for key,value in sorted_partition:
            i+=1
            val1 = booleans[key]
            info+= "{\"id\": \"" + str(key) + "\", \"group\": " + str(value) +  ", \"question\": \"" + str(val1) + "\", "
            val = unadjusted_dict[key]
            
            info+= "\"Centrality\": { \"Betweeness\": " + str(val[0]) + ", \"Degree\": " + str(val[1]) + ", \"Eigenvector\": " + str(val[2]) + ", \"Closeness\": " + str(val[3]) +  ", \"Harmonic\": " + str(val[4]) + ", \"Communicability\": " + str(val[5]) +" } "
            if num == i:
                info += "} \n"
            else:
                info += "}, \n"
        info += "],\n \"links\":[\n"
        num = len(network)
        i=0;
        partition_dict = dict(sorted_partition)
        for key, value in sorted(network.items()):
            i+=1
            term = str(key).split(",")         
            group = partition_dict[term[0]]
            if num == i:
                info += "{\"source\": \"" + term[0] + "\", \"target\": \"" + term[1] + "\", \"value\": \"" + str(value) +"\", \"group\": " + str(group) + "}\n"
            else:
                info += "{\"source\": \"" + term[0] + "\", \"target\": \"" + term[1] + "\", \"value\": \"" + str(value) +"\", \"group\": " + str(group) + "},\n"
        info += "],\n \"Unadjusted_centrality\":[\n"
        i =0
        num = len(unadjusted_dict)
        for key, value in unadjusted_dict.items():
            i+=1
            val = value
            info+= "{\"id\": \"" + str(key) + "\",\"Centrality\": { \"Betweeness\": " + str(val[0]) + ", \"Degree\": " + str(val[1]) + ", \"Eigenvector\": " + str(val[2]) + ", \"Closeness\": " + str(val[3]) +  ", \"Harmonic\": " + str(val[4]) + ", \"Communicability\": " + str(val[5]) +" } "
            if num == i:
                info += "} \n"
            else:
                info += "}, \n"
        num = len(importance)
        i=0;
        info += "],\n \"importance\":[\n"
        for key, value in importance.items():
            i+=1
            val1 = booleans[key]
            info+= "{\"id\": \"" + str(key) + "\", \"importance\": " + str(value) +  ", \"question\": \"" + str(val1) + "\""
            if num == i:
                info += "} \n"
            else:
                info += "}, \n"
        num = len(acc)
        i=0;
        info += "],\n \"group_stats\":[\n"
        for key, value in acc.items():
            i+=1
            val2 = averages[key]
            val3 = totals[key]
            info+= "{\"group\": \"" + str(key) + "\", \"total_importance\": " + str(value) +  ", \"average_importance\": " + str(val2) +", \"total_mentions\": " + str(val3) 
            if num == i:
                info += "} \n"
            else:
                info += "}, \n"
        num = len(pageRank)
        i =0;
        info += "],\n \"pagerank\":[\n"
        for key, value in pageRank.items():
            i+=1
            info+= "{\"id\": \"" + str(key) + "\", \"pagerank\": " + str(value)
            if num == i:
                info += "} \n"
            else:
                info += "}, \n"
                num = len(booleans)
        i =0;
        question = headers[2]
        info += "],\n \"question\":[\n"
        for key, value in booleans.items():
            i+=1
            info+= "{\"id\": \"" + str(key) + "\", \"question\": \"" + str(value) + "\""
            if num == i:
                info += "} \n"
            else:
                info += "}, \n"   
        info += "]\n},"
           
    def writeStatsJson(self):        
        stats = ""      
        trans = nx.transitivity(G)#Number
        if(nx.is_connected(G)):
            diameter = nx.diameter(G)#number
            periphery = nx.periphery(G)#list        
            central = nx.center(G)#list
        else:
            diameter = 0;
            periphery = {}
            central = {}
        density = nx.density(G)#number
        size = G.size();#ticknumber
        connected = nx.algebraic_connectivity(G)#number
        G.remove_edges_from(G.selfloop_edges())
        core = nx.core_number(G)#list
        degrees = nx.degree(G)#list  
        cliques = nx.find_cliques(G)#list
        stats += "\"stats\":{\n\"graph_stats\": \n"
        stats+="{\"size\": " + str(size) + ", \"connectivity\": " + str(connected) + ", \"transitivity\": " + str(trans) + ", \"density\": " + str(density) + ", \"diameter\": " + str(diameter) + "}\n,\n"
        stats+="\"Periphery_stats\": [\n"
        num = len(periphery)
        i=0
        for item in periphery:
            i+=1
            if(i==num):
                stats+="{\"node\": \"" + item + "\"}\n"
            else:
                stats+="{\"node\": \"" + item + "\"},\n"
        stats+= "],\n"
        stats+= "\"Central_stats\": [\n"
        num = len(central)
        i=0
        for item in central:
            i+=1
            if(i==num):
                stats += "{\"node\": \"" + item + "\"}\n"
            else:
                stats += "{\"node\": \"" + item + "\"},\n"
        stats += "],\n"
        num = len(core)
        i=0
        stats += "\"Node_stats\": [\n"
        for key in core:
            i+=1
            val = degrees[key]
            val2 = core[key]
            if(i==num):
                stats += "{\"node\": \"" + key+ "\", \"core\": " + str(val2) + ", \"degree\": " + str(val) + "}\n"
            else:
                stats += "{\"node\": \"" + key+ "\", \"core\": "+ str(val2) + ", \"degree\": " + str(val) + "},\n"
        stats += "],\n"
        stats += "\n\"Clique_stats\": [\n"
        i = 0
        j = 0
        cliques = list(cliques)
        length = len(cliques)
        for item in cliques:           
            stats += "{"
            num = len(item)
            i+=1
            for character in item:
                j+=1
                if(j == num):
                    stats += "\"Character " + str(j) + "\": \"" + character + "\""
                else:
                    stats += "\"Character " + str(j) + "\": \"" + character + "\","
            j = 0
            if(i == length):
                stats += "}\n"
            else:
                stats += "},\n"
        stats += "]\n"        
        #Closing bracket 
        stats+="}\n}"
        json = info + stats
        print(json)
        return json

app = Flask(__name__)
@app.route('/upload')
def upload_file():
    return render_template('upload.html')

    
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        file_object1 = open(f.filename, "r", encoding ='utf-8'); 
        f = request.files['character']
        file_object2 = open(f.filename, "r", encoding ='utf-8');
        R = Table()
        R.SetUp(file_object2, file_object1);
        read_type = request.args.get('type')
        num = int(request.args.get('N'))
        if(read_type == 'Paragraphs'):
            R.findParagraphs(file_object1, num)          
        if(read_type == 'Sentences'):
            R.findSentences(file_object1, num) 
        if(read_type == 'Words'):
            R.findWords(file_object1, num)
        else: 
            R.findParagraphs(file_object1, num)
        R.processTable();
        R.writeCSV();
        R.makeNxGraph();
        R.communityIdentify()
        
        R.makeJSON()
        json = R.writeStatsJson()
        j = make_response(jsonify(json))
        j.mimetype = 'application/json'
        return j, 201, {'Access-Control-Allow-Origin': '*'}

        
if __name__ == '__main__':
    app.run(debug = True)