# Cronの設定について

平日（月〜金）、8時〜20時までの間、20分から30分及び50分から00分まで1分おきに実行

```
20-30,50-59,0 8-20 * * 1-5 /home/banpark/work/JobcanManager/jcmvenv/bin/python3 /home/banpark/work/JobcanManager/src/JobcanManager.py >> /home/banpark/work/JobcanManager/log/cron.log

```