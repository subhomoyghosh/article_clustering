# python3.7 -m pip install newspaper3k
# python3.7 -m pip install -r requirements.txt
# python3.7 -m pip install -r bs4
# python3.7 -m pip install -r colorama
# python3.7 -m pip install -r htmldate

import os
from htmldate import find_date

######################################
## FUNCTION TO TRIM LINKS
######################################

def trimLinks(basepath, fname, website, dt):
    # read links
    with open(basepath + fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    # get only relevant links from mentioned day dt
    links = []
    for element in content:
        dtcontent = find_date(element)
        if dt == dtcontent:
            links.append(element)

    # save data
    fout = basepath + website.split('.')[1] + '.txt'
    with open(fout, "w") as output:
        for item in links:
            output.write("%s\n" % item)




######################
###### GET URL
######################

## basepath
basepath='your_path/'
final_outpath='your_path/data/'

## website links to get links from
weblinks=['https://www.theguardian.com/world/2020/oct/06/all',
          'https://www.cnn.com/world',
          'https://www.nytimes.com/section/world',
          'https://www.bbc.com/news/world']
nlinks= len(weblinks)

## get names of the websites and names of saved txt files
websites=[];
txtfiles=[];
for i in range(0,nlinks):
    websites.append(weblinks[i].split('/')[2])
    txtfiles.append(websites[i]+'_internal_links.txt')

## extract links https://www.thepythoncode.com/article/extract-all-website-links-python
## github code: https://github.com/x4nth055/pythoncode-tutorials/tree/master/web-scraping/link-extractor
for i in range(0,nlinks):
 command = 'python3 link_extractor.py ' + weblinks[i] + ' -m' + ' 15'
 os.system(command)


######################
###### TRIM URL
######################
dt='2020-10-06'

## trim urls
 for i in range(0,nlinks):
   fname= txtfiles[i]
   website=websites[i]
   trimLinks(basepath,fname,website,dt)


######################
###### GET DATA FROM URLS
######################

## Download articles and process
from newspaper import Article
import string
k=0
narticle_media=15

## read file one by one and download all texts
for i in range(0,nlinks):
  website=websites[i]
  fname= basepath + website.split('.')[1] + '.txt'
  file1 = open(fname, 'r')
  content = file1.readlines()
  content = [x.strip() for x in content]
  clen=len(content)

  if narticle_media > clen:
     narticle_media=clen

  for j in range(0,narticle_media):
   ## parse
   article = Article(content[j])
   article.download()
   article.parse()
   ## save (add article number)
   article_number=str(k).zfill(3);
   title=article.title.translate(str.maketrans('', '', string.punctuation)).lower().replace(" ", "_")
   title_with_number= title + '-'+ article_number
   fout=final_outpath + title_with_number + '.txt'
   with open(fout, "w") as text_file:
   text_file.write(article.text)
   k=k+1




