list=("google.com" "fitbit.com" "ed.ac.uk" "harvard.edu" "delugerpg.com" "friv.com" "miniclip.com" "notdoppler.com" "guinnessworldrecords.com" "fearp.usp.br" "facebook.com" "instagram.com")
for varname in ${list[@]}
do
    echo $varname | tee -a $1
    traceroute -I -q1 -m40 $varname | tee -a $1
done