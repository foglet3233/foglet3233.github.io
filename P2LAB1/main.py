# Tristan Fogle
# 10/13/2024
# P2HW1
# Program that calculates price for items with sales tax included
# use 6.75% sales tax rate as a decimal
sales_tax_rate = 0.0675
# get input for the items and prices with the price per item being a float because it could be a decimal, and the quanitity being an int 
because it wont be a decimal
item_name = input("What are you buying? ")
quantity = int(input("How many do you want? "))
price_per_item = float(input("What's the price per item? "))
# calculate price
subtotal = quantity * price_per_item
# calculate sales price
sales_tax = subtotal * sales_tax_rate
# add the sales tax so u get the total price
total_price = subtotal + sales_tax
# print recipt using f string and modifiers like .2f to prevent long decimals since we are dealing with money. spent a good minute figuring 
out how to round it only to find out that .2f rounds automatically so thats cool
print("\n--- Receipt ---")
print(f"Item: {item_name}")
print(f"Quantity: {quantity}")
print(f"Price per item: ${price_per_item:.2f}")
print(f"Subtotal: ${subtotal:.2f}")
print(f"Sales tax (6.75%): ${sales_tax:.2f}")
print(f"Total price: ${total_price:.2f}")
