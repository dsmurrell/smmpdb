# -*- coding: utf-8 -*-

from indigo.indigo_inchi import *
from indigo.indigo_renderer import *

from URLFetchingHelpers import url_fix
import urllib2
from xml.etree.ElementTree import fromstring

class MyIndigo:
    
    def __init__(self, indigo):
        self.indigo = indigo
        self.indigo_inchi = IndigoInchi(indigo)
        
    def getInchiKeyFromSmiles(self, SMILES):
        m = self.indigo.loadMolecule(SMILES)
        return self.indigo_inchi.getInchi(m)

    def readSDF(self, filename, show_errors = True, max_number = -1):
        list = []
        count = 0
        for item in self.indigo.iterateSDFile(filename):
            count += 1
            if max_number!=-1 and count>max_number: break
            try:
                item.checkBadValence()
                item.canonicalSmiles()
                item.molecularWeight()
                list.append(item)
            except IndigoException as e:
                if show_errors:
                    print "Molecule " + str(count) + "(" + str(item.name()) + ") not accepted..."
                    print e
               
        print "Number of molecules read: " + str(len(list))
        print "Out of total molecules: " + str(count)
        return list
    
    def readSmiles(self, filename, show_errors = True, max_number = -1):
        print "reading Smiles " + filename
        list = []
        count = 0
        for item in self.indigo.iterateSmilesFile(filename):
            count += 1
            if max_number!=-1 and count>max_number: break
            try:
                item.checkBadValence()
                item.canonicalSmiles()
                item.molecularWeight()
                list.append(item)
            except IndigoException as e:
                if show_errors:
                    print "Molecule " + str(count) + " not accepted..."
                    print e
               
        print "Number of molecules read: " + str(len(list))
        print "Out of total molecules: " + str(count)
        return list
    
    def writeSDF(self, molecules, filename, number = -1):
        saver = self.indigo.writeFile(filename)
        count = 0
        for item in molecules:
            count += 1
            saver.sdfAppend(item)
            if count == number:
                break 
        print "Number of molecules written: " + str(count)
        
    def writeSMILES(self, molecules, filename, number = -1):
        saver = self.indigo.writeFile(filename)
        count = 0
        for item in molecules:
            count += 1
            saver.smilesAppend(item)
            if count == number:
                break 
        print "Number of molecules written: " + str(count)
    
    # molecules is a list of indigo molecules
    def removeDuplicates(self, molecules):
        list = []
        # use a dictionary to remove duplicates
        u = {}
        repeats = {}
        for item in molecules:
            if item.canonicalSmiles() not in u:
                list.append(item)
            else:
                repeats[item.name()] = u[item.canonicalSmiles()].name()
            u[item.canonicalSmiles()] = item
            
        num_removed = len(molecules) - len(list)
        print "Number of duplicates removed: " + str(num_removed)
        import cPickle
        cPickle.dump(repeats, open('save.p', 'wb')) 
        print repeats
        return list
    
    # returns a list of molecules in set 1 that are not in set 2 by canonical smiles
    def removeMoleculesFromSet1ThatAreInSet2(self, set1, set2):
        u = {}
        for item in set2:
            u[item.canonicalSmiles()] = 1
            
        list = []
        for item in set1:
            if item.canonicalSmiles() not in u:
                list.append(item)
            
        num_removed = len(set1) - len(list)
        print "Number of molecules removed that were in set2: " + str(num_removed)
        return list 
    
    # returns a list of molecules in set 1 that are not in set 2 by canonical 
    def keepMoleculesFromSet1ThatAreInSet2ByName(self, set1, set2):
        u = {}
        for item in set2:
            if item.name() in u:
                print item.name + " already here"
            u[item.name()] = 1
            
        list = []
        for item in set1:
            if item.name() in u:
                list.append(item)
            
        num_removed = len(set1) - len(list)
        print "Number of molecules removed that were in set2 by name: " + str(num_removed)
        return list
    
    # returns a list of tuples of molecules
    def getOverlappingTuples(self, set1, set2):
        u = {}
        for item in set2:
            u[item.canonicalSmiles()] = item

        list = []
        for item in set1: 
            if item.canonicalSmiles() in u:
                otherItem = u[item.canonicalSmiles()]
                list.append((item, otherItem))
        
        print "Number of overlapping molecules by canonical smiles: " + str(len(list))            
        return list
    
    def isAtomOrganic(self, atom):
        return (atom.atomicNumber() == 1 or # hydrogen
            atom.atomicNumber() == 6 or # carbon
            atom.atomicNumber() == 7 or # nitrogen
            atom.atomicNumber() == 8 or # oxygen
            atom.atomicNumber() == 15 or # phosphorus
            atom.atomicNumber() == 16 or # sulphur
            atom.atomicNumber() == 9 or # fluorine
            atom.atomicNumber() == 17 or # chlorine
            atom.atomicNumber() == 35 or # bromine
            atom.atomicNumber() == 53 ) # iodine
    
    def removeNonOrganic(self, molecules):
        list = []
        for item in molecules:
            keep = True
            for atom in item.iterateAtoms():
                if not self.isAtomOrganic(atom):
                    keep = False
                    break
            if keep:
                list.append(item)
        num_removed = len(molecules) - len(list)
        print "Number of non-organic molecules removed: " + str(num_removed)
        return list
    
    def resetIsotopes(self, molecules):
        list = []
        for item in molecules:
            for atom in item.iterateAtoms():
                atom.resetIsotope()    
            
            list.append(item)
        return list
    
    def unfoldHydrogens(self, molecules):
        list = []
        for item in molecules:
            item.unfoldHydrogens()
            list.append(item)
        return list
    
    def removeLarge(self, molecules, large_limit):
        list = []
        for item in molecules:
            if (item.molecularWeight() <= large_limit):
                list.append(item)
        num_removed = len(molecules) - len(list)
        print "Number of molecules deemed to large removed: " + str(num_removed)
        return list
    
    def removeSmallAndLarge(self, molecules, small_limit, large_limit):
        list = []
        for item in molecules:
            if (item.molecularWeight() >= small_limit and item.molecularWeight() <= large_limit):
                list.append(item)
            else:
                print item.molecularWeight()
        num_removed = len(molecules) - len(list)
        print "Number of molecules of the wrong size removed: " + str(num_removed)
        return list
    
    def removeTooManyOfOneAtomType(self, molecules, atomic_number, max_number):
        list = []
        for item in molecules:
            number = 0
            for atom in item.iterateAtoms():
                if atom.atomicNumber() == atomic_number:
                    number += 1
            if number<=max_number:
                list.append(item)
        num_removed = len(molecules) - len(list)
        print "Number of molecules removed having more than " + str(max_number) + " atoms of atomic number " + str(atomic_number) + ": " + str(num_removed)
        return list
    
    def containsMoreThanX(self, molecule, atomic_number, X):
        number = 0
        for atom in molecule.iterateAtoms():
            if atom.atomicNumber() == atomic_number:
                number += 1
        if number<=X:
            return False
        else:
            return True
    
    def removeLackingProperty(self, molecules, property):
        list = []
        for molecule in molecules:
            if (molecule.hasProperty(property)):
                if (molecule.getProperty(property) != "N/A"):
                    list.append(molecule)
        print "Number of molecules removed without property " + property + ": " + str(len(molecules)-len(list))
        return list          
    
    def sortByMolecularWeight(self, molecules):
        print "Sorted by molecular weight"
        return sorted(molecules, key=lambda x: x.molecularWeight(), reverse=True)
    
    def removeAllPropertiesFromMolecules(self, molecules):
        list = []
        for molecule in molecules:
            self.removeAllProperties(molecule)
            list.append(molecule)
        return list
    
    def getTotalCharge(self, molecule):
        total_charge = 0
        for atom in molecule.iterateAtoms():
            total_charge = total_charge + atom.charge()
        return total_charge
    
    def removeAllProperties(self, molecule):
        names= []
        for prop in molecule.iterateProperties():
            names.append(prop.name())
        for name in names:
            molecule.removeProperty(name)
            
    def renderMolecule(self, molecule, filename):
        renderer = IndigoRenderer(self.indigo)
        self.indigo.setOption("render-output-format", "png")
        self.indigo.setOption("render-margins", 10, 10)
        self.indigo.setOption("render-background-color", 1.0, 1.0, 1.0);
        molecule.layout()
        self.indigo.setOption("render-comment", molecule.name())
        renderer.renderToFile(molecule, filename)
        
    def renderMolecules(self, molecules, columns, filename):
        renderer = IndigoRenderer(self.indigo)
        self.indigo.setOption("render-output-format", "png")
        self.indigo.setOption("render-margins", 10, 10)
        self.indigo.setOption("render-grid-margins", 30, 30)
        self.indigo.setOption("render-background-color", 1.0, 1.0, 1.0);
        arr = self.indigo.createArray()
        for molecule in molecules:
            arr.arrayAdd(molecule);
        renderer.renderGridToFile(arr, None, columns, filename)
        
    def trimInchi(self, inchi):
        return inchi.split('/t')[0].split('/b')[0]
        
    # fetches SMILES by name from one source
    def fetchCanonicalSMILESbyNameFast(self, molecule_name):
        print "Fetching SMILES by name: " + molecule_name
        myfix = molecule_name.replace('_', ' ')
        myfix = myfix.decode('utf-8')
        myfix = myfix.replace(u'«', '\'')
        response = urllib2.urlopen('http://cactus.nci.nih.gov/chemical/structure/' + url_fix(myfix) + '/stdinchikey')
        return response.read()  
        
    # fetches SMILES by name from three sources: OP 
    def fetchCanonicalSMILESbyName(self, molecule_name):
        print "Fetching SMILES by name: " + molecule_name
        myfix = molecule_name.replace('_', ' ')
        myfix = myfix.decode('utf-8')
        myfix = myfix.replace(u'«', '\'')
        response = urllib2.urlopen('http://cactus.nci.nih.gov/chemical/structure/' + url_fix(myfix) + '/smiles/xmls?resolver=name_by_chemspider,name_by_opsin,name_by_cir')
        text = response.read()
        root = fromstring(text)
        cs = []
        for i in range(0, len(root)):
            print "smiles: " + root[i][0].text
            m = self.indigo.loadMolecule(root[i][0].text)
            m.aromatize()
            canonical_smiles = m.canonicalSmiles()
            cs.append(canonical_smiles)
            print "canonical: " + canonical_smiles
        if len(root) == 0:
            return "Err: None returned from query"
        elif len(root) == 1:
            return cs[0]
        elif len(root) == 2:
            if cs[0] == cs[1]:
                return cs[0]
            else:
                return "Err: Only two returned and their canonical SMILES don't match"
        elif len(root) == 3:
            if cs[0] == cs[1]:
                return cs[0]
            elif cs[1] == cs[2]:
                return cs[1]
            elif cs[0] == cs[2]:
                return cs[0]
            else:
                return "Err: Three returned but there are no pairs whos canonical SMILES match"
        else:
            for i in range(0, len(root)):
                if root[i].attrib['string_class'] == "IUPAC Name (OPSIN)":
                    return cs[i]
        return "Err: More than three returned with no OPSIN option"
    
    def fetchCanonicalSMILESbySLN(self, SLN):
        print "Fetching SMILES by SLN: " + SLN
        myfix = SLN.replace('_', ' ')
        myfix = SLN.replace('#', '%23')
        response = urllib2.urlopen('http://cactus.nci.nih.gov/chemical/structure/' + URLFetchingHelpers.url_fix(myfix) + '/smiles')
        text = response.read()
        print "smiles: " + text
        m = self.indigo.loadMolecule(text)
        m.aromatize()
        canonical_smiles = m.canonicalSmiles()
        print "canonical: " + canonical_smiles
        return canonical_smiles
        
    # fetches SMILES by name, if error occurs, returns SLN SMILES if exists, otherwise returns the error from the name fetch
    # if no error, then compares and returns error only if different
    def fetchCanonicalSMILESbyNameAndSLN(self, molecule_name, SLN):
        nameSMILES = self.fetchCanonicalSMILESbyName(molecule_name)
        SLNSMILES = self.fetchCanonicalSMILESbySLN(SLN)
        
        if nameSMILES[0:4] == "Err:":
            if SLNSMILES != "":
                if "." in SLNSMILES:
                    return "Err: dots in SLNSMILES and no SMILES for name"
                else:
                    return SLNSMILES
            else:
                return nameSMILES
        else:
            if nameSMILES == SLNSMILES:
                return nameSMILES
            else:
                if "." in SLNSMILES:
                    print "dots in SLNSMILES"
                    return nameSMILES
                else:
                    return "Err: SMILES fetched by name and SMILES fetched by SLN don't match"
                
    def fetchMiLogP(self, SMILES):
        print "Fetching MiLogP by SMILES: " + SMILES
        myfix = SMILES.replace('#', '%23')
        print URLFetchingHelpers.url_fix(myfix)
        response = urllib2.urlopen('http://www.molinspiration.com/cgi-bin/properties?smiles=' + URLFetchingHelpers.url_fix(myfix) + '&out=text')
        text = response.read()
        return text.splitlines(True)[4].split()[1]
        
        #print "smiles: " + text
        #m = self.indigo.loadMolecule(text)
        #m.aromatize()
        #canonical_smiles = m.canonicalSmiles()
        #print "canonical: " + canonical_smiles
        #return canonical_smiles