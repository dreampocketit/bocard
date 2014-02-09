PYTHON中文處理整合版 - 2012/01/05 

please feedback to : skylock777@gmail.com

作業系統需求:
1.win xp/2000/vista/7
系統環境需求:
2.python 2.x 版本 (建議使用python 2.6 or 2.7)
3.nltk模組 (PyYAML,numpy,nltk)
以上軟體皆可在以下網站找到:
http://www.nltk.org/download

使用說明:

1.在命令提示字元視窗底下進到檔案所在目錄下執行LACC.py
  指令輸入建議加上python確保系統知道怎麼執行python:
  python LACC.py

2.關於語料庫:
    a.ASBC為中研院斷詞語料庫，含有詞性標記 
      文本如使用中研院斷詞系統斷過詞的
      請放進這個資料夾下
    b.SSC為中研院分詞語料庫，不含詞性標記
      文本如使用中研院斷詞系統分過詞的
      請放進這個資料夾下
      (上面兩種語料庫目前只支援 utf-8 編碼格式的文字)
    c.MyCorpus為自訂語料庫，可以接受未處理過的文本
      (目前只支援 big5 編碼格式的文字)

3.選項說明
  在決定好使用的語料庫之後，系統會根據使用的語料庫種類產生相對應的功能選單，NLTK中文處理的功能包含以下幾種：

    Concordance:找出關鍵字在文本中出現的句子。
    Collocations：找出文本中常出現的連接詞。
    Similar words：找出文本中跟關鍵字相似度最高的字詞 。
    Common context：找出文本中兩個關鍵字都有出現的前後文。
    Find text patterns：找出文本中包含兩個關鍵字在句子中特定 位置出現的文字。
    Right and Left terms of a Chinese character：找出文本中關鍵字的左接詞以及右接詞。選擇這個選項後系統會再跑出兩個選項:
    show all RLgrams depends on user's input:
    用自行輸入的字詞尋找臨群數，系統會根據找到數量的多寡決定是否儲存到文字檔。
    show all RLgrams for all bi-words in a corpus:
    找出語料中所有雙字詞的臨群數，系統會直接儲存到文字檔裡面。
    Generate a random text：以輸入的關鍵字為基礎隨機產生一段文字。
    Find text patterns with POS tags：與Find text patterns類似，差別在於改以詞性作為判斷依據。

    其中第八個選項是要在語料庫是包含詞性標註的情況下才會出現。

    字劃字音分析的功能共分為四大類：1.筆畫 2.注音 3.音調 4.應用。包括以下幾種：

    sum of all word's stroke：計算所有文字的筆畫總和。
    show all word's stroke：計算所有文字對應的筆畫，若字數過多則另存到文字檔。
    show all word's phone：計算所有文字對應的注音，若字數過多則另存到文字檔。
    show all word's consonat or vowel：計算所有文字對應的韻腳或韻母，若字數過多則另存到文字檔。
    show all word's tone：計算所有文字對應的聲調，若字數過多則另存到文字檔。
    show all repeat-final in bi-words：找出所有文字中韻母、聲調相同的雙字詞。
    show all repeated bi-words：找出所有疊字。
    poem validation：判斷一段文字是否為五言絕句，若否則回傳不符合的規則。
