## the main test 

import sys
import platform
## In next line .. why 1? 
sys.path.insert(1, 'lib/' + platform.system())
## because 0 is the current directory
import random

from imageModel import ImageModel
from modesEnum import Modes
from task3Test import Task3Test

def generateRandomPercentage():
    return round(random.uniform(0.0, 1.0), 2)

# Assign vaild paths to the following 2 variables
image1Path : str = "results/test.jpg"
image2Path : str = "results/test2.jpg"

# this format --> 'variable : variableType' is called annotation
# as you have noticed, python is not a static typed language, so many errors can happen by passing a different type than the expected one to a function
# type annotations can help you not to do this terrible mistake

test = Task3Test(image1Path, image2Path, ImageModel)
test.testMagAndPhaseMode(generateRandomPercentage(), generateRandomPercentage())
test.testRealAndImagMode(generateRandomPercentage(), generateRandomPercentage())