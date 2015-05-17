current_dir=$(pwd)
echo 'Enter the number of cashiers'
read cashier
for i in `seq 1 $cashier`
do
	osascript -e 'tell application "Terminal" to do script "python '$current_dir'/cashier.py"'
done  


