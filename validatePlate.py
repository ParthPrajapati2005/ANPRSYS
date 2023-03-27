def validatePlate(plate):
    plateValid = True
    
    #Length of string
    if(len(plate) != 8):
        plateValid == False

    #First 2 letters
    first2Chars = str(plate[0:2])
    for x in first2Chars:
        if(ord(str(x)) not in range(65,90)):
            plateValid = False
    
    #Third and Fourth numbers
    numbers = str(plate[2:4])
    for y in numbers:
        if(ord(str(y)) not in range(48,57)):
            plateValid = False

    #Space
    if (plate[4].isspace() == False):
        plateValid = False

    #Last 3 Chars
    threeChars = str(plate[5:8])
    for z in threeChars:
        if(ord(str(z)) not in range(65,91)):
            plateValid = False

    if plateValid == True:
        return True
    else:
        return False

#numberPlate = str(input("What is the plate you wish to validate"))
#try1 = validatePlate(numberPlate)

a = "AB12 XYZ"

print(a[3:8])