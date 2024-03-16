import json

source_file="dataset/real_article.txt"
training_file="dataset/real_article_train.txt"
validation_file="dataset/real_article_validation.txt"
testing_file="dataset/real_article_testing.txt"

split_ratio=[0.7,0.1,0.2]

articles=[]

with open(source_file,'r',encoding='UTF=8') as file:
    articles=json.loads(file.read())

# for i in articles:
#     print(i)
#     print()
    
training_data=articles[:int(len(articles)*split_ratio[0])]
validation_data=articles[int(len(articles)*split_ratio[0]):int(len(articles)*(1-split_ratio[2]))]
testing_data=articles[int(len(articles)*(1-split_ratio[2])):]

with open(training_file,'w',encoding='UTF-8') as file:
    file.write(json.dumps(training_data))

with open(validation_file,'w',encoding='UTF-8') as file:
    file.write(json.dumps(validation_data))

with open(testing_file,'w',encoding='UTF-8') as file:
    file.write(json.dumps(testing_data))

