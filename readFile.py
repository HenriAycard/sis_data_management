import csv
import matplotlib.pyplot as plt 
import chart_studio.plotly as py
import chart_studio.tools as tls

class readFile:

    def __init__(self, name):
        self.name = name
        self.reader = []
        self.mail = []
        self.linkedin = []
        self.etablissement = []
        self.numberEtablissement = {}
		



    def read(self):
        with open(self.name, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                self.reader.append(row)
                #print(row[2])
        csvFile.close()
    
    

    def readMail(self, number):
        for row in self.reader:
            self.mail.append(row[number])
        print(self.mail)

    def readLinkedin(self, number):
        for row in self.reader:
            self.linkedin.append(row[number])
        print(self.linkedin)
        
    def readEtablissement(self, number):
        for row in self.reader:
            self.etablissement.append(row[number])
        
        print(self.etablissement)
    
    def numberByEtablissement(self):
        self.numberEtablissement = {}
        for row in self.etablissement:
            if (row in self.numberEtablissement) == False:
                self.numberEtablissement[row] = 1
            else:
                self.numberEtablissement[row] = self.numberEtablissement[row]+1
        for key, value in self.numberEtablissement.items():
            print(str(key) + " => " + str(value))
        left = []
        for cpt in range(len(self.numberEtablissement)):
            left.append(cpt)
        height = []
        tick_label = []
        for key, value in self.numberEtablissement.items():            
            height.append(value)
            tick_label.append(key)
        """plt.bar(left, height, tick_label = tick_label, linewidth=10)
        plt.figure(figsize=(12,12))
        plt.show() """
        dictionary = plt.figure()

        plt.bar(range(len(self.numberEtablissement)), self.numberEtablissement.values(), align='center')
        plt.xticks(range(len(self.numberEtablissement)), self.numberEtablissement.keys())
        
        #plotly_fig = tls.mpl_to_plotly(dictionary)
        #py.iplot(plotly_fig)
    
    def createFileMail(self):
        fichier = open("mail.txt", "w")
        print("Creating file...")
        for m in self.mail:
            fichier.write(m+'\n')
        fichier.close()

    class Personne:
        """docstring for Personne"""
        def __init__(self, mail, linkedin, etablissement):
            self.mail = mail
            self.linkedin = linkedin
            self.etablissement = etablissement

			
