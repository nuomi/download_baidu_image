#!/usr/bin/env python

import json, requests
import chardet
import os

api_list_album='http://image.baidu.com/channel/albums?t=album&s=2&pn=0&rn=5&acn=4&c=' #+category name
api_list_album_by_user='http://image.baidu.com/albumlist/'  #+userid
api_list_images='http://image.baidu.com/picturelist/getpicture?offset=0&size=1000&album_id=' #131427486&from=0&user_id=119622647&format=json'
test_c='%E7%BE%8E%E5%A5%B3'
working_dir='./images/'

def list_album(category):
    try:
        print 'list_album downloading...' 
        r = requests.get(api_list_album+category, stream=True)

        if int(r.status_code) == 200:
            r.encoding = 'utf-8'
            return r.text
        else:
            print r.status_code
    except:
        print 'requests error'

def list_images(album_id, user_id):
    try:
        print 'list_images downloading ...'
        print api_list_images+album_id+'&from=0&user_id='+user_id+'&format=json'
        r = requests.get(api_list_images+album_id+'&from=0&user_id='+user_id+'&format=json')

        if int(r.status_code) == 200:
            return r.json()['data']['picture_list']
        else:
            print r.status_code
    except:
        print 'request error'

   
def update(category):
    all_album = json.loads(list_album(category))
    albums = all_album['albums'][:int(all_album['returnNumber'])]
    new_albums = []
    i = 1
    for album in albums:
        picture_list = list_images(album['id'], album['userId'])
        album['picture_list'] = picture_list
        new_albums.append(album)
        print i
        i+=1

    all_album['albums'] = new_albums

    with open('albums.json', 'w') as f:
        f.write(json.dumps(all_album))

def export():
    with open('albums.json') as f:
        albums = json.loads(f.read()) 

    for album in albums['albums']:
        pwd = working_dir+album['title']
        try:
            os.mkdir(pwd.encode('utf-8'))
        except:
            pass
        for image in album['picture_list']:
            #print json.dumps(image)
            filename = image['picture_name']
            if filename[-3:] != 'jpg': 
                filename = filename+'.jpg'
            with open(pwd +'/'+filename, 'w') as f:
                try:
                    f.write(requests.get(image['download_url'], stream=True).raw.read())    
                except:
                    pass

if __name__ == '__main__':
    #update(test_c)
    export()

