
Dependencies
-------------
Project requires below framework installed on system

- Python 2.7+
- Pyro4
- colorama


How to Run the simulation - Distributed
----------------------------------------


1) Run lavic Environment Processes on a Node
execute below commands from project base directory.
cd lavic_environment
sh setup_env.sh

2) Run lavic Cashier/Cahsiers Processes on a Node
execute below commands from project base directory.
cd cashier
sh start_cashier.sh

3) Run lavic Chef/Chefs Processes on a Node
execute below commands from project base directory.
cd chef
sh start_chef.sh


4) Run lavic Server/Servers Processes on a Node
execute below commands from project base directory.
cd server
sh start_server.sh


5) Run lavic Customer/Customers Processes on a Node
execute below commands from project base directory.
cd customer
sh start_customer.sh
