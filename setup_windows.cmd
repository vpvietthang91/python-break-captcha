@echo off
setlocal enabledelayedexpansion
echo "creating data\raw"
mkdir data\raw
echo "creating data/segmented"
mkdir data\segmented
mkdir data\segmented\uppercase
mkdir data\segmented\lowercase
echo "creating data/models"
mkdir data\models
echo "creating data/results"
mkdir data\results
echo "creating data/test"
mkdir data\test
for %%i in (A B C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
	echo "creating data\segmented\uppercase\%%i"
	if not exist data\segmented\uppercase\%%i mkdir data\segmented\uppercase\%%i
)
for %%i in (a b c d e f g h i j k l m n o p q r s t u v w x y z) do (
	echo "creating data\segmented\lowercase\%%i"
	if not exist data\segmented\lowercase\%%i mkdir data\segmented\lowercase\%%i
)
for %%i in (0 1 2 3 4 5 6 7 8 9) do (
	echo "creating data\segmented\%%i"
	if not exist data\segmented\%%i mkdir data\segmented\%%i
)
pause