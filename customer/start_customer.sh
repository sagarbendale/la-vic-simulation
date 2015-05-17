current_dir=$(pwd)
echo 'Enter the number of customers'
read customers
for i in `seq 1 $customers`
do
	osascript -e 'tell application "Terminal" to do script "python '$current_dir'/customer.py 1 '$i'"'
done  


