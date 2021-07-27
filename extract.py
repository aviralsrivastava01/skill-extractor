import re
import string
import os
import shutil
import ntpath
import textract
from collections import defaultdict

def check(filepath, skill):
    text = textract.process(filepath)
    text = str(text)
    text = text.lower()
    text = re.sub(r'\d+','',text)
    text = text.translate(str.maketrans('','',string.punctuation))
    return True if skill in text else False


if __name__ == "__main__":
    dir, _, files = next(os.walk('resumes'))
    files = [x for x in files if x.lower().endswith('pdf')]
    files = list(map(lambda x: os.path.join(dir, x), files))
    skills = ['sql','nodejs','flask','python']

    for skill in skills:
        skilldir = os.path.join(os.getcwd(), skill)
        try:
            os.stat(skilldir)
        except:
            os.mkdir(skilldir)
    
    stats = defaultdict(list)

    for file in files:
        basename = ntpath.basename(file)
        if len(basename.split()) > 1:
            newfile = os.path.join('resumes', '-'.join(basename.split()))
            oldfile = file
            file = newfile
            shutil.move(oldfile, file)

        for skill in skills:
            if check(file, skill.lower()):
                stats[skill].append(basename)
                # print('{} present {}'.format(skill, file))
                shutil.copy(file, os.path.join(skill, basename))
    
    print(stats)