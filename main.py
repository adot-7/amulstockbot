import subprocess
import json
from twilio.rest import Client
from dotenv import load_dotenv
import os

curl_command = [
    "curl",
    "--location",
    "--globoff",
    "https://shop.amul.com/api/1/entity/ms.products?fields[name]=1&fields[brand]=1&fields[categories]=1&fields[collections]=1&fields[alias]=1&fields[sku]=1&fields[price]=1&fields[compare_price]=1&fields[original_price]=1&fields[images]=1&fields[metafields]=1&fields[discounts]=1&fields[catalog_only]=1&fields[is_catalog]=1&fields[seller]=1&fields[available]=1&fields[inventory_quantity]=1&fields[net_quantity]=1&fields[num_reviews]=1&fields[avg_rating]=1&fields[inventory_low_stock_quantity]=1&fields[inventory_allow_out_of_stock]=1&fields[default_variant]=1&fields[variants]=1&fields[lp_seller_ids]=1&filters[0][field]=categories&filters[0][value][0]=protein&filters[0][operator]=in&filters[0][original]=1&facets=true&facetgroup=default_category_facet&limit=32&total=1&start=0&cdc=1m&substore=66505ff5145c16635e6cc74d"
    #blr url in case del down: "https://shop.amul.com/api/1/entity/ms.products?fields[name]=1&fields[brand]=1&fields[categories]=1&fields[collections]=1&fields[alias]=1&fields[sku]=1&fields[price]=1&fields[compare_price]=1&fields[original_price]=1&fields[images]=1&fields[metafields]=1&fields[discounts]=1&fields[catalog_only]=1&fields[is_catalog]=1&fields[seller]=1&fields[available]=1&fields[inventory_quantity]=1&fields[net_quantity]=1&fields[num_reviews]=1&fields[avg_rating]=1&fields[inventory_low_stock_quantity]=1&fields[inventory_allow_out_of_stock]=1&fields[default_variant]=1&fields[variants]=1&fields[lp_seller_ids]=1&filters[0][field]=categories&filters[0][value][0]=protein&filters[0][operator]=in&filters[0][original]=1&facets=true&facetgroup=default_category_facet&limit=24&total=1&start=0&cdc=1m&substore=66505ff0998183e1b1935c75"
    #del url: "https://shop.amul.com/api/1/entity/ms.products?fields[name]=1&fields[brand]=1&fields[categories]=1&fields[collections]=1&fields[alias]=1&fields[sku]=1&fields[price]=1&fields[compare_price]=1&fields[original_price]=1&fields[images]=1&fields[metafields]=1&fields[discounts]=1&fields[catalog_only]=1&fields[is_catalog]=1&fields[seller]=1&fields[available]=1&fields[inventory_quantity]=1&fields[net_quantity]=1&fields[num_reviews]=1&fields[avg_rating]=1&fields[inventory_low_stock_quantity]=1&fields[inventory_allow_out_of_stock]=1&fields[default_variant]=1&fields[variants]=1&fields[lp_seller_ids]=1&filters[0][field]=categories&filters[0][value][0]=protein&filters[0][operator]=in&filters[0][original]=1&facets=true&facetgroup=default_category_facet&limit=32&total=1&start=0&cdc=1m&substore=66505ff5145c16635e6cc74d"
]

# Run curl and capture output
result = subprocess.run(curl_command, capture_output=True, text=True)

print(result.returncode, result.stderr, result.stdout)

# Convert output to JSON
data = json.loads(result.stdout)['data']
interested = [i for i in data if "lassi" in i.get('alias')] #Gives list of dicts List[Dict]: [{'alias':'', 'q':}, {}]
quantities = [{'quantity': i.get('inventory_quantity'), 'item': ' '.join(i.get('alias').title().split('-')[3:5])} for i in interested]
print(quantities)

load_dotenv()
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
client = Client(account_sid, auth_token)


for quantity in quantities:
    instock = True
    if instock:
        first = f"Amul's {quantity.get('item')}"
        second = f"{quantity.get('quantity')}"
        message = client.messages.create(
            from_=f'whatsapp:{os.getenv("TWILIO_PHONE")}',
            # body=f"The Amul {quantity.get('item')} is in stock! Buy quickly at shop.amul.com",
            content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
            content_variables='{{"1":"{d}", "2":"{t}"}}'.format(d=first, t=second),
            to=f'whatsapp:{os.getenv("MY_PHONE")}'
        )
        print(f"Message Sent for {quantity.get('item')}.")

#Need a better implementation for running the script cause if the stock stays above 100 for more than one hour and we have already got the notification then it gets annoying. 
    

