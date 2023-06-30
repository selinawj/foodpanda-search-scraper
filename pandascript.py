import json
import requests
import pandas as pd

df = pd.read_csv("Q2-files/Q2_PH_queries.csv", header=None)

items_list = []
# url_sg = "https://disco.deliveryhero.io/listing/api/v1/pandora/search?query={}&latitude=1.3117655&longitude=103.8963157&configuration=Control&customer_id=&vertical=restaurants&search_vertical=restaurants&language_id=1&opening_type=delivery&session_id=&language_code=en&customer_type=regular&limit=48&offset=0&country=sg&locale=en_SG&use_free_delivery_label=true&tag_label_metadata=true&ncr_screen=NA%3ANA&ncr_place=search%3Alist"
# url_tw = "https://disco.deliveryhero.io/listing/api/v1/pandora/search?query={}&latitude=25.02275&longitude=121.54872&configuration=Variation15&customer_id=&vertical=restaurants&search_vertical=restaurants&language_id=6&opening_type=delivery&session_id=&language_code=zh&customer_type=regular&limit=48&offset=0&country=tw&locale=zh_TW&use_free_delivery_label=false&tag_label_metadata=true&ncr_screen=NA%3ANA&ncr_place=search%3Alist"
url_ph = "https://disco.deliveryhero.io/listing/api/v1/pandora/search?query={}&latitude=14.54447&longitude=121.0459&configuration=Control&customer_id=&vertical=restaurants&search_vertical=restaurants&language_id=1&opening_type=delivery&session_id=&language_code=en&customer_type=regular&limit=48&offset=0&country=ph&locale=en_PH&use_free_delivery_label=true&tag_label_metadata=true&ncr_screen=NA%3ANA&ncr_place=search%3Alist"

query_lst = []
vendorcodes = []
vendornames = []
vendorcuisines = []
vendorimages = []
vendorurls = []
vendorfeatured = []

for index, row in df.iterrows():
    print ("now extracting row {}...".format(index))
    
    url = url_ph.format(row[0])

    resp = requests.get(
        url,
        headers={
            "x-disco-client-id": "web",
        },
    )
    if resp.status_code == 200:
        items_list = json.loads(resp.text)["data"]["items"]
        
        top_10_res = items_list[:10]
        
        for i in top_10_res:
            query = row[0]
            vendor_code = i["code"]
            vendor_name = i["name"]
            vendor_cuisines = i["cuisines"]
            vendor_char = i["characteristics"]["primary_cuisine"]

            vendor_tags_lst = []
            vendor_tags = i["tags"]
            if len(vendor_tags) == 0:
                tag = "-"
            else:
                for tags in vendor_tags:
                    if tags["origin"] == "NCR":
                        tag = "NCR"
                        vendor_tags_lst.append(tag)
                    else:
                        tag = "-"
                        vendor_tags_lst.append(tag)
            
            vendor_cuisine_lst = []
            for cuisine in vendor_cuisines:
                cuisine_name = cuisine["name"]
                vendor_cuisine_lst.append(cuisine_name)

            vendor_image = i["hero_image"]
            vendor_url = i["web_path"]

            vendorcodes.append(vendor_code)
            vendornames.append(vendor_name)
            vendorfeatured.append(vendor_tags_lst)
            
            vendorimages.append(vendor_image)
            vendorurls.append(vendor_url)
            vendorcuisines.append(vendor_cuisine_lst)

            query_lst.append(query)

output_df = pd.DataFrame({'query': query_lst, 
'vendor_codes': vendorcodes, 'vendor_names': vendornames, 'vendor_tag': vendorfeatured, 
'vendor_cuisines': vendorcuisines, 'vendor_image': vendorimages, 'vendor_urls': vendorurls})

output_df.to_csv("Q2-files/Q2_PH_queries_scraped-new.csv", index=False)
print ("output saved")