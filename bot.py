import time
import random
import threading

# Set the betting amount
bet_amount = 1

# Set the profit threshold (in percentage)
profit_threshold = 20

# Set the number of accounts to manage
num_accounts = 1

# Create a list of accounts
accounts = []
for i in range(num_accounts):
  accounts.append({
    "username": "username{}".format(i),
    "password": "password{}".format(i),
    "balance": 100
  })

# Create a function to place a bet
def place_bet(account):
  # Send a request to the Aviator game to place a bet
  response = requests.post("https://demo.spribe.io/launch/aviator?currency=GHS&lang=EN&return_url=https://www.msport.com/gh/games", headers=headers, data={"bet_amount": bet_amount})

  # Check if the request was successful
  if response.status_code == 200:
    # The request was successful. Get the game data.
    game_data = response.json()

    # Get the bet ID
    bet_id = game_data["bet_id"]

    # Add the bet to the account's list of bets
    account["bets"].append(bet_id)
  else:
    # The request was not successful. Print the error message.
    print("Error placing bet:", response.text)

# Create a function to cash out a bet
def cash_out_bet(account, bet_id):
  # Send a request to the Aviator game to cash out a bet
  response = requests.post("https://demo.spribe.io/launch/aviator?currency=GHS&lang=EN&return_url=https://www.msport.com/gh/games", headers=headers, data={"bet_id": bet_id, "cashout": True})

  # Check if the request was successful
  if response.status_code == 200:
    # The request was successful. Get the winnings.
    winnings = response.json()["winnings"]

    # Add the winnings to the account's balance
    account["balance"] += winnings
  else:
    # The request was not successful. Print the error message.
    print("Error cashing out bet:", response.text)

# Create a function to manage multiple accounts
def manage_accounts():
  # Create a thread for each account
  threads = []
  for account in accounts:
    thread = threading.Thread(target=play_game, args=(account,))
    threads.append(thread)

  # Start all of the threads
  for thread in threads:
    thread.start()

  # Join all of the threads
  for thread in threads:
    thread.join()

# Create a function to track winnings and losses
def track_winnings_and_losses():
  # Initialize the variables
  total_winnings = 0
  total_losses = 0

  # Loop through all of the accounts
  for account in accounts:
    # Loop through all of the bets in the account
    for bet in account["bets"]:
      # Check if the bet was a win or a loss
      if bet["status"] == "win":
        total_winnings += bet["winnings"]
      else:
        total_losses += bet["losses"]

  # Print the total winnings and losses
  print("Total winnings:", total_winnings)
  print("Total losses:", total_losses)

# Create a function to play the game
def play_game(account):
  # Loop forever
  while True:
    # Place a bet
    place_bet(account)

    # Wait for the plane to reach the cashout threshold
    while True:
      # Get the current plane's altitude
      response = requests.get("https://demo.spribe.io/launch/aviator?currency=GHS&lang=EN&return_url=https://www.msport.com/gh/games")

      # Check if the request was successful
      if response.status_code == 200:
        # The request was successful. Get the game data.
        game_data = response.json()

        # Get the current plane's altitude
        altitude = game_data["altitude"]

        # Check if the current plane's altitude is greater than the cashout threshold
        if altitude > bet_amount * (1 + profit_threshold / 100):
          # The current plane's altitude is greater than the cashout threshold. Cash out the bet.
          cash_out_bet(account, bet_id)
          break
      else:
        # The request was not successful. Print the error message.
        print("Error getting game data:", response.text)

# Start the game
manage_accounts