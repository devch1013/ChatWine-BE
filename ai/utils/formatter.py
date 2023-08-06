from wine.models import WineData, WineBar
import json


def wine_data_formatter(wine_ids: list, wine_bar: bool = False):
    formatted_list = list()
    for id in wine_ids:
        print("wine_id: ", id)
        try:
            data_dict = dict()
            if wine_bar:
                wine_bar_data = WineBar.objects.get(id=id)
                data_dict["name"] = wine_bar_data.name
                data_dict["address"] = wine_bar_data.address
                data_dict["rating"] = str(wine_bar_data.rating)
                data_dict["img_url"] = wine_bar_data.img_url
                data_dict["summary"] = wine_bar_data.summary
                data_dict["url"] = wine_bar_data.url
                formatted_list.append(data_dict)
            else:
                wine_data = WineData.objects.get(id=id)
                data_dict["ko_title"] = wine_data.kr_name
                data_dict["en_title"] = wine_data.en_name
                data_dict["image"] = wine_data.img_url
                data_dict["description"] = wine_data.flavor_description
                data_dict["price"] = str(wine_data.price)
                data_dict["url"] = wine_data.url
                formatted_list.append(data_dict)

        except:
            print("id not found!")
    formatted_text = json.dumps(formatted_list, ensure_ascii=False)
    return formatted_text
