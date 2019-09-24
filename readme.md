# Notable to BoostNote Converter
Used to transform notable notes into boostNote documents that are simplied dropped into boostNote's directory. Alll notable attributes will be transferred to the new document.

# Usage



```
#!/bin/bash

targ=~/Boostnote/notes


source ~/Develop/notableConv/venv/bin/activate
for elem in ~/notes/notes/*.md
do 
  if grep -il 'Daily Log' "$elem"
  then 
     python ~/Develop/notableConv/notableConver.py --key 4572a60964f147c6f534 --target $targ < "$elem"
  else
     python ~/Develop/notableConv/notableConver.py --key 65aaa9202309153835ea --target $targ < "$elem"
  fi
done
```
