from nltk.corpus import stopwords
import gensim.models.keyedvectors as word2vec
import time
import os
from Extractrubric import runrubric, Question

stop_words = set(stopwords.words('english'))


def preprocessing(sentence):
    sentence = sentence.lower().split()   #lower and split into list
    sentence = [w for w in sentence if w not in stop_words]     #Remove Stopwords
    return sentence
    

def wordmoverdist(sent1, sent2, model):
    distance = model.wmdistance(sent1, sent2)
    return distance

def marksallot_partiall(distance, maxmarks):
    mist_dist = 0
    if distance <= 2.2:
        mist_dist = 0
    elif distance > 2.2 and distance <= 3.2:
        mist_dist = (distance - 2.2)*100
    else:
        mist_dist = 100

    obtained_marks = ((100 - mist_dist)/100)*maxmarks

    return round(obtained_marks, 2)


def marksallot_binary(distance, maxmarks):
    if distance <= 2.2:
        return maxmarks
    else:
        return 0


def oneword_fill(sent1, sent2, maxmarks):
    if sent1.lower() == sent2.lower():
        return maxmarks
    else:
        return 0


def truefalse(sent1, sent2, maxmarks):
    #sent1 is rubric and sent2 is student
    if sent1.lower() == 'true'or sent1.lower() == 't':
        if sent2.lower() == 'true' or sent2.lower() == 't':
            return maxmarks
        else:
            return 0
    elif sent1.lower() == 'false' or sent1.lower() == 't':
        if sent2.lower() == 'false' or sent2.lower() == 'f':
            return maxmarks
        else:
            return 0




if __name__ == '__main__':

    rubric_dict = runrubric(10)
    for i in rubric_dict.keys():
        print(i)
        print(rubric_dict[i].answer)
        print(rubric_dict[i].answer_list)
        print(rubric_dict[i].marks_list)
        print(rubric_dict[i].question_type)
        print(rubric_dict[i].partial)
    if 'Q5)' in rubric_dict.keys():
        print("Q5")
        print(rubric_dict['Q5)'])



    print("Now Model loading starting")

    
    #path of a trained data of word2Vec
    if not os.path.exists('D:\GoogleNews-vectors-negative300.bin.gz'):
        raise ValueError("download the google news model")
    #load the trained model
    model = word2vec.KeyedVectors.load_word2vec_format('D:\GoogleNews-vectors-negative300.bin.gz', binary=True)









    sentence_1 = 'In the present study, we used this difference between the perception of schematic and natural eyes to examine whether induction of a face context may trigger face-specific activity during processing of stimuli that are not normally perceived as face component.'
    sentence_2 = 'This disparity in interpretation between model and natural eyes was included in this research to see whether inducing a face meaning could cause facial behavior throughout perception of stimuli that are not usually perceived as face components.'
    question_type = 'subjective'
    partial_marking = 0  #if partial available is 1, if not is 0  
    max_marks = 5

    if question_type == 'subjective':
        distance = wordmoverdist(preprocessing(sentence_1), preprocessing(sentence_2), model)
        obt_mark = marksallot_partiall(distance, max_marks)
        print('distance = %.4f' % distance, "     Marks = ", obt_mark)   



    sentence_1 = 'This disparity in interpretation between model and natural eyes was negligible'
    sentence_2 = 'The president greets the press in chicago'

    distance = wordmoverdist(preprocessing(sentence_1), preprocessing(sentence_2), model)
    obt_mark = marksallot_partiall(distance, max_marks)
    print('distance = %.4f' % distance, "     Marks = ", obt_mark)

    sentence_1 = 'I installed Anaconda3 4.4.0 (32 bit) on my Windows 7 Professional machine and imported NumPy and Pandas on Jupyter notebook so I assume Python was installed correctly.'
    sentence_2 = 'The virus that causes COVID-19 is mainly transmitted through droplets generated when an infected person coughs, sneezes, or exhales and these droplets are too heavy to hang in the air, and quickly fall on floors or surfaces.'

    distance = wordmoverdist(preprocessing(sentence_1), preprocessing(sentence_2), model)
    obt_mark = marksallot_partiall(distance, max_marks)
    print('distance = %.4f' % distance, "     Marks = ", obt_mark)

    sentence_1 = 'In Link State routing , routers calculate the paths to all other nodes based on the knowledge of all paths in the network. In Distance Vector routing , routers calculate distances to neighbours only through advertisement. Hence , the computational overhead of the Link State router is larger than Distance Vector Routing.'
    sentence_2 = 'Here link-state protocol is higher than the Distance vector protocol due to the Link-state routing is work on the basis of global information like all node computing the shortest path for the whole network; on the other hand, distance vector routing is based on Local information. So, here Link state Routing protocol will be used.'

    distance = wordmoverdist(preprocessing(sentence_1), preprocessing(sentence_2), model)
    obt_mark = marksallot_partiall(distance, max_marks)
    print('distance = %.4f' % distance, "     Marks = ", obt_mark)

    sentence_1 = 'Here link-state protocol is higher than the Distance vector protocol due to the Link-state routing is work on the basis of global information like all node computing the shortest path for the whole network; on the other hand, distance vector routing is based on Local information. So, here Link state Routing protocol will be used.'
    sentence_2 = 'Link state Routing protocol will be used.'

    distance = wordmoverdist(preprocessing(sentence_1), preprocessing(sentence_2), model)
    obt_mark = marksallot_partiall(distance, max_marks)
    print('distance = %.4f' % distance, "     Marks = ", obt_mark)
    
    sentence_1 = 'Here link-state protocol is higher than the Distance vector protocol due to the Link-state routing is work on the basis of global information like all node computing the shortest path for the whole network; on the other hand, distance vector routing is based on Local information. So, here Link state Routing protocol will be used.'
    sentence_2 = 'link-state protocol is larger compare to Distance vector protocol due to the Link-state routing is work on the principle of global information such as computing the shortest path for all node in whole network; and here, distance vector routing is based on Local information. So, here Link state Routing protocol is best for used.'

    distance = wordmoverdist(preprocessing(sentence_1), preprocessing(sentence_2), model)
    obt_mark = marksallot_partiall(distance, max_marks)
    print('distance = %.4f' % distance, "     Marks = ", obt_mark)


    sentence_1 = 'obama speaks to the media in Illinois'
    sentence_2 = 'The president greets the press in chicago'

    distance = wordmoverdist(preprocessing(sentence_1), preprocessing(sentence_2), model)
    obt_mark = marksallot_partiall(distance, max_marks)
    print('distance = %.4f' % distance, "     Marks = ", obt_mark)




#print("second", time.process_time())
#lower the sentence
'''sentence_1 = sentence_1.lower().split()
sentence_2 = sentence_2.lower().split()


# Remove stopwords.
sentence_1 = [w for w in sentence_1 if w not in stop_words]
sentence_2 = [w for w in sentence_2 if w not in stop_words]


distance = model.wmdistance(sentence_1, sentence_2)
print('distance = %.4f' % distance)

print("third", time.process_time())




sentence_3 = 'This disparity in interpretation between model and natural eyes was negligible'
#sentence_3 = 'obama speaks to the media in Illinois'
sentence_4 = 'The president greets the press in chicago'


#lower the sentence
sentence_3 = sentence_3.lower().split()
sentence_4 = sentence_4.lower().split()


# Remove stopwords.
sentence_3 = [w for w in sentence_3 if w not in stop_words]
sentence_4 = [w for w in sentence_4 if w not in stop_words]


distance2 = model.wmdistance(sentence_3, sentence_4)
print('distance = %.4f' % distance2)

print("fourth", time.process_time())'''



