import os
sumCount = 0
for filename in os.listdir(r'E:\pythonProject\ruisi'):
    if filename.startswith('unkownsex'):
        count = 0
        newName = 'E:\\pythonProject\\ruisi\\%s' % (filename)
        readFile = open(newName,'r')
        for line in open(newName):
            count += 1
            sumCount +=1
        print "%s deal %s lines" %(filename, count)
print '%s unkowns sex' %(sumCount)


