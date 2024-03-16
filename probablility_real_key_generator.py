import json
import jieba
import itertools

real_data='dataset/real_article_train.txt'
fake_data='dataset/fake_article_train.txt'
save_probability_real_key_file='dataset/probability_real_key.txt'

def key_word_generator(file_paths,key_word_threshold=0.005,zipf=True):
    articles=[]
    for file_path in file_paths:
        with open(file_path,'r',encoding='UTF-8') as file:
            articles+=json.loads(file.read())
        # all_word='。'.join(articles)

    num_articles=len(articles)
    articles_words=[]
    for article in articles:
        article_words = list(jieba.cut(article, cut_all=False))  # 精確模式分詞
        articles_words.append(article_words)

    all_words=list(itertools.chain(*articles_words))

    
    articles_word_dict=[dict() for _ in range(num_articles)]
    all_word_dict=dict()
    for counter,article in enumerate(articles_words):
        for word in article:
            if word not in articles_word_dict[counter]:
                articles_word_dict[counter][word]=1
            else:
                articles_word_dict[counter][word]+=1

    for word in all_words:
        if word not in all_word_dict:
           all_word_dict[word]=1
        else:
            all_word_dict[word]+=1

    probability_articles_word=[dict() for _ in range(num_articles)]
    probability_all_word=dict()
    if zipf:
        for counter,article in enumerate(articles_word_dict):
            article_word_list=list(zip(article.keys(),article.values()))
            article_word_list.sort(key=lambda x:x[1])
            cl=0
            for rank in range(1,len(article_word_list)+1):
                cl+=1/rank

            for rank,word in enumerate(article_word_list):
                probability_articles_word[counter][word[0]]=(1/cl)*(1/(rank+1))

        all_word_list=list(zip(all_word_dict.keys(),all_word_dict.values()))
        all_word_list.sort(key=lambda x:x[1])
        cl=0
        for rank in range(1,len(all_word_list)+1):
            cl+=1/rank

        for rank,word in enumerate(all_word_list):
            probability_all_word[word[0]]=(1/cl)*(1/(rank+1))

    else:
        for counter,article in enumerate(articles_word_dict):
            article_word_list=list(zip(article.keys(),article.values()))
            article_word_list.sort(key=lambda x:x[1])
            num_words=0
            for num_specific_word in article_word_list:
                num_words+=num_specific_word[1]

            for word in article_word_list:
                probability_articles_word[counter][word[0]]=word[1]/num_words

        all_word_list=list(zip(all_word_dict.keys(),all_word_dict.values()))
        all_word_list.sort(key=lambda x:x[1])
        num_words=0
        for num_specific_word in all_word_list:
            num_words+=num_specific_word[1]

        for word in all_word_list:
            probability_all_word[word[0]]=word[1]/num_words

    
    # print(f'all {probability_all_word["一項"]} article {probability_articles_word[0]["一項"]}')
    article_key_word=[{'content':article,'key_words':dict()} for article in articles]
    for counter,article in enumerate(probability_articles_word):
        for word in article.items():
            importance=word[1]/num_articles/probability_all_word[word[0]]
            if importance>=key_word_threshold:
                article_key_word[counter]['key_words'][word[0]]=importance
    
    return article_key_word

def probability_real_word(key_words,real_data,fake_data, scale=1e6):
    with open(real_data,'r',encoding='UTF-8') as file:
        real_articles=json.loads(file.read())

    with open(fake_data,'r',encoding='UTF-8') as file:
        fake_articles=json.loads(file.read())



    real_words_dict=dict()
    fake_words_dict=dict()
    sum_real_key_word=0
    sum_fake_key_word=0
    for article in real_articles:
        words= list(jieba.cut(article, cut_all=False))  # 精確模式分詞
        for word in words:
            if word not in real_words_dict:
                real_words_dict[word]=1
                sum_real_key_word+=1
            else:
                real_words_dict[word]+=1
                sum_real_key_word+=1

    for article in fake_articles:
        words= list(jieba.cut(article, cut_all=False))  # 精確模式分詞
        for word in words:
            if word not in fake_words_dict:
                fake_words_dict[word]=1
                sum_fake_key_word+=1
            else:
                fake_words_dict[word]+=1
                sum_fake_key_word+=1

    probability_real_key_word=dict()
    for key_word in key_words:
        if key_word in real_words_dict:
            real_times=real_words_dict[key_word]
        else:
            continue

        if key_word in fake_words_dict:
            fake_times=fake_words_dict[key_word]
        else:
            continue

        prob={'probability_real':real_times*scale/sum_real_key_word, 'probability_fake':fake_times*scale/sum_fake_key_word}
        probability_real_key_word[key_word]=prob


    return probability_real_key_word

    

if __name__=="__main__":
    key_word_with_contents=key_word_generator([real_data,fake_data],0.5,False)
    key_words=[]
    for key_word_with_content in key_word_with_contents:
        key_words+=list(key_word_with_content['key_words'].keys())
    
    prob_key=probability_real_word(key_words,real_data,fake_data)
    
    with open(save_probability_real_key_file,'w',encoding='UTF-8') as file:
        file.write(json.dumps(prob_key))
    



    # probability_real_key_word
