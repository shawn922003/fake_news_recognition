import json
import jieba

real_test_data='dataset/real_article_testing.txt'
fake_test_data='dataset/fake_article_testing.txt'
real_val_data='dataset/real_article_validation.txt'
fake_val_data='dataset/fake_article_validation.txt'
probability_real_key_file='dataset/probability_real_key.txt'

def real_probability(probability_real_key_file,eval_file,article_threshold=0.01):
    with open(probability_real_key_file,'r',encoding='UTF-8') as file:
        probability_real_key=json.loads(file.read())

    with open(eval_file,'r',encoding='UTF-8') as file:
        articles=json.loads(file.read())

    articles_key_words=[]
    for article in articles:
        articles_key_words.append(list(jieba.cut(article, cut_all=False)))

    # probability_real_key_ratio=0
    # for prob in probability_real_key.values():
    #     if prob>=key_threshood:
    #         probability_real_key_ratio+=1
    # probability_real_key_ratio/=len(probability_real_key)

    result=[]
    for article in articles_key_words:
        prob_real_word=1
        prob_fake_word=1
        for word in article:
            if word in probability_real_key:
                prob_real_word*=probability_real_key[word]['probability_real']
                prob_fake_word*=probability_real_key[word]['probability_fake']

            
        prob_real=prob_real_word/(prob_real_word+prob_fake_word)
        result.append(prob_real>=article_threshold)
    return result


if __name__=="__main__":
    real_val_result=real_probability(probability_real_key_file,real_val_data)
    val_acc=0
    for i in real_val_result:
        if i==True:
            val_acc+=1
        

    fake_val_result=real_probability(probability_real_key_file,fake_val_data)
    fake_val_acc=0
    for i in fake_val_result:
        if i==False:
            val_acc+=1
    val_acc/=(len(real_val_result)+len(fake_val_result))


    real_test_result=real_probability(probability_real_key_file,real_test_data)
    test_acc=0
    for i in real_test_result:
        if i==True:
            test_acc+=1


    fake_test_result=real_probability(probability_real_key_file,fake_test_data)
    for i in fake_test_result:
        if i==False:
            test_acc+=1
    test_acc/=(len(fake_test_result)+len(real_test_result))

    print(f'val: {val_acc}, test:  {test_acc}')




    

    


