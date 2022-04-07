#!bin/bash
echo "creating data/raw"
mkdir -p data/raw
echo "creating data/segmented"
mkdir -p data/segmented
echo "creating data/models"
mkdir -p data/models
echo "creating data/results"
mkdir -p data/results
echo "creating data/test"
mkdir -p data/test
for alphabet in {a..z}; do
  echo "creating data/segmented/${alphabet}"
  mkdir -p data/segmented/$alphabet
done
for number in {0..9}; do
  echo "creating data/segmented/${number}"
  mkdir -p data/segmented/${number}
done
