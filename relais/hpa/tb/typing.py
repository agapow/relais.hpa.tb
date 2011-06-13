#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data structures for handling TB loci and typing data.

Different loci are used in different schemes for Tb typing, with some of the
same loci being used under different names. Dreadful. So this converts names
to useful or familar forms when necessary.

These are the loci used according to VNTR-plus::

	Loci   Alias 1  Alias 2   24    15   12    
	154    MIRU02             X          X
	424    Mtub04             X     X     
	577    ETRC               X     X     
	580    MIRU04   ETRD      X     X    X
	802    MIRU40             X     X    X
	960    MIRU10             X     X    X
	1644   MIRU16             X     X    X
	1955   Mtub21             X     X     
	2059   MIRU20             X          X
	2163b  QUB11b             X     X     
	2165   ETRA               X     X     
	2347   Mtub29             X           
	2401   Mtub30             X     X     
	2461   ETRB               X         
	2531   MIRU23             X          X
	2687   MIRU24             X          X
	2996   MIRU26             X     X    X
	3007   MIRU27    QUB5     X          X
	3171   Mtub34             X         
	3192   MIRU31    ETRE     X     X    X
	3690   Mtub39             X     X     
	4052   QUB26              X     X     
	4156   QUB4156            X     X     
	4348   MIRU39             X          X

This appears to be the VNTRPLUS_24 order.

Things get even more complicated, because ETR-E is MIRU-31, while MIRU-4 can be
calculated from ETR-D (MIRU-4 = ETR-D - 1). Now:

	ETR
		ETR-A, ETR-B, ETR-C, ETR-D, ETR-E
	MIRU
		MIRU-2, MIRU-4, MIRU-10, MIRU-16, MIRU-20, MIRU-23, MIRU-24, MIRU-26,
		MIRU-27, MIRU-31, MIRU-39, MIRU-40
	VNTR
		ETR-A, ETR-B, ETR-C, ETR-D, ETR-E, MIRU-2, MIRU-10, MIRU-16, MIRU-20,
		MIRU-23, MIRU-24, MIRU-26, MIRU-27, MIRU-39, MIRU-40


"""


### IMPORTS

import defs


### CONSTANTS & DEFINES

### IMPLEMENTATION ### 

class TbType (object):
	# The loci data are stored internally in a hash, under their most canonical
	# name, which is the location (number) or the loci as a string. All other
	# names are translated to this form before access.

	def __init__ (self, data=None, scheme=None, ambig_sym='-'):
		"""
		C'tor, setting loci as ambiguous.
		
		For example::
		
			>>> tbt = TbType()
			>>> len (tbt._data) == len (LOCI)
			True
			
		"""
		self._data = dict ([(x[0], None) for x in LOCI])
		self.ambig_sym = ambig_sym
		if data:
			self.from_string (data, scheme)
		
	def __getitem__ (self, loci):
		"""
		Access a loci value under one of its many names.
		
		For example::
		
			>>> tbt = TbType()
			>>> tbt['ETR-D'] is None
			True
			>>> tbt['ETR-D'] = 5
			>>> tbt['etrd']
			5
			>>> tbt['ETR-D'] == tbt['580'] == tbt['MIRU-04']
			True
			
		"""
		return self._data[LOCI_TO_INDEX[normalize_name(loci)]]
		
	def __setitem__ (self, loci, value):
		"""
		Set a loci value under one of its many names.
			
		For example::
		
			>>> tbt = TbType()
			>>> tbt['VNTR-4156'] is None
			True
			>>> tbt['VNTR-4156'] = 5
			>>> tbt['VNTR-4156']
			5
			>>> tbt['VNTR-4156'] = 'a'
			>>> tbt['VNTR-4156']
			10
			
		"""
		if isinstance (value, basestring):
			value = self.alpha_to_int(value.upper())
		else:
			assert (isinstance (value, int))
			assert (0 < value)
		self._data[LOCI_TO_INDEX[normalize_name(loci)]] = value
		
	def contains_ambigs (self):
		"""
		Are any of the loci ambiguous (i.e. undefined).
			
		For example::
		
			>>> tbt = TbType()
			>>> tbt.contains_ambigs()
			True
			
		"""
		return (None in self._data.values())
		
	def from_string (self, s, scheme=None):
		"""
		Set the contents (loci) from the characters of this string.
		
		:Parameters:
			s
				A loci string, e.g. '3481096A2C22806'
			scheme
				An array giving the names and order of the loci in the string
		
		For example::
		
			>>> tbt = TbType()
			>>> tbt.from_string('3481096A2C22806')
			>>> tbt['etr-a']
			3
			>>> tbt['miru-40']
			6
			>>> tbt['miru-16']
			10
			
		"""
		# TODO: sniff the format
		## Preconditions:
		if scheme is None:
			if len(s) == 24:
				scheme = NMRL_24
			if len(s) == 15:
				scheme =  NMRL_15
			else:
				assert (false)
		assert (len(s) == len(scheme)), "scheme length doesn't equal string length"
		# clear current values
		for k in self._data.keys():
			self._data[k] = None
		## Main:
		for i, k in enumerate(scheme):
			self[k] = s[i]
			
	def to_string (self, scheme=None):
		"""
		Get the contents (loci values) as a string.
		
		:Parameters:
			scheme
				An array giving the names and order of the loci in the string
			
		For example::
		
			>>> tbt = TbType()
			>>> tbt.from_string('3481096A2C22806')
			>>> tbt.to_string(NMRL_15)
			'3481096A2C22806'
			>>> tbt.to_string()
			'3481096A2C22806---------'
			
		"""
		## Main:
		return ''.join ([self.int_to_alpha(x) for x in self.to_array(scheme)])
		
	def to_array (self, scheme=None):
		"""
		Get the contents (loci values) as an array of integers.
		
		:Parameters:
			scheme
				An array giving the names and order of the loci in the string
				
		For example::
		
			>>> tbt = TbType()
			>>> tbt.from_string('3481096A2C22806')
			>>> tbt.to_array(NMRL_15)
			[3, 4, 8, 1, 0, 9, 6, 10, 2, 12, 2, 2, 8, 0, 6]
			>>> tbt.to_array()
			[3, 4, 8, 1, 0, 9, 6, 10, 2, 12, 2, 2, 8, 0, 6, None, None, None, None, None, None, None, None, None]
			
		"""
		## Preconditions:
		if scheme is None:
			scheme = NMRL_24
		## Main:
		return [self[loci] for loci in scheme]
		
	def alpha_to_int (self, c):
		"""
		Convert a character for a loci value into an integer.
		
		:Parameters:
			c
				a single character, expected to be from '123456789ABC ...' or '-'
		
		:Returns:
			an integer, from 0 upwards, or None (for unknown)
			
		This is for storing values internally as integers. Values proceed from 0 to 9
		then A, B, C for 10, 11, 12, etc.
		
		For example::
		
			>>> tbt = TbType()
			>>> [tbt.alpha_to_int(x) for x in '01569ABC']
			[0, 1, 5, 6, 9, 10, 11, 12]
			
		"""
		if (c == self.ambig_sym):
			return None
		elif '0' <= c <= '9':
			return int(c)
		else:
			return ord(c.upper()) - ord('A') + 10
	
	def int_to_alpha (self, i):
		"""
		Convert a a loci value from an integer to a character.
		
		:Parameters:
			i
				a single integer, expected to be from 0 upwards
		
		:Returns:
			a single character, from '123456789ABC ...'
			
		This is for output of loci values as strings.
		
		For example::
		
			>>> tbt = TbType()
			>>> [tbt.int_to_alpha(x) for x in range(12)]
			['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B']
			
		"""
		if (i is None):
			return self.ambig_sym
		elif (i < 10):
			return "%s" % i
		else:
			return chr(i - 10 + ord('A'))
			
	def phylo_type (self):
		if ((self['miru-39'] is 3) and
				(self['etr-a'] is 4) and
				(self['etr-c'] is 4) and
				(self['miru-39'] is 1))
			):
			return PHYLOTYPE_I_BEIJING
		elif ((self['miru-16'] in [1, 2, 3]) and
				(self['miru-39'] is 2) and
				(self['etr-b'] in [1, 2]))
			):
			return PHYLOTYPE_II_EURO_AMERICAN
		elif ((self['miru-23'] is 5) and
				(self['etr-c'] is 2))
			):
			return PHYLOTYPE_II_CAS
		elif ((self['miru-24'] is 2) and
				(self['miru-26'] is 2))
			):
			return PHYLOTYPE_II_EAI
		elif ((self['miru-10'] is 2) and
				(self['miru-40'] is 2) and
				(self['etr-c'] is 5))
			):
			return PHYLOTYPE_M_BOVIS
		elif ((self['miru-10'] >= 4) and
				(self['miru-23'] is 4) and
				(self['miru-26'] in [3, 4, 5]) and
				(self['etr-a'] >= 4))
			):
			return PHYLOTYPE_M_AFRICANUM
		elif ((self['miru-23'] is 4) and
				(self['miru-40'] is 2) and
				(self['etr-A'] >= 8))
			):
			return PHYLOTYPE_M_MICROTI
		else
			return None
		
		
		
		
## DEBUG & TEST ###

if __name__ == "__main__":
	import doctest
	doctest.testmod()


### END #######################################################################
