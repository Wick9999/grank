from utils.logger import log
from json import load

def buy(Client, item: str, cwd: str) -> None:
	Client.send_message(f"pls buy {item}")
	
	latest_message = Client.retreive_message(f"pls buy {item}")

	if latest_message is None:
		return
		
	if latest_message["content"] in ["your wallet is short on cash, go withdraw some BANK money to make this purchase", "Far out, you don't have enough money in your wallet or your bank to buy that much!!"]:
		from scripts.balance import balance
		bal = balance(Client)
		
		if bal is not None:  
			data = load(open(f"{cwd}database.json", "r"))
			latest_message = Client.retreive_message("pls bal")
   
			bank = int("".join(filter(str.isdigit, latest_message["embeds"][0]["description"].split("\n")[1].split("/")[0].strip())))
			wallet = int("".join(filter(str.isdigit, latest_message["embeds"][0]["description"].split("\n")[0])))
			
			if (wallet + bank) - data["price"][f"{item}"] > 0:
				amount = (wallet + bank) - data["price"][f"{item}"]
				
				Client.send_message(f"pls with {amount}")                                
				Client.send_message(f"pls buy {item}")
			elif Client.config["logging"]["warning"]:
				log(Client.username, "WARNING", f"Insufficient funds to buy a {item}.")  
	elif latest_message["embeds"][0]["author"]["name"].lower() == f"successful {item} purchase":
		if Client.config["logging"]["debug"]:
			log(Client.username, "DEBUG", f"Successfully bought {item}.")