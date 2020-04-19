#!/bin/bash
MODEL_LIST="mobilenet resnet mobilenet mlp"
BATCHSIZE_LIST="32 50 64 100 128"
TRAINSET_LIST="imagenet cifar10 mnist"
REPEAT=5
FOLDER="exp-results"

echo ${REPEAT}
for midx in ${MODEL_LIST}
do
  for bidx in ${BATCHSIZE_LIST}
  do
    for tidx in ${TRAINSET_LIST}
    do
      CASE=${midx}_${bidx}_${tidx}  
      for i in $(seq 1 ${REPEAT}) 
      do 
        echo "########################################" >> ./${FOLDER}/${CASE}.txt
        echo "================EXP ${i}================" >> ./${FOLDER}/${CASE}.txt
        echo "########################################" >> ./${FOLDER}/${CASE}.txt
        python3 single_train_profiler.py -m ${midx} -b ${bidx} -d ${tidx} >> ./${FOLDER}/${CASE}.txt
      done
      LEN=0
      SUM=0
      while read -r line
      do
        if [[ $line =~ ^"average step time:" ]]
        then
          AST=${line#*"average step time: "}
          LEN=$((${LEN}+1))
          SUM=$(echo "${SUM} + ${AST}" | bc)
        fi
      done < ./${FOLDER}/${CASE}.txt
      echo "================EXP: ${midx}-${bidx}-${tidx} ================" >> ./${FOLDER}/all-results.txt
      echo AVG=$(echo "scale=3; ${SUM}/${LEN}" | bc) >> ./${FOLDER}/all-results.txt
    done          
  done
done
