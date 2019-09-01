#!/bin/bash
if [[ `whoami` != root ]];
then
    echo Please run this script as root or using sudo
    exit 1
fi

if [[ $(basename `pwd`) != "gistconfs" ]]
then
  printf "You need to be located at the gistconfs directory.\nPlease re-run this script in a proper directory.\n"
  exit 1
fi

PACKAGES=(python3)
for i in ${PACKAGES[@]}
do
  dpkg -l $i 1>/dev/null 2>&1
  if [[ $? -eq 1 ]]
  then
    sudo apt install $i -y
  fi
done

MODULES=(requests sys datetime time random zlib)
for i in ${MODULES[@]}
do
  python3 -c "import $i" 2>/dev/null
  if [[ $? -eq 1 ]]
  then
    pip3 install $i
  fi
done

if [[ ! -f "./jlav.py" ]]
then
  wget -q https://gist.githubusercontent.com/LordShedy/b24831be673bd3a176442f3eded8c116/raw/9dfd4a70979af4258962a3d257804194a0ed3c9b/jlav.py
  printf "jlav.py was downloaded and stored at `pwd`.jlav\n"
fi

if [[ -f "./automated_configs.cron" ]]
then
  cp ./automated_configs.cron /etc/cron.d/automated_configs
  printf "a cron file automated_configs was created in /etc/cron.d/\n"
fi
printf "all prerequesities downloaded and installed\n"
exit 0
