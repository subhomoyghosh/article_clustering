# python3.7 -m pip install newspaper3k
# python3.7 -m pip install -r requirements.txt
# python3.7 -m pip install -r bs4
# python3.7 -m pip install -r colorama
# python3.7 -m pip install -r htmldate

import os
from htmldate import find_date
import sys
import glob

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
basepath='your_path'
final_outpath='your_path/data/'

## website links to get links from
weblinks=['https://www.theguardian.com/world/2020/oct/06/all',
          'https://www.cnn.com/world',
          'https://www.nytimes.com/section/world',
          'https://www.bbc.com/news/world',
          'https://www.reuters.com/news/world']
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
k=1
narticle_media=100

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
   title=article.title.translate(str.maketrans('', '', string.punctuation)).lower().replace(" ", "_")
   title_titletext= title
   fout=final_outpath + 'article-' + str(k) + '.txt'
   fout_title= final_outpath + 'title-' + str(k) + '.txt'
   with open(fout, "w") as text_file:
   text_file.write(article.text)
   with open(fout_title, "w") as text_file:
   text_file.write(title_titletext)
   k=k+1


## delete small files
p1='your_path/data/article*'
p2='your_path/data/title*'
files1 = glob.glob(p1)
files2=glob.glob(p2)
nfl= len(files1)

# file with paths
files_path1 = []
files_path2 = []
 for i in range(0,nfl):
    files_path1.append(files1[i])
    files_path2.append(files2[i])

# delete small files and titles as well
 for i in range(0,nfl):
   if os.path.getsize(files_path1[i]) < 1024:
      os.remove(files_path1[i])
      os.remove(files_path2[i])


## again read and rename to make naming continuous
files1 = glob.glob(p1)
files2=glob.glob(p2)
nfl= len(files1)

for i in range(0,nfl):
    fn1= 'article' +'-'+ str(i+1) +'.txt'
    fn2 = 'title' + '-' + str(i+1) + '.txt'
    file_path_src1=files1[i]
    file_path_src2=files2[i]
    file_path_dst1=final_outpath+ fn1
    file_path_dst2=final_outpath+ fn2
    os.rename(file_path_src1,file_path_dst1)
    os.rename(file_path_src2, file_path_dst2)


















