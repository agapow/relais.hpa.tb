#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module-wise common definitions and constants.

Largely, these are loci and typing scheme names, and the systems for translating
between them.

"""


### IMPORTS

import re


### CONSTANTS & DEFINES

# A list of loci canonical names and their various synonyms
# We use the loci number as canonical, and try to accept all other forms.
LOCI = [
	['154',   'MIRU-02', 'MIRU-2',                                             ],
	['424',                                   'VNTR-424',    'Mtub04', 'Mtub4' ],
	['577',                         'ETR-C',                                   ],
	['580',   'MIRU-04', 'MIRU-4',  'ETR-D',                                   ],
	['802',   'MIRU-40',                                                       ],
	['960',   'MIRU-10',                                                       ],
	['1644',  'MIRU-16',                                                       ],
	['1955',                                  'VNTR-1955',   'Mtub21'          ],
	['2059',  'MIRU-20',                                                       ],
	['2163b',                                 'VNTR-2163b',  'QUB11b'          ],     
	['2165',                        'ETR-A',                                   ],     
	['2347',                                  'VNTR-2347',   'Mtub29'          ],    
	['2401',                                  'VNTR-2401',   'Mtub30'          ],     
	['2461',                        'ETR-B',                                   ], 
	['2531',  'MIRU-23',                                                       ],
	['2687',  'MIRU-24',                                                       ],
	['2996',  'MIRU-26',                                                       ],
	['3007',  'MIRU-27',                                     'QUB5'            ],
	['3171',                                  'VNTR-3171',   'Mtub34'          ], 
	['3192',  'MIRU-31',            'ETR-E',                                   ],
	['3690',                                  'VNTR-3690',   'Mtub39'          ],     
	['4052',                                  'VNTR-4052',   'QUB26'           ],     
	['4156',                                  'VNTR-4156',   'QUB4156'         ],     
	['4348',  'MIRU-39',                                                       ],
]


NORM_RE = re.compile (r'[\s\-\_]+')

def normalize_name (s):
	"""
	Reduces loci names to a canonical form.
	
	For example::
	
		>>> normalize_name ('ETR-D')
		'etrd'
		>>> normalize_name (' MIRU_04 ')
		'miru04'
		
	"""
	return NORM_RE.sub ('', s.strip().lower())


# table to translate all names to their canonical form
LOCI_TO_INDEX = {}
for x in LOCI:
	for loci_name in x:
		LOCI_TO_INDEX[normalize_name(loci_name)] = x[0]

# the various typing schemes expressed as an ordered array of the loci used
ETR = ['ETR-A', 'ETR-B', 'ETR-C', 'ETR-D', 'ETR-E']
MIRU = ['MIRU-2', 'MIRU-4', 'MIRU-10', 'MIRU-16', 'MIRU-20', 'MIRU-23',
	'MIRU-24', 'MIRU-26', 'MIRU-27', 'MIRU-31', 'MIRU-39', 'MIRU-40']
VNTR = ETR + ['MIRU-2', 'MIRU-10', 'MIRU-16', 'MIRU-20', 'MIRU-23',
	'MIRU-24', 'MIRU-26', 'MIRU-27', 'MIRU-39', 'MIRU-40']
AUX = ['VNTR-424', 'VNTR-1955', 'VNTR-2163b', 'VNTR-2347', 'VNTR-2401',
'VNTR-3171', 'VNTR-3690', 'VNTR-4052', 'VNTR-4156']
	
NMRL_15 = VNTR
NMRL_24 = NMRL_15 + AUX

# phylotypes
PHYLOTYPE_I_BEIJING = "I (Beijing)"
PHYLOTYPE_II_EURO_AMERICAN = "II (Euro-american)"
PHYLOTYPE_III_CAS = "III (CAS)"
PHYLOTYPE_IV_EAI = "IV (EAI)"
PHYLOTYPE_M_BOVIS = "M. bovis"
PHYLOTYPE_M_AFRICANUM = "M. africanum"
PHYLOTYPE_M_MICROTI = "M. microti"

PHYLOTYPE_PREFIXES = {
	PHYLOTYPE_I_BEIJING:         'B',
	PHYLOTYPE_II_EURO_AMERICAN:  'E',
	PHYLOTYPE_III_CAS:           'C',
	PHYLOTYPE_IV_EAI:            'A',
	PHYLOTYPE_M_BOVIS:           'V',
	PHYLOTYPE_M_AFRICANUM:       'F',
	PHYLOTYPE_M_MICROTI:         'M',
	None:                        'U',
}



### IMPLEMENTATION ### 

## DEBUG & TEST ###

if __name__ == "__main__":
	import doctest
	doctest.testmod()


### END #######################################################################
