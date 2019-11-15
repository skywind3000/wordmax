import sys
import time
import config
import ascmini
import resource
import wordkit

if False:
    sys.path.append('../lib')

def test1():
    book = wordkit.WordBook('dictation.txt')
    if len(book) <= 0:
        print('empty input in dictation.txt')
        return 0
    # words = ['by cash', 'hello', 'hello2']
    words = resource.utils.disorder(book)
    # words = words[:12]
    fp = open('output.txt', 'w')
    size = len(words)
    ngroup = (size + 9) // 10
    for group in range(ngroup):
        print('- Group %d/%d:'%(group + 1, ngroup))
        fp.write('- Group %d:\n'%(group + 1))
        resource.utils.tts_say('group %d'%(group + 1))
        time.sleep(4)
        for i in range(10):
            index = group * 10 + i
            if index >= size:
                break
            word = words[index]
            print(word)
            resource.utils.say(word)
            fp.write(word + '\n')
            time.sleep(4)
        print()
        fp.write('\n')
        fp.flush()
        input('press enter to continue ...')
        print()
    return 0


def test2():
    resource.utils.say('dates')
    return 0


#----------------------------------------------------------------------
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    test1()



