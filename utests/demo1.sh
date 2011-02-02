#!/bin/bash
echo "Welcome to VADpy 2.0 demostration"
echo 
echo 
echo "Please make sure that you have VADpy environment configured."
echo "It's probably ready, if you're on cs3 server."

echo "Are you ready to start (y/n)?";
read -n 1 -s REPLY
[ "$REPLY" == "n" ] && exit 0

clear
echo "VADpy is a program with modular architecture."
echo "The main task of the core is to provide a unified data-transfer interface to modules." 
read -s -p "[Next >>]"

clear
echo "VADpy's execution idea is very close to 'shell pipelines'. For example:"
echo "vad.py ! nist05 ! info # Press [Enter] to execute"
read -s
./vad.py ! nist05 ! info | less
echo
echo "You've just seen the information about elements inside the pipeline"
read -s -p "[Next >>]"

clear
echo "Let's try parsing the GT of NIST-05 corpus:"
echo "vad.py ! nist05 ! inist ! info # Press [Enter] to execute"
read -s
./vad.py ! nist05 ! inist ! info | less
echo 
echo "Have you noticed that every Element has a gt_labels attribute filled?"
echo "If not, pay attention on next step!"
read -s -p "[Next >>]"

clear
echo "The next goal is to execute a VAD and parse it's output."
echo "vad.py ! nist05 ! amr1 ! inist ! iamr ! info # Press [Enter] to execute"
./vad.py ! nist05 ! amr1 ! inist ! iamr ! info | less


clear
echo "The next goal is to execute a VAD and parse it's output:"
echo "vad.py ! nist05 ! amr1 ! inist ! iamr ! info # Press [Enter] to execute"
read -s
./vad.py ! nist05 ! amr1 ! inist ! iamr ! info | less
echo 
echo "I believe you've noticed Labels objects this time :)"
echo "Now, every element posesses both original GT and VAD output labels."
echo "Also, you should have noticed, that AMR worked much faster this time."
echo "A VAD doesn't overwrite existsting output files unless it is explicitly required by user." 
read -s -p "[Next >>]"

clear
echo "At last, we're going to do something useful."
echo "vad.py -q ! nist05 ! amr1 ! inist ! iamr ! confusion # Press [Enter] to execute"
read 
./vad.py ! nist05 ! amr1 ! inist ! iamr ! confusion
echo "Just in case: FRR is False Request Rate and FAR is False Acceptance Rate."
echo "These values are based on comparison of corpus' GT and VAD's output."
echo "Please write them down. We'll need them for the next step."
read -s -p "[Next >>]"

clear
echo "Let's change the VAD to AMR2 and enable debug output (-d option)"
echo "vad.py -d ! nist05 ! amr2 ! inist ! iamr ! confusion # Press [Enter] to execute"
read -s 
./vad.py -d ! nist05 ! amr2 ! inist ! iamr ! confusion
echo "Do the FRR and FAR of AMR1 and AMR2 results differ much? How do you think, which VAD is better?"
read -s -p "[Next >>]"

clear 
echo "Even though logging looks horrible, it is recommended to have hat option turned on."
echo "Note that logging goes to stderr. Modules (e.g. info, confusion) print their output to stdout."
echo 
echo "This means, you can redirect the output to a file:"
echo "vad.py ! nist05 ! amr2 ! inist ! iamr ! confusion > amr2_nist_frr_far.txt # Press [Enter] to execute"
read -s 
./vad.py ! nist05 ! amr2 ! inist ! iamr ! confusion > amr2_nist_frr_far.txt
read -s -p "[Next >>]"

clear 
echo "Even though the log might look horrible, it is recommended to have debug option turned on."
echo "Note that logging goes to stderr. Modules (e.g. info, confusion) print their output to stdout."
echo 
echo "This means, you can redirect the output to a file:"
echo "vad.py ! nist05 ! amr2 ! inist ! iamr ! confusion > amr2_nist_frr_far.txt # Press [Enter] to execute"
read -s 
./vad.py ! nist05 ! amr2 ! inist ! iamr ! confusion > amr2_nist_frr_far.txt
echo "You can check that file later :)"
read -s -p "[Next >>]"
