import configuration as conf

from rabaDB.setup import *
RabaConfiguration(conf.pyGeno_RABA_NAMESPACE, conf.pyGeno_RABA_DBFILE)
from rabaDB.Raba import *
import rabaDB.fields as rf

from tools import UsefulFunctions as uf
from tools.BinarySequence import AABinarySequence
import copy

class Protein(Raba) :
	_raba_namespace = conf.pyGeno_RABA_NAMESPACE
	
	id = rf.Primitive()
	name = rf.Primitive()
	
	genome = rf.RabaObject('Genome')
	chromosome = rf.RabaObject('Chromosome')
	gene = rf.RabaObject('Gene')
	transcript = rf.RabaObject('Transcript')
	
	_raba_uniques = [('genome', 'id')]
	
	def __init__(self, importing = False) :
		if not importing :
			self.sequence = uf.translateDNA(self.transcript.CDNA[:-3])
			self.binarySequence = AABinarySequence(self.sequence)
		
	def _curate(self) :
		pass
	
	def getSequence(self):
		return self.sequence
	
	def getDefaultSequence(self) :
		"""returns a version str sequence where only the last allele of each polymorphisms is shown"""
		return self.binarySequence.defaultSequence
	
	def getPolymorphisms(self) :
		return self.binarySequence.getPolymorphisms()

	def find(self, sequence):
		"""Returns the first occurence of sequence taking polymorphisme into account this is slower than the simple string search findString"""
		if self.updateBinarySequence :
			self.binarySequence = AABinarySequence(self.sequence)
			self.updateBinarySequence = False
		return self.binarySequence.find(sequence)

	def findAll(self, sequence):
		"""Returns all occurences of sequence taking polymorphisme into account this slower than the simple string search findStringAll"""
		if self.updateBinarySequence :
			self.binarySequence = AABinarySequence(self.sequence)
			self.updateBinarySequence = False
		return self.binarySequence.findAll(sequence)

	def findString(self, sequence) :
		"""return the first occurence of sequence using simple string search in sequence doesn't care about polymorphisme"""
		return self.sequence.find(sequence)

	def findStringAll(self, sequence):
		"""return all first occurences of sequence using simple string search in sequence doesn't care about polymorphisme"""
		return uf.findAll(self.sequence, sequence)
	
	def pluck(self) :
		"""Returns a plucked object. Plucks the protein off the tree, set the value of self.transcript into str(self.transcript). This effectively disconnects the object and
		makes it much more lighter in case you'd like to pickle it"""
		e = copy.copy(self)
		e.transcript = str(self.transcript)
		return e
		
	def __getitem__(self, i) :
		return self.binarySequence.getChar(i)

	def __len__(self) :
		return len(self.binarySequence)

	def __str__(self) :
		return "Protein, id: %s > %s" %(self.id, str(self.transcript))
