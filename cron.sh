#!/usr/bin/env bash

#stores=(amazon jabong flipkart shopclues babyoye bewakoof yepme zansaar koovs zivame fashionara fabfurnish snapdeal trendin pepperfry);

stores=(amazon jabong flipkart shopclues yepme koovs zivame fashionara snapdeal);

echo "Check Started" > /home/ubuntu/priceAccQA/cronRun.log 2>&1

for i in "${stores[@]}"
do
    echo $i >> /home/ubuntu/priceAccQA/cronRun.log 2>&1
    nohup python /home/ubuntu/priceAccQA/Check.py $i >> /home/ubuntu/priceAccQA/cronRun.log 2>&1
done

nohup python /home/ubuntu/priceAccQA/sendMail.py &
