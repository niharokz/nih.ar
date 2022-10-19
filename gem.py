#!/bin/python3

#
#       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
#       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
#       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
#       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
#       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
#       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
#       DRAFTED BY [https://nihars.com] ON 20-06-2021.
#       SOURCE [gem.py] LAST MODIFIED ON 07-07-2021.
#

from yaml import safe_load
from os import path,makedirs
from glob import glob


try:
    def create_log(post_detail,md,note):
        logfile = "#"+post_detail.get("title")+'\n'
        logfile += "#"+post_detail.get("subtitle")+'\n'
        logfile += "> Last Modified on "+post_detail.get("date").strftime('%d %b %Y')+'\n'
        logfile += md +'\n'
        logfile += "=> / home"
        post_data = note.split('/')
        post_path = path.join("gem","log")
        post_file = post_data[2].replace('.md','.gmi')
        makedirs(post_path,exist_ok=True)
        with open(path.join(post_path,post_file),'w') as output_file:
            output_file.write(logfile)
        return post_file
    
    with open('config.yml') as conf:
        config = safe_load(conf.read())
        for key,val in config.items():
            globals()[key] = val

    logs = []
    for note in glob(path.join(content_path,"note","*.md")):
        yaml_lines, ym, md = [],'',''
        with open(note) as infile:
            for s in infile:
                if s.startswith('---'):
                    for s in infile:
                        if s.startswith('---'):
                            break;
                        else:
                            yaml_lines.append(s)
                    ym = ''.join(yaml_lines)
                    md = ''.join(infile)
                    break;
        post_detail=safe_load(ym)
        if (post_detail is not None) and ((post_detail.get("showInHome") is None) or post_detail.get("showInHome") ):
            post_url = create_log(post_detail,md,note)
            ymd = post_detail
            ymd.update({'url' : '/'+post_url})
            logs += [ymd]
    
    logs= sorted(logs, key=lambda post :  post['date'], reverse=True)

    logFile="# nihar's page on gemini\n\nNamaste! I'm Nihar, a hobbyist systems programmer from India.\n\n## Log\n"
    for log in logs:
        logFile += "=> /log/"+log.get("url")+" "
        logFile += log.get("date").strftime('%d %b %Y')+" - "+log.get("title")+"\n"

    logFile+="\n## Places to get me: \n=> https://nihars.com Website\n=> mailto:hi@nihars.com Email nihar (hi@nihars.com)\n"
    logFile+="=> https://codeberg.org/niharokz My Git\n=> https://fosstodon.org/@nihar Mastodon\n=> https://nihars.com/rss.xml RSS articles"
    logFile+="=> https://nihars.com/public-key.txt pgpkey"

    with open(path.join("gem","index.gmi"),'w') as output_file:
        output_file.write(logFile)
        
except:
    print("Gem creation failed")


