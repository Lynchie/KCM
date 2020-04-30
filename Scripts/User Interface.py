import time
from Process import test

def printOneByOne(message, delay=0,end=''):

    for character in message:
        print(character,end=end)
        time.sleep(delay)


def analyseSheet():
    test(True,False)
    pass
def classifySheet():
    pass
def analyseManySheets():
    test(True,True)
    pass
def showSheet():
    test(False,False)
    pass


def main():

    menuOptions = ['Analyse whole sheet',
                   'Classify whole sheet',
                   'Analyse multiple sheets',
                   'Show and analyse specific symbols']

    menuFunctions = [analyseSheet,
                     classifySheet,
                     analyseManySheets,
                     showSheet]

    printOneByOne('\n\n',delay=0.03)
    printOneByOne('-~-~-~-~ KCM User Interface ~-~-~-~-',delay=0.03)
    printOneByOne('\n\n\n',delay = 0.3)

    while True:

        print('Menu:')
        for i in range(len(menuOptions)):
            print( '{}: {}'.format(i,menuOptions[i]) )

        print()
        choice = ''
        while choice not in [str(i) for i in range(len(menuOptions))]:
            choice = input('Enter option: ')

        choice = int(choice)
        print()
        menuFunctions[choice]()















if __name__ == '__main__':
    main()
