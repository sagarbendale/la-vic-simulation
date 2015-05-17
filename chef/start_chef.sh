current_dir=$(pwd)
echo 'Enter the number of chefs'
read chefs
for i in `seq 1 $chefs`
do
	osascript -e 'tell application "Terminal" to do script "python '$current_dir'/chef.py"'
done  


