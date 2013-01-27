#!/bin/bash

logspath="/home/roux/.purple/logs/irc"
echo 'id;user;"tweet";url' > tweets-acta.csv
grep -i "ungarage.*#acta.*twitter.*/status" $logspath/*@irc.freenode.net/#laquadrature.chat/* | 
    sed 's/^.*) ungarage:\s\+//i' | 
    sed 's/^\s*\(\S*\)\s*:\s\+//' | 
    sed 's# - \(http://\S\+\)\s*$#";\1#i' | 
    while read l; do
        id=`printf "%018d" $(echo "$l" | sed 's#^.*statuse\?s\?/\(.*\)$#\1#')`;
        user=`echo "$l" | sed 's#^.*\.com/\(\S\+\)/status.*$#\1#'`;
        echo "$id;$user;\"$l";
    done |
    sort | uniq >> tweets-acta.csv

echo 'tweets;user' > tweets-acta-users.stats
awk -F ";" '{print $2}' tweets-acta.csv |
    sed 's/^\(.*\)$/\L\1/' |
    sort | uniq -c |
    while read l; do
        n=`printf "%04d" $(echo $l | sed 's/\S\+$//')`;
        echo $l | sed 's/^[0-9]*/'$n'/';
    done |
    sort -r >> tweets-acta-users.stats

