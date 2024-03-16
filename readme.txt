step 1.
執行line_fact_check.py 下載虛假新聞
執行real_news.py 下載真實新聞

step 2.
執行split.data把資料切割成training data、validation data和testing data，並處存到dataset資料夾下 (要手動替換是真實新聞(real)還是虛假新聞(fake))

step 3.
執行probability_real_key_generator.py，此程式會找出每篇文章的關鍵字，並記錄每個關鍵字出現在真實新聞的機率和出現在虛假新聞的機率，並處存到dataset/probability_real_key.txt

stpe 4.
執行evaluation.py，使用dataset/real_artice_testing.txt、dataset/fake_article_testing.txt、dataset/real_article_validation.txt和dataset/fake_article_validation.txt評估找到的key的好壞以及threshold設定的好壞。

作者: 林裕翔