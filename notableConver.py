import sys
import hashlib
import random
import argparse
import string
import os


def extract_data_element(target, target_list):
    ret = None
    for elem in target_list:
        if elem.startswith(target):
            return elem.partition(':')[2]
    return ret

def sringlist_to_list(list_string):
    result = list_string.replace(']', '')
    result = result.replace('[', '')
    result = result.replace("'", '')
    return result.split(',')

def generate_filename():
    cats = string.ascii_lowercase
    filename = ''.join(random.choice(cats) for i in range(32))

    x = hashlib.md5(filename.encode()).hexdigest()
    s = '%s-%s-%s-%s-%s.cson' % (x[:8], x[8:12], x[12:16], x[16:20], x[20:])
    return s

def create_boostnote(data, folder_id):
    bounding_range = [cnt for cnt, elem in enumerate(data) if '---' in elem.rstrip('\n')]
    meta_data = [elem.rstrip('\n') for cnt, elem in enumerate(data) if cnt > bounding_range[0] and cnt < bounding_range[1]]
    post_data = [elem for cnt, elem in enumerate(data) if cnt >= bounding_range[1]]

    title = extract_data_element('title', meta_data)
    created = extract_data_element('created', meta_data).replace("'", '')
    modified = extract_data_element('modified', meta_data).replace("'", '')
    tag_list = extract_data_element('tags', meta_data)
    favorite = extract_data_element('favorited', meta_data)
    pinned = extract_data_element('pinned', meta_data)

    # turn it into an array so I can sort it
    tags = sringlist_to_list(tag_list)
    tags.sort()

    ntags = [ f'"{elem.strip()}"' for elem in tags]
    if len(tags) > 1:
        ntags_result = ",".join(ntags)
    else:
        ntags_result = "".join(ntags)
    ntags_result = f'[{ntags_result}]'

    header = [f'createdAt: "{created.strip()}"',
              f'updatedAt: "{modified.strip()}"',
              f'type: "MARKDOWN_NOTE"',
              f'folder: "{folder_id}"',
              f'title: "{title.strip()}"',
              f'tags: {ntags_result}'
              ]

    if (favorite):
        header.append(f'isStarred: "true"')
    if (pinned):
        header.append(f'isPinned: "true"')
    header.append(f"content:'''\n")
    pp = ''.join(post_data)
    header.append(f"{pp}'''\n")
    return '\n'.join(header)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Notable converter to BoostNote")
    parser.add_argument("--key",
                        action="store",
                        metavar="folder_key",
                        help="Folder key used by BoostNote folders")
    parser.add_argument("--target",
                        action="store",
                        metavar='target_directory',
                        help="Directory that BoostNote.json file resides")

    parser_args = parser.parse_args()

    data = sys.stdin.readlines()
    header = create_boostnote(data, parser_args.key)




    try:
        os.chdir(parser_args.target)
        fileName = generate_filename()
        # open file and stuff contents
        with open(fileName, 'w') as f:
            f.write(header)
            f.close()
    except os.error:
        print(F'{parser_args.target} directory cannot be found')
