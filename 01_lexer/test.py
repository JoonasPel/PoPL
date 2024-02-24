'''
THIS FILE IS FOR MY LOCAL TESTING ONLY! Not purposed to be usable elsewhere or
anything!
I made this to tokenize and validate all testing files automatically.
'''

import subprocess
import os

def GetTestFileNames(path):
    dirList = os.listdir(path)
    names = set()
    for file in dirList:
        parsedName = file[:file.find('.')]
        names.add(parsedName)
    return names

if __name__ == '__main__':
    currentPath = os.getcwd()
    EnvPath = os.path.join(currentPath, r'venv\Scripts\activate')
    testFilesBasePath = r'public_examples-main-01_lexer\01_lexer'
    testFileNames = GetTestFileNames(testFilesBasePath)

    for testFileName in testFileNames:
        print(f"\nTESTING WITH FILE {testFileName}")
        inputFile = os.path.join(testFilesBasePath, testFileName) + ".ph"
        expectedOutputFile = os.path.join(testFilesBasePath, testFileName) + ".output"
        # get token from input file
        cmd = f'{EnvPath} && python main.py --file {inputFile}'
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, _ = process.communicate()
        lines = output.decode('utf-8').split('\r\n')
        # read expected output file
        with open(expectedOutputFile, 'r') as expectedOutput:
            temp = expectedOutput.read()
            lines2 = temp.split('\n')
        # compare
        for x in range(0, min(len(lines), len(lines2))):
            if (lines[x] == lines2[x]):
                pass
            else:
                print(f"expected: {lines2[x]}")
                print(f"got: {lines[x]}\n")
        if (len(lines2) != len(lines)):
            print(f"DIFFERENT SIZE FOUND! expected: {lines2}, got {lines}")
