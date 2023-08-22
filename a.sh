list=("google.com" "youtube.com" "fitbit.com" "socratic.com" "keio.ac.jp" "ed.ac.uk" "harvard.edu" "delugerpg.com" "friv.com" "kongregate.com" "miniclip.com" "notdoppler.com" "guinnessworldrecords.com" "fearp.usp.br" "uj.ac.za" "canberra.edu.au" "facebook.com" "instagram.com" "threads.net" "web.whatsapp.com")
for varname in ${list[@]}
do
    echo $varname | tee -a c.txt
    traceroute -I -q1 -m40 $varname | tee -a c.txt
done