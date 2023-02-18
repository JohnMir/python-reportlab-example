# TODO color terminal window

dragged_input = input('Drag photos into terminal')

replacespace = dragged_input.replace('\\ ','SPACECHAR').strip()
inputsplit = replacespace.split(' ')

print(f'Photos {len(inputsplit)}')
for i in inputsplit:
    print(i)


#myfile = myfile.replace('\\ ', ' ').strip()
#os.path.exists(myfile)

#if __name__ == '__main__':
 #   print('hi')
print('done')