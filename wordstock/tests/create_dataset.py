import os
import urllib.request

if not os.path.exists('data'):
    os.mkdir('data')

urllib.request.urlretrieve(
    'http://www.gutenberg.org/cache/epub/2243/pg2243.txt',
    'data/merchant_of_venice.txt')
urllib.request.urlretrieve(
    'http://www.gutenberg.org/cache/epub/2244/pg2244.txt',
    'data/as_you_like_it.txt')
urllib.request.urlretrieve(
    'http://www.gutenberg.org/cache/epub/2245/pg2245.txt',
    'data/taming_of_the_shrew.txt')
urllib.request.urlretrieve(
    'http://www.gutenberg.org/cache/epub/2246/pg2246.txt',
    'data/all_is_well_that_ends_well.txt')
urllib.request.urlretrieve(
    'http://www.gutenberg.org/cache/epub/2247/pg2247.txt',
    'data/twelve_night_or_what_you_will.txt')
urllib.request.urlretrieve(
    'http://www.gutenberg.org/cache/epub/2248/pg2248.txt',
    'data/the_winters_tale.txt')

filecount = 0
while filecount < 100:
    filecount = filecount + 1
    index = str(2243 + filecount)
    url_name = 'http://www.gutenberg.org/cache/epub/'+index+'/pg'+index+'.txt'
    local_file_name = 'data/file' + index + '.txt'
    print("Downloading URL: " + url_name)
    try:
        urllib.request.urlretrieve(url_name, local_file_name)
    except urllib.error.HTTPError as e:
        print("Failed to download url")
        print("Continuing further...")
        continue
