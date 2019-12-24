# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 16:56:25 2019

@author: Samuel P. Sellberg
"""

import sys
import logging
sys.path.insert(0, 'D:\Dokument D\Python Scripts')
import Protein_Conformational_Adaptation

logger = logging.getLogger('PCA_logger')
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    error_handler = logging.StreamHandler()
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter('%(levelname)s >> %(message)s'))
    logger.addHandler(error_handler)
    debug_handler = logging.FileHandler('PCA.log',mode='w')
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(logging.Formatter('%(name)s: %(levelname)s >> %(message)s'))
    logger.addHandler(debug_handler)


logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')


debug_handler.close()


"""
handlers = logger.handlers[:]
for handler in handlers:
    handler.close()
    logger.removeHandler(handler)
"""

"""
# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

logger.warning('This is a warning')
logger.error('This is an error')
"""