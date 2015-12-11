#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
pattern = re.compile("([A-Z])$")
patternQuots = re.compile("[\"]")
patternNewLine = re.compile("[\n]")

pattern = re.compile("([A-Z])")

my_final_words = []
my_final_diff = []
my_search_word = []
my_wrd_arr = []
my_dif_arr = []
index_arr = []
str = u""
myindex = 0

def key_count(cipher):
    global nl, N
    print cipher
    global my_final_diff
    global my_search_word
    global my_wrd_arr
    global my_dif_arr
    global index_arr
    global str
    global myindex
    cipherLetters = u""
    for i in range(cipher.__len__()):
        if i > 4000:
            break
        if pattern.match(cipher[i]):
             cipherLetters += cipher[i]
    print cipherLetters
    arr_index = 0
    word_lenght = 3
    for i in range(cipherLetters.__len__() - word_lenght):
        my_search_word.append(cipherLetters[i:i + word_lenght])
        if i == cipherLetters.__len__() - word_lenght:
            i = 0
            word_lenght += 1
        arr_index += 1
        if word_lenght > 5:
            break

    for i in range(my_search_word.__len__()):
        index_arr.append([])
        str = my_search_word[i]
        myindex = cipherLetters.find(str)
        while myindex != -1:
            index_arr[i].append(myindex)
            myindex += 1
            myindex = cipherLetters.find(str, myindex)
    # for i in range(index_arr.__len__()):
    #     if index_arr[i] == -1:
    #         continue
    #     for j in range(index_arr[i].__len__() - 1):
    #         index_arr[index_arr[i][j + 1]] = -1
    # for i in range(index_arr.__len__()):
    #     if index_arr[i] == -1:
    #         continue
    #     if index_arr[i].__len__() == 1:
    #         index_arr[i][0] = -1
    wrd = 0
    for i in range(index_arr.__len__()):
        if index_arr[i] != -1:
            my_dif_arr.append([])
            my_wrd_arr.append(my_search_word[i])
            for z in range(index_arr[i].__len__() - 1):
                ind1 = index_arr[i][z]
                ind2 = index_arr[i][z + 1]
                diff = ind2 - ind1
                my_dif_arr[wrd].append(diff)
            wrd += 1

    for i in range(my_wrd_arr.__len__()):
        if my_wrd_arr[i] != -1:
            if my_dif_arr[i].__len__() != 0:
                my_final_diff.append(my_dif_arr[i])
    # print my_final_diff
    my_factor = []
    for j in range(my_final_diff.__len__()):
        for k in range(my_final_diff[j].__len__()):
            num = my_final_diff[j][k]
            c_num = 20
            if num > 20:
                c_num = num
            for i in range(2, c_num):
                if num % i == 0:
                    try:
                        my_factor[i] += 1
                    except IndexError:
                        for _ in range (i - len(my_factor) + 1):
                            my_factor.append(0)
                        my_factor[i] += 1
    print my_factor
    first_max = max(my_factor)
    first_max_i = my_factor.index(first_max)
    current_i = first_max_i
    i = 2
    prev_max = first_max
    next_max = sorted(my_factor)[-i]
    next_max_i = my_factor.index(next_max)
    while i != -1:
        if float(next_max) / float(prev_max) >= 0.8 and (next_max_i > current_i or float(next_max) / float(prev_max) >= 0.95):
            i += 1
            current_i = next_max_i
            prev_max = next_max
            next_max = sorted(my_factor)[-i]
            next_max_i = my_factor.index(next_max)
        else:
            i = -1
    print current_i
    sorted_indexes = []
    sorted_indexes.append(current_i)
    sorted_indexes.append(first_max_i)
    prev_max = first_max
    prev_max_i = first_max_i
    for i in range(2, len(my_factor)):
        next_max = sorted(my_factor)[-i]
        next_max_i = my_factor.index(next_max)
        print next_max
        print prev_max
        if float(next_max) / float(prev_max) >= 0.5 and (next_max_i > prev_max_i or float(next_max) / float(prev_max) >= 0.95):
            prev_max = next_max
            prev_max_i = next_max_i
            sorted_indexes.append(next_max_i)
        else:
            break
    print sorted_indexes
    if sorted_indexes[0] == sorted_indexes[-1]:
        print [sorted_indexes[0]]
        return [sorted_indexes[0]]
    else:
        print sorted_indexes[1:sorted_indexes.__len__()]
        return sorted_indexes[1:sorted_indexes.__len__()]

def deleteChangeBadSymbols(text):
    text = re.sub(patternQuots, '', text)
    text = re.sub(patternNewLine, ' ', text)
    return text


def cipher(text, key):
    global pattern
    text = text.upper()
    key = key.upper()
    cipherText = u""
    keyLen = key.__len__()
    keyInt = []
    for i in range(keyLen):
        keyInt.append(ord(key[i]) - ord(u'A'))
    print keyInt

    ordOfZChar = ord(u'Z')
    offset = 0

    for i in range(text.__len__()):
        j = (i - offset) % keyLen
        if pattern.match(text[i]):
            newOrd = ord(text[i]) + keyInt[j]
            if newOrd > ordOfZChar:
                newOrd -= 26
            cipherText += chr(newOrd)
        else:
            offset += 1
            cipherText += text[i]

    # print(text)
    print(cipherText)
    return cipherText

def calculateLettersRate(cipher, keyLen):
    print cipher
    cipherLetters = u""
    for i in range(cipher.__len__()):
         if pattern.match(cipher[i]):
             cipherLetters += cipher[i]


    print cipherLetters
    lettersCount = []
    for j in range(keyLen):
        lettersCount.append({})
        for i in range(ord('A'), ord('Z') + 1, 1):
            lettersCount[j][chr(i)] = 0



    for i in range(cipherLetters.__len__()):
        lettersCount[i % keyLen][cipherLetters[i]] += 1
        # print(cipherLetters[i])
        # print i

    print(lettersCount)
    lettersRate =  []
    for i in range(keyLen):
        temp = sorted(lettersCount[i], key=lettersCount[i].__getitem__, reverse=True)
        letters = u""
        for i in range(len(temp)):
            letters += temp[i]
        lettersRate.append(letters)

    return lettersRate




if __name__ == '__main__':
    text = u"Scrooge was better than his word. He did it all, and infinitely more; and to Tiny Tim, who did not die, he was a second father. He became as good a friend, as good a master, and as good a man, as the good old city knew, or any other good old city, town, or borough, in the good old world. Some people laughed to see the alteration in him, but he let them laugh, and little heeded them; for he was wise enough to know that nothing ever happened on this globe, for good, at which some people did not have their fill of laughter in the outset; and knowing that such as these would be blind anyway, he thought it quite as well that they should wrinkle up their eyes in grins, as have the malady in less attractive forms. His own heart laughed: and that was quite enough for him. He had no further intercourse with Spirits, but lived upon the Total Abstinence Principle, ever afterwards; and it was always said of him, that he knew how to keep Christmas well, if any man alive possessed the knowledge. May that be truly said of us, and all of us! And so, as Tiny Tim observed, God bless Us, Every One!"
    textArtem = u"THAT RUTH HAD LITTLE FAITH IN HIS POWER AS A WRITER, DID NOT ALTER HER NOR DIMINISH HER IN MARTIN’S EYES. IN THE BREATHING SPELL OF THE VACATION HE HAD TAKEN, HE HAD SPENT MANY HOURS IN SELF-ANALYSIS, AND THEREBY LEARNED MUCH OF HIMSELF. HE HAD DISCOVERED THAT HE LOVED BEAUTY MORE THAN FAME, AND THAT WHAT DESIRE HE HAD FOR FAME WAS LARGELY FOR RUTH’S SAKE. IT WAS FOR THIS REASON THAT HIS DESIRE FOR FAME WAS STRONG. HE WANTED TO BE GREAT IN THE WORLD’S EYES; TO MAKE GOOD, AS HE EXPRESSED IT, IN ORDER THAT THE WOMAN HE LOVED SHOULD BE PROUD OF HIM AND DEEM HIM WORTHY.   AS FOR HIMSELF, HE LOVED BEAUTY PASSIONATELY, AND THE JOY OF SERVING HER WAS TO HIM SUFFICIENT WAGE. AND MORE THAN BEAUTY HE LOVED RUTH. HE CONSIDERED LOVE THE FINEST THING IN THE WORLD. IT WAS LOVE THAT HAD WORKED THE REVOLUTION IN HIM, CHANGING HIM FROM AN UNCOUTH SAILOR TO A STUDENT AND AN ARTIST; THEREFORE, TO HIM, THE FINEST AND GREATEST OF THE THREE, GREATER THAN LEARNING AND ARTISTRY, WAS LOVE. ALREADY HE HAD DISCOVERED THAT HIS BRAIN WENT BEYOND RUTH’S, JUST AS IT WENT BEYOND THE BRAINS OF HER BROTHERS, OR THE BRAIN OF HER FATHER. IN SPITE OF EVERY ADVANTAGE OF UNIVERSITY TRAINING, AND IN THE FACE OF HER BACHELORSHIP OF ARTS, HIS POWER OF INTELLECT OVERSHADOWED HERS, AND HIS YEAR OR SO OF SELF-STUDY AND EQUIPMENT GAVE HIM A MASTERY OF THE AFFAIRS OF THE WORLD AND ART AND LIFE THAT SHE COULD NEVER HOPE TO POSSESS.   ALL THIS HE REALIZED, BUT IT DID NOT AFFECT HIS LOVE FOR HER, NOR HER LOVE FOR HIM. LOVE WAS TOO FINE AND NOBLE, AND HE WAS TOO LOYAL A LOVER FOR HIM TO BESMIRCH LOVE WITH CRITICISM. WHAT DID LOVE HAVE TO DO WITH RUTH’S DIVERGENT VIEWS ON ART, RIGHT CONDUCT, THE FRENCH REVOLUTION, OR EQUAL SUFFRAGE? THEY WERE MENTAL PROCESSES, BUT LOVE WAS BEYOND REASON; IT WAS SUPERRATIONAL. HE COULD NOT BELITTLE LOVE. HE WORSHIPPED IT. LOVE LAY ON THE MOUNTAIN-TOPS BEYOND THE VALLEY-LAND OF REASON. IT WAS A SUBLIMATES CONDITION OF EXISTENCE, THE TOPMOST PEAK OF LIVING, AND IT CAME RARELY. THANKS TO THE SCHOOL OF SCIENTIFIC PHILOSOPHERS HE FAVORED, HE KNEW THE BIOLOGICAL SIGNIFICANCE OF LOVE; BUT BY A REFINED PROCESS OF THE SAME SCIENTIFIC REASONING HE REACHED THE CONCLUSION THAT THE HUMAN ORGANISM ACHIEVED ITS HIGHEST PURPOSE IN LOVE, THAT LOVE MUST NOT BE QUESTIONED, BUT MUST BE ACCEPTED AS THE HIGHEST GUERDON OF LIFE. THUS, HE CONSIDERED THE LOVER BLESSED OVER ALL CREATURES, AND IT WAS A DELIGHT TO HIM TO THINK OF GOD’S OWN MAD LOVER, RISING ABOVE THE THINGS OF EARTH, ABOVE WEALTH AND JUDGMENT, PUBLIC OPINION AND APPLAUSE, RISING ABOVE LIFE ITSELF AND DYING ON A KISS.   MUCH OF THIS MARTIN HAD ALREADY REASONED OUT, AND SOME OF IT HE REASONED OUT LATER. IN THE MEANTIME HE WORKED, TAKING NO RECREATION EXCEPT WHEN HE WENT TO SEE RUTH, AND LIVING LIKE A SPARTAN. HE PAID TWO DOLLARS AND A HALF A MONTH RENT FOR THE SMALL ROOM HE GOT FROM HIS PORTUGUESE LANDLADY, MARIA SILVA, A VIRAGO AND A WIDOW, HARD WORKING AND HARSHER TEMPERED, REARING HER LARGE BROOD OF CHILDREN SOMEHOW, AND DROWNING HER SORROW AND FATIGUE AT IRREGULAR INTERVALS IN A GALLON OF THE THIN, SOUR WINE THAT SHE BOUGHT FROM THE CORNER GROCERY AND SALOON FOR FIFTEEN CENTS. FROM DETESTING HER AND HER FOUL TONGUE AT FIRST, MARTIN GREW TO ADMIRE HER AS HE OBSERVED THE BRAVE FIGHT SHE MADE. THERE WERE BUT FOUR ROOMS IN THE LITTLE HOUSE-THREE, WHEN MARTIN’S WAS SUBTRACTED. ONE OF THESE, THE PARLOR, GAY WITH AN INGRAIN CARPET AND DOLOROUS WITH A FUNERAL CARD AND A DEATH-PICTURE OF ONE OF HER NUMEROUS DEPARTED BABES, WAS KEPT STRICTLY FOR COMPANY. THE BLINDS WERE ALWAYS DOWN, AND HER BAREFOOTED TRIBE WAS NEVER PERMITTED TO ENTER THE SACRED PRECINCT SAVE ON STATE OCCASIONS. SHE COOKED, AND ALL ATE, IN THE KITCHEN, WHERE SHE LIKEWISE WASHED, STARCHED, AND IRONED CLOTHES ON ALL DAYS OF THE WEEK EXCEPT SUNDAY; FOR HER INCOME CAME LARGELY FROM TAKING IN WASHING FROM HER MORE PROSPEROUS NEIGHBORS. REMAINED THE BEDROOM, SMALL AS THE ONE OCCUPIED BY MARTIN, INTO WHICH SHE AND HER SEVEN LITTLE ONES CROWDED AND SLEPT. IT WAS AN EVERLASTING MIRACLE TO MARTIN HOW IT WAS ACCOMPLISHED, AND FROM HER SIDE OF THE THIN PARTITION HE HEARD NIGHTLY EVERY DETAIL OF THE GOING TO BED, THE SQUALLS AND SQUABBLES, THE SOFT CHATTERING, AND THE SLEEPY, TWITTERING NOISES AS OF BIRDS. ANOTHER SOURCE OF INCOME TO MARIA WERE HER COWS, TWO OF THEM, WHICH SHE MILKED NIGHT AND MORNING AND WHICH GAINED A SURREPTITIOUS LIVELIHOOD FROM VACANT LOTS AND THE GRASS THAT GREW ON EITHER SIDE THE PUBLIC SIDE WALKS, ATTENDED ALWAYS BY ONE OR MORE OF HER RAGGED BOYS, WHOSE WATCHFUL GUARDIANSHIP CONSISTED CHIEFLY IN KEEPING THEIR EYES OUT FOR THE POUNDMEN.   IN HIS OWN SMALL ROOM MARTIN LIVED, SLEPT, STUDIED, WROTE, AND KEPT HOUSE. BEFORE THE ONE WINDOW, LOOKING OUT ON THE TINY FRONT PORCH, WAS THE KITCHEN TABLE THAT SERVED AS DESK, LIBRARY, AND TYPE-WRITING STAND. THE BED, AGAINST THE REAR WALL, OCCUPIED TWO-THIRDS OF THE TOTAL SPACE OF THE ROOM. THE TABLE WAS FLANKED ON ONE SIDE BY A GAUDY BUREAU, MANUFACTURED FOR PROFIT AND NOT FOR SERVICE, THE THIN VENEER OF WHICH WAS SHED DAY BY DAY. THIS BUREAU STOOD IN THE CORNER, AND IN THE OPPOSITE CORNER, ON THE TABLE’S OTHER FLANK, WAS THE KITCHEN-THE OIL-STOVE ON A DRY-GOODS BOX, INSIDE OF WHICH WERE DISHES AND COOKING UTENSILS, A SHELF ON THE WALL FOR PROVISIONS, AND A BUCKET OF WATER ON THE FLOOR. MARTIN HAD TO CARRY HIS WATER FROM THE KITCHEN SINK, THERE BEING NO TAP IN HIS ROOM. ON DAYS WHEN THERE WAS MUCH STEAM TO HIS COOKING, THE HARVEST OF VENEER FROM THE BUREAU WAS UNUSUALLY GENEROUS. OVER THE BED, HOISTED BY A TACKLE TO THE CEILING, WAS HIS BICYCLE. AT FIRST HE HAD TRIED TO KEEP IT IN THE BASEMENT; BUT THE TRIBE OF SILVA, LOOSENING THE BEARINGS AND PUNCTURING THE TIRES, HAD DRIVEN HIM OUT. NEXT HE ATTEMPTED THE TINY FRONT PORCH, UNTIL A HOWLING SOUTHEASTER DRENCHED THE WHEEL A NIGHT-LONG. THEN HE HAD RETREATED WITH IT TO HIS ROOM AND SLUNG IT ALOFT.   A SMALL CLOSET CONTAINED HIS CLOTHES AND THE BOOKS HE HAD ACCUMULATED AND FOR WHICH THERE WAS NO ROOM ON THE TABLE OR UNDER THE TABLE. HAND IN HAND WITH READING, HE HAD DEVELOPED THE HABIT OF MAKING NOTES, AND SO COPIOUSLY DID HE MAKE THEM THAT THERE WOULD HAVE BEEN NO EXISTENCE FOR HIM IN THE CONFINED QUARTERS HAD HE NOT RIGGED SEVERAL CLOTHES-LINES ACROSS THE ROOM ON WHICH THE NOTES WERE HUNG. EVEN SO, HE WAS CROWDED UNTIL NAVIGATING THE ROOM WAS A DIFFICULT TASK. HE COULD NOT OPEN THE DOOR WITHOUT FIRST CLOSING THE CLOSET DOOR, AND VICE VERSA . IT WAS IMPOSSIBLE FOR HIM ANYWHERE TO TRAVERSE THE ROOM IN A STRAIGHT LINE. TO GO FROM THE DOOR TO THE HEAD OF THE BED WAS A ZIGZAG COURSE THAT HE WAS NEVER QUITE ABLE TO ACCOMPLISH IN THE DARK WITHOUT COLLISIONS. HAVING SETTLED THE DIFFICULTY OF THE CONFLICTING DOORS, HE HAD TO STEER SHARPLY TO THE RIGHT TO AVOID THE KITCHEN. NEXT, HE SHEERED TO THE LEFT, TO ESCAPE THE FOOT OF THE BED; BUT THIS SHEER, IF TOO GENEROUS, BROUGHT HIM AGAINST THE CORNER OF THE TABLE. WITH A SUDDEN TWITCH AND LURCH, HE TERMINATED THE SHEER AND BORE OFF TO THE RIGHT ALONG A SORT OF CANAL, ONE BANK OF WHICH WAS THE BED, THE OTHER THE TABLE. WHEN THE ONE CHAIR IN THE ROOM WAS AT ITS USUAL PLACE BEFORE THE TABLE, THE CANAL WAS UNNAVIGABLE. WHEN THE CHAIR WAS NOT IN USE, IT REPOSED ON TOP OF THE BED, THOUGH SOMETIMES HE SAT ON THE CHAIR WHEN COOKING, READING A BOOK WHILE THE WATER BOILED, AND EVEN BECOMING SKILFUL ENOUGH TO MANAGE A PARAGRAPH OR TWO WHILE STEAK WAS FRYING. ALSO, SO SMALL WAS THE LITTLE CORNER THAT CONSTITUTED THE KITCHEN, HE WAS ABLE, SITTING DOWN, TO REACH ANYTHING HE NEEDED. IN FACT, IT WAS EXPEDIENT TO COOK SITTING DOWN; STANDING UP, HE WAS TOO OFTEN IN HIS OWN WAY.   IN CONJUNCTION WITH A PERFECT STOMACH THAT COULD DIGEST ANYTHING, HE POSSESSED KNOWLEDGE OF THE VARIOUS FOODS THAT WERE AT THE SAME TIME NUTRITIOUS AND CHEAP. PEA-SOUP WAS A COMMON ARTICLE IN HIS DIET, AS WELL AS POTATOES AND BEANS, THE LATTER LARGE AND BROWN AND COOKED IN MEXICAN STYLE. RICE, COOKED AS AMERICAN HOUSEWIVES NEVER COOK IT AND CAN NEVER LEARN TO COOK IT, APPEARED ON MARTIN’S TABLE AT LEAST ONCE A DAY. DRIED FRUITS WERE LESS EXPENSIVE THAN FRESH, AND HE HAD USUALLY A POT OF THEM, COOKED AND READY AT HAND, FOR THEY TOOK THE PLACE OF BUTTER ON HIS BREAD. OCCASIONALLY HE GRACED HIS TABLE WITH A PIECE OF ROUND-STEAK, OR WITH A SOUP-BONE. COFFEE, WITHOUT CREAM OR MILK, HE HAD TWICE A DAY, IN THE EVENING SUBSTITUTING TEA; BUT BOTH COFFEE AND TEA WERE EXCELLENTLY COOKED.   THERE WAS NEED FOR HIM TO BE ECONOMICAL. HIS VACATION HAD CONSUMED NEARLY ALL HE HAD EARNED IN THE LAUNDRY, AND HE WAS SO FAR FROM HIS MARKET THAT WEEKS MUST ELAPSE BEFORE HE COULD HOPE FOR THE FIRST RETURNS FROM HIS HACK-WORK. EXCEPT AT SUCH TIMES AS HE SAW RUTH, OR DROPPED IN TO SEE HIS SISTER GERTUDE, HE LIVED A RECLUSE, IN EACH DAY ACCOMPLISHING AT LEAST THREE DAYS’ LABOR OF ORDINARY MEN. HE SLEPT A SCANT FIVE HOURS, AND ONLY ONE WITH A CONSTITUTION OF IRON COULD HAVE HELD HIMSELF DOWN, AS MARTIN DID, DAY AFTER DAY, TO NINETEEN CONSECUTIVE HOURS OF TOIL. HE NEVER LOST A MOMENT. ON THE LOOKING-GLASS WERE LISTS OF DEFINITIONS AND PRONUNCIATIONS; WHEN SHAVING, OR DRESSING, OR COMBING HIS HAIR, HE CONNED THESE LISTS OVER. SIMILAR LISTS WERE ON THE WALL OVER THE OIL-STOVE, AND THEY WERE SIMILARLY CONNED WHILE HE WAS ENGAGED IN COOKING OR IN WASHING THE DISHES. NEW LISTS CONTINUALLY DISPLACED THE OLD ONES. EVERY STRANGE OR PARTLY FAMILIAR WORD ENCOUNTERED IN HIS READING WAS IMMEDIATELY JOTTED DOWN, AND LATER, WHEN A SUFFICIENT NUMBER HAD BEEN ACCUMULATED, WERE TYPED AND PINNED TO THE WALL OR LOOKING-GLASS. HE EVEN CARRIED THEM IN HIS POCKETS, AND REVIEWED THEM AT ODD MOMENTS ON THE STREET, OR WHILE WAITING IN BUTCHER SHOP OR GROCERY TO BE SERVED.   HE WENT FARTHER IN THE MATTER. READING THE WORKS OF MEN WHO HAD ARRIVED, HE NOTED EVERY RESULT ACHIEVED BY THEM, AND WORKED OUT THE TRICKS BY WHICH THEY HAD BEEN ACHIEVED-THE TRICKS OF NARRATIVE, OF EXPOSITION, OF STYLE, THE POINTS OF VIEW, THE CONTRASTS, THE EPIGRAMS; AND OF ALL THESE HE MADE LISTS FOR STUDY. HE DID NOT APE. HE SOUGHT PRINCIPLES. HE DREW UP LISTS OF EFFECTIVE AND FETCHING MANNERISMS, TILL OUT OF MANY SUCH, CULLED FROM MANY WRITERS, HE WAS ABLE TO INDUCE THE GENERAL PRINCIPLE OF MANNERISM, AND, THUS EQUIPPED, TO CAST ABOUT FOR NEW AND ORIGINAL ONES OF HIS OWN, AND TO WEIGH AND MEASURE AND APPRAISE THEM PROPERLY. IN SIMILAR MANNER HE COLLECTED LISTS OF STRONG PHRASES, THE PHRASES OF LIVING LANGUAGE, PHRASES THAT BIT LIKE ACID AND SCORCHED LIKE FLAME, OR THAT GLOWED AND WERE MELLOW AND LUSCIOUS IN THE MIDST OF THE ARID DESERT OF COMMON SPEECH. HE SOUGHT ALWAYS FOR THE PRINCIPLE THAT LAY BEHIND AND BENEATH. HE WANTED TO KNOW HOW THE THING WAS DONE; AFTER THAT HE COULD DO IT FOR HIMSELF. HE WAS NOT CONTENT WITH THE FAIR FACE OF BEAUTY. HE DISSECTED BEAUTY IN HIS CROWDED LITTLE BEDROOM LABORATORY, WHERE COOKING SMELLS ALTERNATED WITH THE OUTER BEDLAM OF THE SILVA TRIBE; AND, HAVING DISSECTED AND LEARNED THE ANATOMY OF BEAUTY, HE WAS NEARER BEING ABLE TO CREATE BEAUTY ITSELF.   HE WAS SO MADE THAT HE COULD WORK ONLY WITH UNDERSTANDING. HE COULD NOT WORK BLINDLY, IN THE DARK, IGNORANT OF WHAT HE WAS PRODUCING AND TRUSTING TO CHANCE AND THE STAR OF HIS GENIUS THAT THE EFFECT PRODUCED SHOULD BE RIGHT AND FINE. HE HAD NO PATIENCE WITH CHANCE EFFECTS. HE WANTED TO KNOW WHY AND HOW. HIS WAS DELIBERATE CREATIVE GENIUS, AND, BEFORE HE BEGAN A STORY OR POEM, THE THING ITSELF WAS ALREADY ALIVE IN HIS BRAIN, WITH THE END IN SIGHT AND THE MEANS OF REALIZING THAT END IN HIS CONSCIOUS POSSESSION. OTHERWISE THE EFFORT WAS DOOMED TO FAILURE. ON THE OTHER HAND, HE APPRECIATED THE CHANCE EFFECTS IN WORDS AND PHRASES THAT CAME LIGHTLY AND EASILY INTO HIS BRAIN, AND THAT LATER STOOD ALL TESTS OF BEAUTY AND POWER AND DEVELOPED TREMENDOUS AND INCOMMUNICABLE CONNOTATIONS. BEFORE SUCH HE BOWED DOWN AND MARVELLED, KNOWING THAT THEY WERE BEYOND THE DELIBERATE CREATION OF ANY MAN. AND NO MATTER HOW MUCH HE DISSECTED BEAUTY IN SEARCH OF THE PRINCIPLES THAT UNDERLIE BEAUTY AND MAKE BEAUTY POSSIBLE, HE WAS AWARE, ALWAYS, OF THE INNERMOST MYSTERY OF BEAUTY TO WHICH HE DID NOT PENETRATE AND TO WHICH NO MAN HAD EVER PENETRATED. HE KNEW FULL WELL, FROM HIS SPENCER, THAT MAN CAN NEVER ATTAIN ULTIMATE KNOWLEDGE OF ANYTHING, AND THAT THE MYSTERY OF BEAUTY WAS NO LESS THAN THAT OF LIFE-NAY, MORE THAT THE FIBRES OF BEAUTY AND LIFE WERE INTERTWISTED, AND THAT HE HIMSELF WAS BUT A BIT OF THE SAME NONUNDERSTANDABLE FABRIC, TWISTED OF SUNSHINE AND STAR-DUST AND WONDER.   IN FACT, IT WAS WHEN FILLED WITH THESE THOUGHTS THAT HE WROTE HIS ESSAY ENTITLED STAR-DUST, IN WHICH HE HAD HIS FLING, NOT AT THE PRINCIPLES OF CRITICISM, BUT AT THE PRINCIPAL CRITICS. IT WAS BRILLIANT, DEEP, PHILOSOPHICAL, AND DELICIOUSLY TOUCHED WITH LAUGHTER. ALSO IT WAS PROMPTLY REJECTED BY THE MAGAZINES AS OFTEN AS IT WAS SUBMITTED. BUT HAVING CLEARED HIS MIND OF IT, HE WENT SERENELY ON HIS WAY. IT WAS A HABIT HE DEVELOPED, OF INCUBATING AND MATURING HIS THOUGHT UPON A SUBJECT, AND OF THEN RUSHING INTO THE TYPE-WRITER WITH IT. THAT IT DID NOT SEE PRINT WAS A MATTER A SMALL MOMENT WITH HIM. THE WRITING OF IT WAS THE CULMINATING ACT OF A LONG MENTAL PROCESS, THE DRAWING TOGETHER OF SCATTERED THREADS OF THOUGHT AND THE FINAL GENERALIZING UPON ALL THE DATA WITH WHICH HIS MIND WAS BURDENED. TO WRITE SUCH AN ARTICLE WAS THE CONSCIOUS EFFORT BY WHICH HE FREED HIS MIND AND MADE IT READY FOR FRESH MATERIAL AND PROBLEMS. IT WAS IN A WAY AKIN TO THAT COMMON HABIT OF MEN AND WOMEN TROUBLED BY REAL OR FANCIED GRIEVANCES, WHO PERIODICALLY AND VOLUBLY BREAK THEIR LONG-SUFFERING SILENCE AND HAVE THEIR SAY TILL THE LAST WORD IS SAID."


    text138 = u'''CHAPTER I

The one opened the door with a latch-key and went in, followed by a young fellow who awkwardly removed his cap. He wore rough clothes that smacked of the sea, and he was manifestly out of place in the spacious hall in which he found himself. He did not know what to do with his cap, and was stuffing it into his coat pocket when the other took it from him. The act was done quietly and naturally, and the awkward young fellow appreciated it. "He understands," was his thought. "He’ll see me through all right."

He walked at the other’s heels with a swing to his shoulders, and his legs spread unwittingly, as if the level floors were tilting up and sinking down to the heave and lunge of the sea. The wide rooms seemed too narrow for his rolling gait, and to himself he was in terror lest his broad shoulders should collide with the doorways or sweep the bric-a-brac from the low mantel. He recoiled from side to side between the various objects and multiplied the hazards that in reality lodged only in his mind. Between a grand piano and a centre-table piled high with books was space for a half a dozen to walk abreast, yet he essayed it with trepidation. His heavy arms hung loosely at his sides. He did not know what to do with those arms and hands, and when, to his excited vision, one arm seemed liable to brush against the books on the table, he lurched away like a frightened horse, barely missing the piano stool. He watched the easy walk of the other in front of him, and for the first time realized that his walk was different from that of other men. He experienced a momentary pang of shame that he should walk so uncouthly. The sweat burst through the skin of his forehead in tiny beads, and he paused and mopped his bronzed face with his handkerchief.

"Hold on, Arthur, my boy," he said, attempting to mask his anxiety with facetious utterance. "This is too much all at once for yours truly. Give me a chance to get my nerve. You know I didn’t want to come, an’ I guess your fam’ly ain’t hankerin’ to see me neither."

"That’s all right," was the reassuring answer. "You mustn’t be frightened at us. We’re just homely people-Hello, there’s a letter for me."

He stepped back to the table, tore open the envelope, and began to read, giving the stranger an opportunity to recover himself. And the stranger understood and appreciated. His was the gift of sympathy, understanding; and beneath his alarmed exterior that sympathetic process went on. He mopped his forehead dry and glanced about him with a controlled face, though in the eyes there was an expression such as wild animals betray when they fear the trap. He was surrounded by the unknown, apprehensive of what might happen, ignorant of what he should do, aware that he walked and bore himself awkwardly, fearful that every attribute and power of him was similarly afflicted. He was keenly sensitive, hopelessly self-conscious, and the amused glance that the other stole privily at him over the top of the letter burned into him like a dagger-thrust. He saw the glance, but he gave no sign, for among the things he had learned was discipline. Also, that dagger-thrust went to his pride. He cursed himself for having come, and at the same time resolved that, happen what would, having come, he would carry it through. The lines of his face hardened, and into his eyes came a fighting light. He looked about more unconcernedly, sharply observant, every detail of the pretty interior registering itself on his brain. His eyes were wide apart; nothing in their field of vision escaped; and as they drank in the beauty before them the fighting light died out and a warm glow took its place. He was responsive to beauty, and here was cause to respond.

An oil painting caught and held him. A heavy surf thundered and burst over an outjutting rock; lowering storm-clouds covered the sky; and, outside the line of surf, a pilot-schooner, close-hauled, heeled over till every detail of her deck was visible, was surging along against a stormy sunset sky. There was beauty, and it drew him irresistibly. He forgot his awkward walk and came closer to the painting, very close. The beauty faded out of the canvas. His face expressed his bepuzzlement. He stared at what seemed a careless daub of paint, then stepped away. Immediately all the beauty flashed back into the canvas. "A trick picture," was his thought, as he dismissed it, though in the midst of the multitudinous impressions he was receiving he found time to feel a prod of indignation that so much beauty should be sacrificed to make a trick. He did not know painting. He had been brought up on chromos and lithographs that were always definite and sharp, near or far. He had seen oil paintings, it was true, in the show windows of shops, but the glass of the windows had prevented his eager eyes from approaching too near.

He glanced around at his friend reading the letter and saw the books on the table. Into his eyes leaped a wistfulness and a yearning as promptly as the yearning leaps into the eyes of a starving man at sight of food. An impulsive stride, with one lurch to right and left of the shoulders, brought him to the table, where he began affectionately handling the books. He glanced at the titles and the authors’ names, read fragments of text, caressing the volumes with his eyes and hands, and, once, recognized a book he had read. For the rest, they were strange books and strange authors. He chanced upon a volume of Swinburne and began reading steadily, forgetful of where he was, his face glowing. Twice he closed the book on his forefinger to look at the name of the author. Swinburne! he would remember that name. That fellow had eyes, and he had certainly seen color and flashing light. But who was Swinburne? Was he dead a hundred years or so, like most of the poets? Or was he alive still, and writing? He turned to the title-page… yes, he had written other books; well, he would go to the free library the first thing in the morning and try to get hold of some of Swinburne’s stuff. He went back to the text and lost himself. He did not notice that a young woman had entered the room. The first he knew was when he heard Arthur’s voice saying:-

"Ruth, this is Mr. Eden."

The book was closed on his forefinger, and before he turned he was thrilling to the first new impression, which was not of the girl, but of her brother’s words. Under that muscled body of his he was a mass of quivering sensibilities. At the slightest impact of the outside world upon his consciousness, his thoughts, sympathies, and emotions leapt and played like lambent flame. He was extraordinarily receptive and responsive, while his imagination, pitched high, was ever at work establishing relations of likeness and difference. "Mr. Eden," was what he had thrilled to-he who had been called "Eden," or "Martin Eden," or just "Martin," all his life. And " Mister !" It was certainly going some, was his internal comment. His mind seemed to turn, on the instant, into a vast camera obscura, and he saw arrayed around his consciousness endless pictures from his life, of stoke-holes and forecastles, camps and beaches, jails and boozing-kens, fever-hospitals and slum streets, wherein the thread of association was the fashion in which he had been addressed in those various situations.

And then he turned and saw the girl. The phantasmagoria of his brain vanished at sight of her. She was a pale, ethereal creature, with wide, spiritual blue eyes and a wealth of golden hair. He did not know how she was dressed, except that the dress was as wonderful as she. He likened her to a pale gold flower upon a slender stem. No, she was a spirit, a divinity, a goddess; such sublimated beauty was not of the earth. Or perhaps the books were right, and there were many such as she in the upper walks of life. She might well be sung by that chap, Swinburne. Perhaps he had had somebody like her in mind when he painted that girl, Iseult, in the book there on the table. All this plethora of sight, and feeling, and thought occurred on the instant. There was no pause of the realities wherein he moved. He saw her hand coming out to his, and she looked him straight in the eyes as she shook hands, frankly, like a man. The women he had known did not shake hands that way. For that matter, most of them did not shake hands at all. A flood of associations, visions of various ways he had made the acquaintance of women, rushed into his mind and threatened to swamp it. But he shook them aside and looked at her. Never had he seen such a woman. The women he had known! Immediately, beside her, on either hand, ranged the women he had known. For an eternal second he stood in the midst of a portrait gallery, wherein she occupied the central place, while about her were limned many women, all to be weighed and measured by a fleeting glance, herself the unit of weight and measure. He saw the weak and sickly faces of the girls of the factories, and the simpering, boisterous girls from the south of Market. There were women of the cattle camps, and swarthy cigarette-smoking women of Old Mexico. These, in turn, were crowded out by Japanese women, doll-like, stepping mincingly on wooden clogs; by Eurasians, delicate featured, stamped with degeneracy; by full-bodied South-Sea-Island women, flower-crowned and brown-skinned. All these were blotted out by a grotesque and terrible nightmare brood-frowsy, shuffling creatures from the pavements of Whitechapel, gin-bloated hags of the stews, and all the vast hell’s following of harpies, vile-mouthed and filthy, that under the guise of monstrous female form prey upon sailors, the scrapings of the ports, the scum and slime of the human pit.

"Won’t you sit down, Mr. Eden?" the girl was saying. "I have been looking forward to meeting you ever since Arthur told us. It was brave of you-"

He waved his hand deprecatingly and muttered that it was nothing at all, what he had done, and that any fellow would have done it. She noticed that the hand he waved was covered with fresh abrasions, in the process of healing, and a glance at the other loose-hanging hand showed it to be in the same condition. Also, with quick, critical eye, she noted a scar on his cheek, another that peeped out from under the hair of the forehead, and a third that ran down and disappeared under the starched collar. She repressed a smile at sight of the red line that marked the chafe of the collar against the bronzed neck. He was evidently unused to stiff collars. Likewise her feminine eye took in the clothes he wore, the cheap and unaesthetic cut, the wrinkling of the coat across the shoulders, and the series of wrinkles in the sleeves that advertised bulging biceps muscles.

While he waved his hand and muttered that he had done nothing at all, he was obeying her behest by trying to get into a chair. He found time to admire the ease with which she sat down, then lurched toward a chair facing her, overwhelmed with consciousness of the awkward figure he was cutting. This was a new experience for him. All his life, up to then, he had been unaware of being either graceful or awkward. Such thoughts of self had never entered his mind. He sat down gingerly on the edge of the chair, greatly worried by his hands. They were in the way wherever he put them. Arthur was leaving the room, and Martin Eden followed his exit with longing eyes. He felt lost, alone there in the room with that pale spirit of a woman. There was no bar-keeper upon whom to call for drinks, no small boy to send around the corner for a can of beer and by means of that social fluid start the amenities of friendship flowing.

"You have such a scar on your neck, Mr. Eden," the girl was saying. "How did it happen? I am sure it must have been some adventure."

"A Mexican with a knife, miss," he answered, moistening his parched lips and clearing hip throat. "It was just a fight. After I got the knife away, he tried to bite off my nose."

Baldly as he had stated it, in his eyes was a rich vision of that hot, starry night at Salina Cruz, the white strip of beach, the lights of the sugar steamers in the harbor, the voices of the drunken sailors in the distance, the jostling stevedores, the flaming passion in the Mexican’s face, the glint of the beast-eyes in the starlight, the sting of the steel in his neck, and the rush of blood, the crowd and the cries, the two bodies, his and the Mexican’s, locked together, rolling over and over and tearing up the sand, and from away off somewhere the mellow tinkling of a guitar. Such was the picture, and he thrilled to the memory of it, wondering if the man could paint it who had painted the pilot-schooner on the wall. The white beach, the stars, and the lights of the sugar steamers would look great, he thought, and midway on the sand the dark group of figures that surrounded the fighters. The knife occupied a place in the picture, he decided, and would show well, with a sort of gleam, in the light of the stars. But of all this no hint had crept into his speech. "He tried to bite off my nose," he concluded.

"Oh," the girl said, in a faint, far voice, and he noticed the shock in her sensitive face.

He felt a shock himself, and a blush of embarrassment shone faintly on his sunburned cheeks, though to him it burned as hotly as when his cheeks had been exposed to the open furnace-door in the fire-room. Such sordid things as stabbing affrays were evidently not fit subjects for conversation with a lady. People in the books, in her walk of life, did not talk about such things-perhaps they did not know about them, either.

There was a brief pause in the conversation they were trying to get started. Then she asked tentatively about the scar on his cheek. Even as she asked, he realized that she was making an effort to talk his talk, and he resolved to get away from it and talk hers.

"It was just an accident," he said, putting his hand to his cheek. "One night, in a calm, with a heavy sea running, the main-boom-lift carried away, an’ next the tackle. The lift was wire, an’ it was threshin’ around like a snake. The whole watch was tryin’ to grab it, an’ I rushed in an’ got swatted."

"Oh," she said, this time with an accent of comprehension, though secretly his speech had been so much Greek to her and she was wondering what a lift was and what swatted meant.

"This man Swineburne," he began, attempting to put his plan into execution and pronouncing the i long.

"Who?"

"Swineburne," he repeated, with the same mispronunciation. "The poet."

"Swinburne," she corrected.

"Yes, that’s the chap," he stammered, his cheeks hot again. "How long since he died?"

"Why, I haven’t heard that he was dead." She looked at him curiously. "Where did you make his acquaintance?"

"I never clapped eyes on him," was the reply. "But I read some of his poetry out of that book there on the table just before you come in. How do you like his poetry?"

And thereat she began to talk quickly and easily upon the subject he had suggested. He felt better, and settled back slightly from the edge of the chair, holding tightly to its arms with his hands, as if it might get away from him and buck him to the floor. He had succeeded in making her talk her talk, and while she rattled on, he strove to follow her, marvelling at all the knowledge that was stowed away in that pretty head of hers, and drinking in the pale beauty of her face. Follow her he did, though bothered by unfamiliar words that fell glibly from her lips and by critical phrases and thought-processes that were foreign to his mind, but that nevertheless stimulated his mind and set it tingling. Here was intellectual life, he thought, and here was beauty, warm and wonderful as he had never dreamed it could be. He forgot himself and stared at her with hungry eyes. Here was something to live for, to win to, to fight for-ay, and die for. The books were true. There were such women in the world. She was one of them. She lent wings to his imagination, and great, luminous canvases spread themselves before him whereon loomed vague, gigantic figures of love and romance, and of heroic deeds for woman’s sake-for a pale woman, a flower of gold. And through the swaying, palpitant vision, as through a fairy mirage, he stared at the real woman, sitting there and talking of literature and art. He listened as well, but he stared, unconscious of the fixity of his gaze or of the fact that all that was essentially masculine in his nature was shining in his eyes. But she, who knew little of the world of men, being a woman, was keenly aware of his burning eyes. She had never had men look at her in such fashion, and it embarrassed her. She stumbled and halted in her utterance. The thread of argument slipped from her. He frightened her, and at the same time it was strangely pleasant to be so looked upon. Her training warned her of peril and of wrong, subtle, mysterious, luring; while her instincts rang clarion-voiced through her being, impelling her to hurdle caste and place and gain to this traveller from another world, to this uncouth young fellow with lacerated hands and a line of raw red caused by the unaccustomed linen at his throat, who, all too evidently, was soiled and tainted by ungracious existence. She was clean, and her cleanness revolted; but she was woman, and she was just beginning to learn the paradox of woman.

"As I was saying-what was I saying?" She broke off abruptly and laughed merrily at her predicament.

"You was saying that this man Swinburne failed bein’ a great poet because-an’ that was as far as you got, miss," he prompted, while to himself he seemed suddenly hungry, and delicious little thrills crawled up and down his spine at the sound of her laughter. Like silver, he thought to himself, like tinkling silver bells; and on the instant, and for an instant, he was transported to a far land, where under pink cherry blossoms, he smoked a cigarette and listened to the bells of the peaked pagoda calling straw-sandalled devotees to worship.

"Yes, thank you," she said. "Swinburne fails, when all is said, because he is, well, indelicate. There are many of his poems that should never be read. Every line of the really great poets is filled with beautiful truth, and calls to all that is high and noble in the human. Not a line of the great poets can be spared without impoverishing the world by that much."

"I thought it was great," he said hesitatingly, "the little I read. I had no idea he was such a-a scoundrel. I guess that crops out in his other books."

"There are many lines that could be spared from the book you were reading," she said, her voice primly firm and dogmatic.

"I must ’a’ missed ’em," he announced. "What I read was the real goods. It was all lighted up an’ shining, an’ it shun right into me an’ lighted me up inside, like the sun or a searchlight. That’s the way it landed on me, but I guess I ain’t up much on poetry, miss."

He broke off lamely. He was confused, painfully conscious of his inarticulateness. He had felt the bigness and glow of life in what he had read, but his speech was inadequate. He could not express what he felt, and to himself he likened himself to a sailor, in a strange ship, on a dark night, groping about in the unfamiliar running rigging. Well, he decided, it was up to him to get acquainted in this new world. He had never seen anything that he couldn’t get the hang of when he wanted to and it was about time for him to want to learn to talk the things that were inside of him so that she could understand. She was bulking large on his horizon.

"Now Longfellow-" she was saying.

"Yes, I’ve read ’m," he broke in impulsively, spurred on to exhibit and make the most of his little store of book knowledge, desirous of showing her that he was not wholly a stupid clod. "‘The Psalm of Life,’ ‘Excelsior,’ an’… I guess that’s all."

She nodded her head and smiled, and he felt, somehow, that her smile was tolerant, pitifully tolerant. He was a fool to attempt to make a pretence that way. That Longfellow chap most likely had written countless books of poetry.

"Excuse me, miss, for buttin’ in that way. I guess the real facts is that I don’t know nothin’ much about such things. It ain’t in my class. But I’m goin’ to make it in my class."

It sounded like a threat. His voice was determined, his eyes were flashing, the lines of his face had grown harsh. And to her it seemed that the angle of his jaw had changed; its pitch had become unpleasantly aggressive. At the same time a wave of intense virility seemed to surge out from him and impinge upon her.

"I think you could make it in-in your class," she finished with a laugh. "You are very strong."

Her gaze rested for a moment on the muscular neck, heavy corded, almost bull-like, bronzed by the sun, spilling over with rugged health and strength. And though he sat there, blushing and humble, again she felt drawn to him. She was surprised by a wanton thought that rushed into her mind. It seemed to her that if she could lay her two hands upon that neck that all its strength and vigor would flow out to her. She was shocked by this thought. It seemed to reveal to her an undreamed depravity in her nature. Besides, strength to her was a gross and brutish thing. Her ideal of masculine beauty had always been slender gracefulness. Yet the thought still persisted. It bewildered her that she should desire to place her hands on that sunburned neck. In truth, she was far from robust, and the need of her body and mind was for strength. But she did not know it. She knew only that no man had ever affected her before as this one had, who shocked her from moment to moment with his awful grammar.

"Yes, I ain’t no invalid," he said. "When it comes down to hard-pan, I can digest scrap-iron. But just now I’ve got dyspepsia. Most of what you was sayin’ I can’t digest. Never trained that way, you see. I like books and poetry, and what time I’ve had I’ve read ’em, but I’ve never thought about ’em the way you have. That’s why I can’t talk about ’em. I’m like a navigator adrift on a strange sea without chart or compass. Now I want to get my bearin’s. Mebbe you can put me right. How did you learn all this you’ve ben talkin’?"

"By going to school, I fancy, and by studying," she answered.

"I went to school when I was a kid," he began to object.

"Yes; but I mean high school, and lectures, and the university."

"You’ve gone to the university?" he demanded in frank amazement. He felt that she had become remoter from him by at least a million miles.

"I’m going there now. I’m taking special courses in English."

He did not know what "English" meant, but he made a mental note of that item of ignorance and passed on.

"How long would I have to study before I could go to the university?" he asked.

She beamed encouragement upon his desire for knowledge, and said: "That depends upon how much studying you have already done. You have never attended high school? Of course not. But did you finish grammar school?"

"I had two years to run, when I left," he answered. "But I was always honorably promoted at school."

The next moment, angry with himself for the boast, he had gripped the arms of the chair so savagely that every finger-end was stinging. At the same moment he became aware that a woman was entering the room. He saw the girl leave her chair and trip swiftly across the floor to the newcomer. They kissed each other, and, with arms around each other’s waists, they advanced toward him. That must be her mother, he thought. She was a tall, blond woman, slender, and stately, and beautiful. Her gown was what he might expect in such a house. His eyes delighted in the graceful lines of it. She and her dress together reminded him of women on the stage. Then he remembered seeing similar grand ladies and gowns entering the London theatres while he stood and watched and the policemen shoved him back into the drizzle beyond the awning. Next his mind leaped to the Grand Hotel at Yokohama, where, too, from the sidewalk, he had seen grand ladies. Then the city and the harbor of Yokohama, in a thousand pictures, began flashing before his eyes. But he swiftly dismissed the kaleidoscope of memory, oppressed by the urgent need of the present. He knew that he must stand up to be introduced, and he struggled painfully to his feet, where he stood with trousers bagging at the knees, his arms loose-hanging and ludicrous, his face set hard for the impending ordeal.



CHAPTER II

The process of getting into the dining room was a nightmare to him. Between halts and stumbles, jerks and lurches, locomotion had at times seemed impossible. But at last he had made it, and was seated alongside of Her. The array of knives and forks frightened him. They bristled with unknown perils, and he gazed at them, fascinated, till their dazzle became a background across which moved a succession of forecastle pictures, wherein he and his mates sat eating salt beef with sheath-knives and fingers, or scooping thick pea-soup out of pannikins by means of battered iron spoons. The stench of bad beef was in his nostrils, while in his ears, to the accompaniment of creaking timbers and groaning bulkheads, echoed the loud mouth-noises of the eaters. He watched them eating, and decided that they ate like pigs. Well, he would be careful here. He would make no noise. He would keep his mind upon it all the time.

He glanced around the table. Opposite him was Arthur, and Arthur’s brother, Norman. They were her brothers, he reminded himself, and his heart warmed toward them. How they loved each other, the members of this family! There flashed into his mind the picture of her mother, of the kiss of greeting, and of the pair of them walking toward him with arms entwined. Not in his world were such displays of affection between parents and children made. It was a revelation of the heights of existence that were attained in the world above. It was the finest thing yet that he had seen in this small glimpse of that world. He was moved deeply by appreciation of it, and his heart was melting with sympathetic tenderness. He had starved for love all his life. His nature craved love. It was an organic demand of his being. Yet he had gone without, and hardened himself in the process. He had not known that he needed love. Nor did he know it now. He merely saw it in operation, and thrilled to it, and thought it fine, and high, and splendid.

He was glad that Mr. Morse was not there. It was difficult enough getting acquainted with her, and her mother, and her brother, Norman. Arthur he already knew somewhat. The father would have been too much for him, he felt sure. It seemed to him that he had never worked so hard in his life. The severest toil was child’s play compared with this. Tiny nodules of moisture stood out on his forehead, and his shirt was wet with sweat from the exertion of doing so many unaccustomed things at once. He had to eat as he had never eaten before, to handle strange tools, to glance surreptitiously about and learn how to accomplish each new thing, to receive the flood of impressions that was pouring in upon him and being mentally annotated and classified; to be conscious of a yearning for her that perturbed him in the form of a dull, aching restlessness; to feel the prod of desire to win to the walk in life whereon she trod, and to have his mind ever and again straying off in speculation and vague plans of how to reach to her. Also, when his secret glance went across to Norman opposite him, or to any one else, to ascertain just what knife or fork was to be used in any particular occasion, that person’s features were seized upon by his mind, which automatically strove to appraise them and to divine what they were-all in relation to her. Then he had to talk, to hear what was said to him and what was said back and forth, and to answer, when it was necessary, with a tongue prone to looseness of speech that required a constant curb. And to add confusion to confusion, there was the servant, an unceasing menace, that appeared noiselessly at his shoulder, a dire Sphinx that propounded puzzles and conundrums demanding instantaneous solution. He was oppressed throughout the meal by the thought of finger-bowls. Irrelevantly, insistently, scores of times, he wondered when they would come on and what they looked like. He had heard of such things, and now, sooner or later, somewhere in the next few minutes, he would see them, sit at table with exalted beings who used them-ay, and he would use them himself. And most important of all, far down and yet always at the surface of his thought, was the problem of how he should comport himself toward these persons. What should his attitude be? He wrestled continually and anxiously with the problem. There were cowardly suggestions that he should make believe, assume a part; and there were still more cowardly suggestions that warned him he would fail in such course, that his nature was not fitted to live up to it, and that he would make a fool of himself.

It was during the first part of the dinner, struggling to decide upon his attitude, that he was very quiet. He did not know that his quietness was giving the lie to Arthur’s words of the day before, when that brother of hers had announced that he was going to bring a wild man home to dinner and for them not to be alarmed, because they would find him an interesting wild man. Martin Eden could not have found it in him, just then, to believe that her brother could be guilty of such treachery-especially when he had been the means of getting this particular brother out of an unpleasant row. So he sat at table, perturbed by his own unfitness and at the same time charmed by all that went on about him. For the first time he realized that eating was something more than a utilitarian function. He was unaware of what he ate. It was merely food. He was feasting his love of beauty at this table where eating was an aesthetic function. It was an intellectual function, too. His mind was stirred. He heard words spoken that were meaningless to him, and other words that he had seen only in books and that no man or woman he had known was of large enough mental caliber to pronounce. When he heard such words dropping carelessly from the lips of the members of this marvellous family, her family, he thrilled with delight. The romance, and beauty, and high vigor of the books were coming true. He was in that rare and blissful state wherein a man sees his dreams stalk out from the crannies of fantasy and become fact.

Never had he been at such an altitude of living, and he kept himself in the background, listening, observing, and pleasuring, replying in reticent monosyllables, saying, "Yes, miss," and "No, miss," to her, and "Yes, ma’am," and "No, ma’am," to her mother. He curbed the impulse, arising out of his sea-training, to say "Yes, sir," and "No, sir," to her brothers. He felt that it would be inappropriate and a confession of inferiority on his part-which would never do if he was to win to her. Also, it was a dictate of his pride. "By God!" he cried to himself, once; "I’m just as good as them, and if they do know lots that I don’t, I could learn ’m a few myself, all the same!" And the next moment, when she or her mother addressed him as "Mr. Eden," his aggressive pride was forgotten, and he was glowing and warm with delight. He was a civilized man, that was what he was, shoulder to shoulder, at dinner, with people he had read about in books. He was in the books himself, adventuring through the printed pages of bound volumes.

But while he belied Arthur’s description, and appeared a gentle lamb rather than a wild man, he was racking his brains for a course of action. He was no gentle lamb, and the part of second fiddle would never do for the high-pitched dominance of his nature. He talked only when he had to, and then his speech was like his walk to the table, filled with jerks and halts as he groped in his polyglot vocabulary for words, debating over words he knew were fit but which he feared he could not pronounce, rejecting other words he knew would not be understood or would be raw and harsh. But all the time he was oppressed by the consciousness that this carefulness of diction was making a booby of him, preventing him from expressing what he had in him. Also, his love of freedom chafed against the restriction in much the same way his neck chafed against the starched fetter of a collar. Besides, he was confident that he could not keep it up. He was by nature powerful of thought and sensibility, and the creative spirit was restive and urgent. He was swiftly mastered by the concept or sensation in him that struggled in birth-throes to receive expression and form, and then he forgot himself and where he was, and the old words-the tools of speech he knew-slipped out.

Once, he declined something from the servant who interrupted and pestered at his shoulder, and he said, shortly and emphatically, "Pew!"

On the instant those at the table were keyed up and expectant, the servant was smugly pleased, and he was wallowing in mortification. But he recovered himself quickly.

"It’s the Kanaka for ‘finish,’" he explained, "and it just come out naturally. It’s spelt p-a-u."

He caught her curious and speculative eyes fixed on his hands, and, being in explanatory mood, he said:-

"I just come down the Coast on one of the Pacific mail steamers. She was behind time, an’ around the Puget Sound ports we worked like niggers, storing cargo-mixed freight, if you know what that means. That’s how the skin got knocked off."

"Oh, it wasn’t that," she hastened to explain, in turn. "Your hands seemed too small for your body."

His cheeks were hot. He took it as an exposure of another of his deficiencies.

"Yes," he said depreciatingly. "They ain’t big enough to stand the strain. I can hit like a mule with my arms and shoulders. They are too strong, an’ when I smash a man on the jaw the hands get smashed, too."

He was not happy at what he had said. He was filled with disgust at himself. He had loosed the guard upon his tongue and talked about things that were not nice.

"It was brave of you to help Arthur the way you did-and you a stranger," she said tactfully, aware of his discomfiture though not of the reason for it.

He, in turn, realized what she had done, and in the consequent warm surge of gratefulness that overwhelmed him forgot his loose-worded tongue.

"It wasn’t nothin’ at all," he said. "Any guy ’ud do it for another. That bunch of hoodlums was lookin’ for trouble, an’ Arthur wasn’t botherin’ ’em none. They butted in on ’m, an’ then I butted in on them an’ poked a few. That’s where some of the skin off my hands went, along with some of the teeth of the gang. I wouldn’t ’a’ missed it for anything. When I seen-"

He paused, open-mouthed, on the verge of the pit of his own depravity and utter worthlessness to breathe the same air she did. And while Arthur took up the tale, for the twentieth time, of his adventure with the drunken hoodlums on the ferry-boat and of how Martin Eden had rushed in and rescued him, that individual, with frowning brows, meditated upon the fool he had made of himself, and wrestled more determinedly with the problem of how he should conduct himself toward these people. He certainly had not succeeded so far. He wasn’t of their tribe, and he couldn’t talk their lingo, was the way he put it to himself. He couldn’t fake being their kind. The masquerade would fail, and besides, masquerade was foreign to his nature. There was no room in him for sham or artifice. Whatever happened, he must be real. He couldn’t talk their talk just yet, though in time he would. Upon that he was resolved. But in the meantime, talk he must, and it must be his own talk, toned down, of course, so as to be comprehensible to them and so as not to shook them too much. And furthermore, he wouldn’t claim, not even by tacit acceptance, to be familiar with anything that was unfamiliar. In pursuance of this decision, when the two brothers, talking university shop, had used "trig" several times, Martin Eden demanded:-

"What is trig ?"

"Trignometry," Norman said; "a higher form of math."

"And what is math?" was the next question, which, somehow, brought the laugh on Norman.

"Mathematics, arithmetic," was the answer.

Martin Eden nodded. He had caught a glimpse of the apparently illimitable vistas of knowledge. What he saw took on tangibility. His abnormal power of vision made abstractions take on concrete form. In the alchemy of his brain, trigonometry and mathematics and the whole field of knowledge which they betokened were transmuted into so much landscape. The vistas he saw were vistas of green foliage and forest glades, all softly luminous or shot through with flashing lights. In the distance, detail was veiled and blurred by a purple haze, but behind this purple haze, he knew, was the glamour of the unknown, the lure of romance. It was like wine to him. Here was adventure, something to do with head and hand, a world to conquer-and straightway from the back of his consciousness rushed the thought, conquering, to win to her, that lily-pale spirit sitting beside him .

The glimmering vision was rent asunder and dissipated by Arthur, who, all evening, had been trying to draw his wild man out. Martin Eden remembered his decision. For the first time he became himself, consciously and deliberately at first, but soon lost in the joy of creating in making life as he knew it appear before his listeners’ eyes. He had been a member of the crew of the smuggling schooner Halcyon when she was captured by a revenue cutter. He saw with wide eyes, and he could tell what he saw. He brought the pulsing sea before them, and the men and the ships upon the sea. He communicated his power of vision, till they saw with his eyes what he had seen. He selected from the vast mass of detail with an artist’s touch, drawing pictures of life that glowed and burned with light and color, injecting movement so that his listeners surged along with him on the flood of rough eloquence, enthusiasm, and power. At times he shocked them with the vividness of the narrative and his terms of speech, but beauty always followed fast upon the heels of violence, and tragedy was relieved by humor, by interpretations of the strange twists and quirks of sailors’ minds.

And while he talked, the girl looked at him with startled eyes. His fire warmed her. She wondered if she had been cold all her days. She wanted to lean toward this burning, blazing man that was like a volcano spouting forth strength, robustness, and health. She felt that she must lean toward him, and resisted by an effort. Then, too, there was the counter impulse to shrink away from him. She was repelled by those lacerated hands, grimed by toil so that the very dirt of life was ingrained in the flesh itself, by that red chafe of the collar and those bulging muscles. His roughness frightened her; each roughness of speech was an insult to her ear, each rough phase of his life an insult to her soul. And ever and again would come the draw of him, till she thought he must be evil to have such power over her. All that was most firmly established in her mind was rocking. His romance and adventure were battering at the conventions. Before his facile perils and ready laugh, life was no longer an affair of serious effort and restraint, but a toy, to be played with and turned topsy-turvy, carelessly to be lived and pleasured in, and carelessly to be flung aside. "Therefore, play!" was the cry that rang through her. "Lean toward him, if so you will, and place your two hands upon his neck!" She wanted to cry out at the recklessness of the thought, and in vain she appraised her own cleanness and culture and balanced all that she was against what he was not. She glanced about her and saw the others gazing at him with rapt attention; and she would have despaired had not she seen horror in her mother’s eyes-fascinated horror, it was true, but none the less horror. This man from outer darkness was evil. Her mother saw it, and her mother was right. She would trust her mother’s judgment in this as she had always trusted it in all things. The fire of him was no longer warm, and the fear of him was no longer poignant.

Later, at the piano, she played for him, and at him, aggressively, with the vague intent of emphasizing the impassableness of the gulf that separated them. Her music was a club that she swung brutally upon his head; and though it stunned him and crushed him down, it incited him. He gazed upon her in awe. In his mind, as in her own, the gulf widened; but faster than it widened, towered his ambition to win across it. But he was too complicated a plexus of sensibilities to sit staring at a gulf a whole evening, especially when there was music. He was remarkably susceptible to music. It was like strong drink, firing him to audacities of feeling,-a drug that laid hold of his imagination and went cloud-soaring through the sky. It banished sordid fact, flooded his mind with beauty, loosed romance and to its heels added wings. He did not understand the music she played. It was different from the dance-hall piano-banging and blatant brass bands he had heard. But he had caught hints of such music from the books, and he accepted her playing largely on faith, patiently waiting, at first, for the lifting measures of pronounced and simple rhythm, puzzled because those measures were not long continued. Just as he caught the swing of them and started, his imagination attuned in flight, always they vanished away in a chaotic scramble of sounds that was meaningless to him, and that dropped his imagination, an inert weight, back to earth.

Once, it entered his mind that there was a deliberate rebuff in all this. He caught her spirit of antagonism and strove to divine the message that her hands pronounced upon the keys. Then he dismissed the thought as unworthy and impossible, and yielded himself more freely to the music. The old delightful condition began to be induced. His feet were no longer clay, and his flesh became spirit; before his eyes and behind his eyes shone a great glory; and then the scene before him vanished and he was away, rocking over the world that was to him a very dear world. The known and the unknown were commingled in the dream-pageant that thronged his vision. He entered strange ports of sun-washed lands, and trod market-places among barbaric peoples that no man had ever seen. The scent of the spice islands was in his nostrils as he had known it on warm, breathless nights at sea, or he beat up against the southeast trades through long tropic days, sinking palm-tufted coral islets in the turquoise sea behind and lifting palm-tufted coral islets in the turquoise sea ahead. Swift as thought the pictures came and went. One instant he was astride a broncho and flying through the fairy-colored Painted Desert country; the next instant he was gazing down through shimmering heat into the whited sepulchre of Death Valley, or pulling an oar on a freezing ocean where great ice islands towered and glistened in the sun. He lay on a coral beach where the cocoanuts grew down to the mellow-sounding surf. The hulk of an ancient wreck burned with blue fires, in the light of which danced the hula dancers to the barbaric love-calls of the singers, who chanted to tinkling ukuleles and rumbling tom-toms. It was a sensuous, tropic night. In the background a volcano crater was silhouetted against the stars. Overhead drifted a pale crescent moon, and the Southern Cross burned low in the sky.

He was a harp; all life that he had known and that was his consciousness was the strings; and the flood of music was a wind that poured against those strings and set them vibrating with memories and dreams. He did not merely feel. Sensation invested itself in form and color and radiance, and what his imagination dared, it objectified in some sublimated and magic way. Past, present, and future mingled; and he went on oscillating across the broad, warm world, through high adventure and noble deeds to Her-ay, and with her, winning her, his arm about her, and carrying her on in flight through the empery of his mind.

And she, glancing at him across her shoulder, saw something of all this in his face. It was a transfigured face, with great shining eyes that gazed beyond the veil of sound and saw behind it the leap and pulse of life and the gigantic phantoms of the spirit. She was startled. The raw, stumbling lout was gone. The ill-fitting clothes, battered hands, and sunburned face remained; but these seemed the prison-bars through which she saw a great soul looking forth, inarticulate and dumb because of those feeble lips that would not give it speech. Only for a flashing moment did she see this, then she saw the lout returned, and she laughed at the whim of her fancy. But the impression of that fleeting glimpse lingered, and when the time came for him to beat a stumbling retreat and go, she lent him the volume of Swinburne, and another of Browning-she was studying Browning in one of her English courses. He seemed such a boy, as he stood blushing and stammering his thanks, that a wave of pity, maternal in its prompting, welled up in her. She did not remember the lout, nor the imprisoned soul, nor the man who had stared at her in all masculineness and delighted and frightened her. She saw before her only a boy, who was shaking her hand with a hand so calloused that it felt like a nutmeg-grater and rasped her skin, and who was saying jerkily:-

"The greatest time of my life. You see, I ain’t used to things… " He looked about him helplessly. "To people and houses like this. It’s all new to me, and I like it."

"I hope you’ll call again," she said, as he was saying good night to her brothers.

He pulled on his cap, lurched desperately through the doorway, and was gone.

"Well, what do you think of him?" Arthur demanded.

"He is most interesting, a whiff of ozone," she answered. "How old is he?"

"Twenty– almost twenty-one. I asked him this afternoon. I didn’t think he was that young."

And I am three years older, was the thought in her mind as she kissed her brothers goodnight.



CHAPTER III

As Martin Eden went down the steps, his hand dropped into his coat pocket. It came out with a brown rice paper and a pinch of Mexican tobacco, which were deftly rolled together into a cigarette. He drew the first whiff of smoke deep into his lungs and expelled it in a long and lingering exhalation. "By God!" he said aloud, in a voice of awe and wonder. "By God!" he repeated. And yet again he murmured, "By God!" Then his hand went to his collar, which he ripped out of the shirt and stuffed into his pocket. A cold drizzle was falling, but he bared his head to it and unbuttoned his vest, swinging along in splendid unconcern. He was only dimly aware that it was raining. He was in an ecstasy, dreaming dreams and reconstructing the scenes just past.

He had met the woman at last-the woman that he had thought little about, not being given to thinking about women, but whom he had expected, in a remote way, he would sometime meet. He had sat next to her at table. He had felt her hand in his, he had looked into her eyes and caught a vision of a beautiful spirit;-but no more beautiful than the eyes through which it shone, nor than the flesh that gave it expression and form. He did not think of her flesh as flesh,-which was new to him; for of the women he had known that was the only way he thought. Her flesh was somehow different. He did not conceive of her body as a body, subject to the ills and frailties of bodies. Her body was more than the garb of her spirit. It was an emanation of her spirit, a pure and gracious crystallization of her divine essence. This feeling of the divine startled him. It shocked him from his dreams to sober thought. No word, no clew, no hint, of the divine had ever reached him before. He had never believed in the divine. He had always been irreligious, scoffing good-naturedly at the sky-pilots and their immortality of the soul. There was no life beyond, he had contended; it was here and now, then darkness everlasting. But what he had seen in her eyes was soul-immortal soul that could never die. No man he had known, nor any woman, had given him the message of immortality. But she had. She had whispered it to him the first moment she looked at him. Her face shimmered before his eyes as he walked along,-pale and serious, sweet and sensitive, smiling with pity and tenderness as only a spirit could smile, and pure as he had never dreamed purity could be. Her purity smote him like a blow. It startled him. He had known good and bad; but purity, as an attribute of existence, had never entered his mind. And now, in her, he conceived purity to be the superlative of goodness and of cleanness, the sum of which constituted eternal life.

And promptly urged his ambition to grasp at eternal life. He was not fit to carry water for her-he knew that; it was a miracle of luck and a fantastic stroke that had enabled him to see her and be with her and talk with her that night. It was accidental. There was no merit in it. He did not deserve such fortune. His mood was essentially religious. He was humble and meek, filled with self-disparagement and abasement. In such frame of mind sinners come to the penitent form. He was convicted of sin. But as the meek and lowly at the penitent form catch splendid glimpses of their future lordly existence, so did he catch similar glimpses of the state he would gain to by possessing her. But this possession of her was dim and nebulous and totally different from possession as he had known it. Ambition soared on mad wings, and he saw himself climbing the heights with her, sharing thoughts with her, pleasuring in beautiful and noble things with her. It was a soul-possession he dreamed, refined beyond any grossness, a free comradeship of spirit that he could not put into definite thought. He did not think it. For that matter, he did not think at all. Sensation usurped reason, and he was quivering and palpitant with emotions he had never known, drifting deliciously on a sea of sensibility where feeling itself was exalted and spiritualized and carried beyond the summits of life.

He staggered along like a drunken man, murmuring fervently aloud: "By God! By God!"

A policeman on a street corner eyed him suspiciously, then noted his sailor roll.

"Where did you get it?" the policeman demanded.

Martin Eden came back to earth. His was a fluid organism, swiftly adjustable, capable of flowing into and filling all sorts of nooks and crannies. With the policeman’s hail he was immediately his ordinary self, grasping the situation clearly.

"It’s a beaut, ain’t it?" he laughed back. "I didn’t know I was talkin’ out loud."

"You’ll be singing next," was the policeman’s diagnosis.

"No, I won’t. Gimme a match an’ I’ll catch the next car home."

He lighted his cigarette, said good night, and went on. "Now wouldn’t that rattle you?" he ejaculated under his breath. "That copper thought I was drunk." He smiled to himself and meditated. "I guess I was," he added; "but I didn’t think a woman’s face’d do it."

He caught a Telegraph Avenue car that was going to Berkeley. It was crowded with youths and young men who were singing songs and ever and again barking out college yells. He studied them curiously. They were university boys. They went to the same university that she did, were in her class socially, could know her, could see her every day if they wanted to. He wondered that they did not want to, that they had been out having a good time instead of being with her that evening, talking with her, sitting around her in a worshipful and adoring circle. His thoughts wandered on. He noticed one with narrow-slitted eyes and a loose-lipped mouth. That fellow was vicious, he decided. On shipboard he would be a sneak, a whiner, a tattler. He, Martin Eden, was a better man than that fellow. The thought cheered him. It seemed to draw him nearer to Her. He began comparing himself with the students. He grew conscious of the muscled mechanism of his body and felt confident that he was physically their master. But their heads were filled with knowledge that enabled them to talk her talk,-the thought depressed him. But what was a brain for? he demanded passionately. What they had done, he could do. They had been studying about life from the books while he had been busy living life. His brain was just as full of knowledge as theirs, though it was a different kind of knowledge. How many of them could tie a lanyard knot, or take a wheel or a lookout? His life spread out before him in a series of pictures of danger and daring, hardship and toil. He remembered his failures and scrapes in the process of learning. He was that much to the good, anyway. Later on they would have to begin living life and going through the mill as he had gone. Very well. While they were busy with that, he could be learning the other side of life from the books.

As the car crossed the zone of scattered dwellings that separated Oakland from Berkeley, he kept a lookout for a familiar, two-story building along the front of which ran the proud sign, HIGGINBOTHAM’S CASH STORE. Martin Eden got off at this corner. He stared up for a moment at the sign. It carried a message to him beyond its mere wording. A personality of smallness and egotism and petty underhandedness seemed to emanate from the letters themselves. Bernard Higginbotham had married his sister, and he knew him well. He let himself in with a latch-key and climbed the stairs to the second floor. Here lived his brother-in-law. The grocery was below. There was a smell of stale vegetables in the air. As he groped his way across the hall he stumbled over a toy-cart, left there by one of his numerous nephews and nieces, and brought up against a door with a resounding bang. "The pincher," was his thought; "too miserly to burn two cents’ worth of gas and save his boarders’ necks."

He fumbled for the knob and entered a lighted room, where sat his sister and Bernard Higginbotham. She was patching a pair of his trousers, while his lean body was distributed over two chairs, his feet dangling in dilapidated carpet-slippers over the edge of the second chair. He glanced across the top of the paper he was reading, showing a pair of dark, insincere, sharp-staring eyes. Martin Eden never looked at him without experiencing a sense of repulsion. What his sister had seen in the man was beyond him. The other affected him as so much vermin, and always aroused in him an impulse to crush him under his foot. "Some day I’ll beat the face off of him," was the way he often consoled himself for enduring the man’s existence. The eyes, weasel-like and cruel, were looking at him complainingly.

"Well," Martin demanded. "Out with it."

"I had that door painted only last week," Mr. Higginbotham half whined, half bullied; "and you know what union wages are. You should be more careful."

Martin had intended to reply, but he was struck by the hopelessness of it. He gazed across the monstrous sordidness of soul to a chromo on the wall. It surprised him. He had always liked it, but it seemed that now he was seeing it for the first time. It was cheap, that was what it was, like everything else in this house. His mind went back to the house he had just left, and he saw, first, the paintings, and next, Her, looking at him with melting sweetness as she shook his hand at leaving. He forgot where he was and Bernard Higginbotham’s existence, till that gentleman demanded:-

"Seen a ghost?"

Martin came back and looked at the beady eyes, sneering, truculent, cowardly, and there leaped into his vision, as on a screen, the same eyes when their owner was making a sale in the store below-subservient eyes, smug, and oily, and flattering.

"Yes," Martin answered. "I seen a ghost. Good night. Good night, Gertrude."

He started to leave the room, tripping over a loose seam in the slatternly carpet.

"Don’t bang the door," Mr. Higginbotham cautioned him.

He felt the blood crawl in his veins, but controlled himself and closed the door softly behind him.

Mr. Higginbotham looked at his wife exultantly.

"He’s ben drinkin’," he proclaimed in a hoarse whisper. "I told you he would."

She nodded her head resignedly.

"His eyes was pretty shiny," she confessed; "and he didn’t have no collar, though he went away with one. But mebbe he didn’t have more’n a couple of glasses."

"He couldn’t stand up straight," asserted her husband. "I watched him. He couldn’t walk across the floor without stumblin’. You heard ’m yourself almost fall down in the hall."

"I think it was over Alice’s cart," she said. "He couldn’t see it in the dark."

Mr. Higginbotham’s voice and wrath began to rise. All day he effaced himself in the store, reserving for the evening, with his family, the privilege of being himself.

"I tell you that precious brother of yours was drunk."

His voice was cold, sharp, and final, his lips stamping the enunciation of each word like the die of a machine. His wife sighed and remained silent. She was a large, stout woman, always dressed slatternly and always tired from the burdens of her flesh, her work, and her husband.

"He’s got it in him, I tell you, from his father," Mr. Higginbotham went on accusingly. "An’ he’ll croak in the gutter the same way. You know that."

She nodded, sighed, and went on stitching. They were agreed that Martin had come home drunk. They did not have it in their souls to know beauty, or they would have known that those shining eyes and that glowing face betokened youth’s first vision of love.

"Settin’ a fine example to the children," Mr. Higginbotham snorted, suddenly, in the silence for which his wife was responsible and which he resented. Sometimes he almost wished she would oppose him more. "If he does it again, he’s got to get out. Understand! I won’t put up with his shinanigan-debotchin’ innocent children with his boozing." Mr. Higginbotham liked the word, which was a new one in his vocabulary, recently gleaned from a newspaper column. "That’s what it is, debotchin’-there ain’t no other name for it."

Still his wife sighed, shook her head sorrowfully, and stitched on. Mr. Higginbotham resumed the newspaper.

"Has he paid last week’s board?" he shot across the top of the newspaper.

She nodded, then added, "He still has some money."

"When is he goin’ to sea again?"

"When his pay-day’s spent, I guess," she answered. "He was over to San Francisco yesterday looking for a ship. But he’s got money, yet, an’ he’s particular about the kind of ship he signs for."

"It’s not for a deck-swab like him to put on airs," Mr. Higginbotham snorted. "Particular! Him!"

"He said something about a schooner that’s gettin’ ready to go off to some outlandish place to look for buried treasure, that he’d sail on her if his money held out."

"If he only wanted to steady down, I’d give him a job drivin’ the wagon," her husband said, but with no trace of benevolence in his voice. "Tom’s quit."

His wife looked alarm and interrogation.

"Quit to– night. Is goin’ to work for Carruthers. They paid ’m more’n I could afford."

"I told you you’d lose ’m," she cried out. "He was worth more’n you was giving him."

"Now look here, old woman," Higginbotham bullied, "for the thousandth time I’ve told you to keep your nose out of the business. I won’t tell you again."

"I don’t care," she sniffled. "Tom was a good boy." Her husband glared at her. This was unqualified defiance.

"If that brother of yours was worth his salt, he could take the wagon," he snorted.

"He pays his board, just the same," was the retort. "An’ he’s my brother, an’ so long as he don’t owe you money you’ve got no right to be jumping on him all the time. I’ve got some feelings, if I have been married to you for seven years."

"Did you tell ’m you’d charge him for gas if he goes on readin’ in bed?" he demanded.

Mrs. Higginbotham made no reply. Her revolt faded away, her spirit wilting down into her tired flesh. Her husband was triumphant. He had her. His eyes snapped vindictively, while his ears joyed in the sniffles she emitted. He extracted great happiness from squelching her, and she squelched easily these days, though it had been different in the first years of their married life, before the brood of children and his incessant nagging had sapped her energy.

"Well, you tell ’m to-morrow, that’s all," he said. "An’ I just want to tell you, before I forget it, that you’d better send for Marian to-morrow to take care of the children. With Tom quit, I’ll have to be out on the wagon, an’ you can make up your mind to it to be down below waitin’ on the counter."

"But to– morrow’s wash day," she objected weakly.

"Get up early, then, an’ do it first. I won’t start out till ten o’clock."

He crinkled the paper viciously and resumed his reading.



CHAPTER IV

Martin Eden, with blood still crawling from contact with his brother-in-law, felt his way along the unlighted back hall and entered his room, a tiny cubbyhole with space for a bed, a wash-stand, and one chair. Mr. Higginbotham was too thrifty to keep a servant when his wife could do the work. Besides, the servant’s room enabled them to take in two boarders instead of one. Martin placed the Swinburne and Browning on the chair, took off his coat, and sat down on the bed. A screeching of asthmatic springs greeted the weight of his body, but he did not notice them. He started to take off his shoes, but fell to staring at the white plaster wall opposite him, broken by long streaks of dirty brown where rain had leaked through the roof. On this befouled background visions began to flow and burn. He forgot his shoes and stared long, till his lips began to move and he murmured, "Ruth."

"Ruth." He had not thought a simple sound could be so beautiful. It delighted his ear, and he grew intoxicated with the repetition of it. "Ruth." It was a talisman, a magic word to conjure with. Each time he murmured it, her face shimmered before him, suffusing the foul wall with a golden radiance. This radiance did not stop at the wall. It extended on into infinity, and through its golden depths his soul went questing after hers. The best that was in him was out in splendid flood. The very thought of her ennobled and purified him, made him better, and made him want to be better. This was new to him. He had never known women who had made him better. They had always had the counter effect of making him beastly. He did not know that many of them had done their best, bad as it was. Never having been conscious of himself, he did not know that he had that in his being that drew love from women and which had been the cause of their reaching out for his youth. Though they had often bothered him, he had never bothered about them; and he would never have dreamed that there were women who had been better because of him. Always in sublime carelessness had he lived, till now, and now it seemed to him that they had always reached out and dragged at him with vile hands. This was not just to them, nor to himself. But he, who for the first time was becoming conscious of himself, was in no condition to judge, and he burned with shame as he stared at the vision of his infamy.

He got up abruptly and tried to see himself in the dirty looking-glass over the wash-stand. He passed a towel over it and looked again, long and carefully. It was the first time he had ever really seen himself. His eyes were made for seeing, but up to that moment they had been filled with the ever changing panorama of the world, at which he had been too busy gazing, ever to gaze at himself. He saw the head and face of a young fellow of twenty, but, being unused to such appraisement, he did not know how to value it. Above a square-domed forehead he saw a mop of brown hair, nut-brown, with a wave to it and hints of curls that were a delight to any woman, making hands tingle to stroke it and fingers tingle to pass caresses through it. But he passed it by as without merit, in Her eyes, and dwelt long and thoughtfully on the high, square forehead,-striving to penetrate it and learn the quality of its content. What kind of a brain lay behind there? was his insistent interrogation. What was it capable of? How far would it take him? Would it take him to her?

He wondered if there was soul in those steel-gray eyes that were often quite blue of color and that were strong with the briny airs of the sun-washed deep. He wondered, also, how his eyes looked to her. He tried to imagine himself she, gazing into those eyes of his, but failed in the jugglery. He could successfully put himself inside other men’s minds, but they had to be men whose ways of life he knew. He did not know her way of life. She was wonder and mystery, and how could he guess one thought of hers? Well, they were honest eyes, he concluded, and in them was neither smallness nor meanness. The brown sunburn of his face surprised him. He had not dreamed he was so black. He rolled up his shirt-sleeve and compared the white underside if the arm with his face. Yes, he was a white man, after all. But the arms were sunburned, too. He twisted his arm, rolled the biceps over with his other hand, and gazed underneath where he was least touched by the sun. It was very white. He laughed at his bronzed face in the glass at the thought that it was once as white as the underside of his arm; nor did he dream that in the world there were few pale spirits of women who could boast fairer or smoother skins than he-fairer than where he had escaped the ravages of the sun.

His might have been a cherub’s mouth, had not the full, sensuous lips a trick, under stress, of drawing firmly across the teeth. At times, so tightly did they draw, the mouth became stern and harsh, even ascetic. They were the lips of a fighter and of a lover. They could taste the sweetness of life with relish, and they could put the sweetness aside and command life. The chin and jaw, strong and just hinting of square aggressiveness, helped the lips to command life. Strength balanced sensuousness and had upon it a tonic effect, compelling him to love beauty that was healthy and making him vibrate to sensations that were wholesome. And between the lips were teeth that had never known nor needed the dentist’s care. They were white and strong and regular, he decided, as he looked at them. But as he looked, he began to be troubled. Somewhere, stored away in the recesses of his mind and vaguely remembered, was the impression that there were people who washed their teeth every day. They were the people from up above-people in her class. She must wash her teeth every day, too. What would she think if she learned that he had never washed his teeth in all the days of his life? He resolved to get a tooth-brush and form the habit. He would begin at once, to-morrow. It was not by mere achievement that he could hope to win to her. He must make a personal reform in all things, even to tooth-washing and neck-gear, though a starched collar affected him as a renunciation of freedom.

He held up his hand, rubbing the ball of the thumb over the calloused palm and gazing at the dirt that was ingrained in the flesh itself and which no brush could scrub away. How different was her palm! He thrilled deliciously at the remembrance. Like a rose-petal, he thought; cool and soft as a snowflake. He had never thought that a mere woman’s hand could be so sweetly soft. He caught himself imagining the wonder of a caress from such a hand, and flushed guiltily. It was too gross a thought for her. In ways it seemed to impugn her high spirituality. She was a pale, slender spirit, exalted far beyond the flesh; but nevertheless the softness of her palm persisted in his thoughts. He was used to the harsh callousness of factory girls and working women. Well he knew why their hands were rough; but this hand of hers… It was soft because she had never used it to work with. The gulf yawned between her and him at the awesome thought of a person who did not have to work for a living. He suddenly saw the aristocracy of the people who did not labor. It towered before him on the wall, a figure in brass, arrogant and powerful. He had worked himself; his first memories seemed connected with work, and all his family had worked. There was Gertrude. When her hands were not hard from the endless housework, they were swollen and red like boiled beef, what of the washing. And there was his sister Marian. She had worked in the cannery the preceding summer, and her slim, pretty hands were all scarred with the tomato-knives. Besides, the tips of two of her fingers had been left in the cutting machine at the paper-box factory the preceding winter. He remembered the hard palms of his mother as she lay in her coffin. And his father had worked to the last fading gasp; the horned growth on his hands must have been half an inch thick when he died. But Her hands were soft, and her mother’s hands, and her brothers’. This last came to him as a surprise; it was tremendously indicative of the highness of their caste, of the enormous distance that stretched between her and him.

He sat back on the bed with a bitter laugh, and finished taking off his shoes. He was a fool; he had been made drunken by a woman’s face and by a woman’s soft, white hands. And then, suddenly, before his eyes, on the foul plaster-wall appeared a vision. He stood in front of a gloomy tenement house. It was night-time, in the East End of London, and before him stood Margey, a little factory girl of fifteen. He had seen her home after the bean-feast. She lived in that gloomy tenement, a place not fit for swine. His hand was going out to hers as he said good night. She had put her lips up to be kissed, but he wasn’t going to kiss her. Somehow he was afraid of her. And then her hand closed on his and pressed feverishly. He felt her callouses grind and grate on his, and a great wave of pity welled over him. He saw her yearning, hungry eyes, and her ill-fed female form which had been rushed from childhood into a frightened and ferocious maturity; then he put his arms about her in large tolerance and stooped and kissed her on the lips. Her glad little cry rang in his ears, and he felt her clinging to him like a cat. Poor little starveling! He continued to stare at the vision of what had happened in the long ago. His flesh was crawling as it had crawled that night when she clung to him, and his heart was warm with pity. It was a gray scene, greasy gray, and the rain drizzled greasily on the pavement stones. And then a radiant glory shone on the wall, and up through the other vision, displacing it, glimmered Her pale face under its crown of golden hair, remote and inaccessible as a star.

He took the Browning and the Swinburne from the chair and kissed them. Just the same, she told me to call again, he thought. He took another look at himself in the glass, and said aloud, with great solemnity:-

"Martin Eden, the first thing to-morrow you go to the free library an’ read up on etiquette. Understand!"

He turned off the gas, and the springs shrieked under his body.

"But you’ve got to quit cussin’, Martin, old boy; you’ve got to quit cussin’," he said aloud.

Then he dozed off to sleep and to dream dreams that for madness and audacity rivalled those of poppy-eaters.'''
    key = u"kfdsffjskdfjdkfd"
    # lettetsRate = calculateLettersRate(text138, 10)
    # print(lettetsRate)
    # print(lettetsRate)


    text138 = deleteChangeBadSymbols(text138)
    text138 = text138.upper()
    print(text138.__len__())
    lettetsRate = calculateLettersRate(text138, 30)
    print(lettetsRate)
    print(text138)
    key_count(cipher(text138, key))

