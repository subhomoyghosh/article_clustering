# python3.7 -m pip install newspaper3k
# python3.7 -m pip install -r requirements.txt
# python3.7 -m pip install -r bs4
# python3.7 -m pip install -r colorama

import os

######################################
## FUNCTION TO TRIM LINKS
######################################

def trimLinks(basepath,fname,website,IsEndWithNumber,keywords):

  # read links
  with open(basepath+fname) as f:
    content = f.readlines()
  # you may also want to remove whitespace characters like `\n` at the end of each line
  content = [x.strip() for x in content]

  # does the link have date if yes=extract or keep as is
  n= len(keywords)


  # get only relevant links from same day!
  links=[]

  # this depnds on whether links end with number or contain the date inside
   if isEndWithNumber==0:
    for element in content:
      if len(set(keywords) & set(element.split('/'))) ==(n-1):
        print(element)
        links.append(element)
   else:
    for element in content:
     # does the link end with number (for bbc)
     m = re.search(r'\d+$', element)
     # if the string ends in digits m will be a Match object, or None otherwise.
      if m is not None:
        print(element)
        links.append(element)

     # save all relevant links in a text file
    fout= basepath + website.split('.')[1] + '.txt'
      with open(fout, "w") as output:
        for item in links:
          output.write("%s\n" % item)




######################
###### GET URL
######################

## basepaths
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

## trim urls
keywords=['https:','2020','oct','10','06']
 for i in range(0,nlinks):
   fname= txtfiles[i]
   website=websites[i]
   if i< nlinks-1:
     isEndWithNumber=0
    else:
     isEndWithNumber = 1
   print(i)
   trimLinks(basepath,fname,website,isEndWithNumber,keywords)


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


