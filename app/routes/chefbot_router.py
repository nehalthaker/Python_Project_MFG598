import os
import pandas as pd
from fastapi import APIRouter
from fastapi.responses import FileResponse, StreamingResponse
import matplotlib.pyplot as plt
from io import BytesIO

router = APIRouter()
csv_file = r"C:\Users\nehpa\Documents\Python project\megamind_api\app\utils\Modified_Indian_Food_Dataset.csv"
markdown_file_path = r"C:\Users\nehpa\Documents\Python project\megamind_api\app\recipes"


@router.get("/chefbot/get_dishes", tags=["chefbot"])
def fetch_the_menu(dish: str = None):
    """Search for your favourite dish to make!

    Args:
        dish: Name of the dish. Eg: salad, pizza, pasta, sandwich, upma, idli.

    Returns:
        Dictionary of dishes.
    """
    count = 1
    dish_dictionary = {}
    df = pd.read_csv(csv_file)
    df = df.sort_values(by=["TotalTimeInMins"])
    for dishes in df["TranslatedRecipeName"]:
        if dish.title() in dishes:
            dish_dictionary[count] = []
            dish_dictionary[count].append(dishes)
            count += 1

    if len(dish_dictionary) > 0:
        return dish_dictionary
    else:
        return {404: "Sorry, we don't have what you are looking for!"}


@router.get("/chefbot/pie_chart", tags = ["chefbot"])
def pie_chart(dish: str):
    df = pd.read_csv(csv_file)
    df = df.sort_values(by=["TotalTimeInMins"])
    result = df[df["TranslatedRecipeName"].str.contains(dish.title())]
    dish_dictionary = {}
    for i in result.index:
        dish_dictionary[result["TranslatedRecipeName"][i]] = result["TotalTimeInMins"][i]
    labels = list(dish_dictionary.keys())
    values = list(dish_dictionary.values())

    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct=lambda pct: str(int(pct * sum(values) / 100)) + " Minutes", startangle=90)
    ax1.axis('equal')

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")


@router.post("/chefbot/fetch_recipe", tags=["chefbot"])
def fetch_recipe(dish: str, index_number: int):
    """Return the recipe for the dish enterred.

    Args:
        dish : Name of the dish. Eg: salad, pizza, pasta, sandwich, upma, idli.
        index_number : Index number for the dish.

    Returns:
        Recipe for the dish.
    """
    count = 1
    dish_dictionary = {}
    df = pd.read_csv(csv_file)
    df = df.sort_values(by=["TotalTimeInMins"])
    for dishes in df["TranslatedRecipeName"]:
        if dish.title() in dishes:
            dish_dictionary[count] = []
            dish_dictionary[count].append(dishes)
            count += 1
    if len(dish_dictionary) > 0 and index_number in dish_dictionary.keys():
        chosen_dish = dish_dictionary[int(index_number)][0]
        df_new = df[df["TranslatedRecipeName"] == chosen_dish]
        index = df_new.index[0]
        dictionary = df_new.to_dict()
        if os.path.isfile(f"{markdown_file_path}/{chosen_dish}.md"):
            return FileResponse(rf"{markdown_file_path}/{chosen_dish}.md")
        else:
            with open(
                rf"{markdown_file_path}/{chosen_dish}.md",
                "w",
            ) as file:
                file.write(
                    f"""# {chosen_dish}\n\n## Cooking time: {dictionary['TotalTimeInMins'][index]} minutes.\n\n## Ingredients:\n{dictionary['Cleaned-Ingredients'][index]}\n\n## Cooking Instructions:\n{dictionary['TranslatedInstructions'][index]}"""
                )
            return FileResponse(rf"{markdown_file_path}/{chosen_dish}.md")
    else:
        return {404: "Sorry, we don't have what you are looking for!"}


@router.post("/chefbot/download_recipe", tags=["chefbot"])
def dish_maker(dish: str, index_number: int):
    """Download the recipe for the dish enterred.

    Args:
        dish : Name of the dish. Eg: salad, pizza, pasta, sandwich, upma, idli.
        index_number : Index number for the dish.

    Returns:
        Download file for the recipe.
    """
    count = 1
    dish_dictionary = {}
    df = pd.read_csv(csv_file)
    df = df.sort_values(by=["TotalTimeInMins"])
    for dishes in df["TranslatedRecipeName"]:
        if dish.title() in dishes:
            dish_dictionary[count] = []
            dish_dictionary[count].append(dishes)
            count += 1
    if len(dish_dictionary) > 0:
        chosen_dish = dish_dictionary[int(index_number)][0]
        df_new = df[df["TranslatedRecipeName"] == chosen_dish]
        index = df_new.index[0]
        dictionary = df_new.to_dict()
        with open(
            rf"{markdown_file_path}/{chosen_dish}.md",
            "w",
        ) as file:
            file.write(
                f"""# {chosen_dish}\n\n## Cooking time: {dictionary['TotalTimeInMins'][index]} minutes.\n\n## Ingredients:\n{dictionary['Cleaned-Ingredients'][index]}\n\n## Cooking Instructions:\n{dictionary['TranslatedInstructions'][index]}"""
            )

        return FileResponse(f"{markdown_file_path}\\{chosen_dish}.md",media_type='application/octet-stream', filename=chosen_dish + ".md")
    else:
        return {404: "Sorry, we don't have what you are looking for!"}


@router.get("/chefbot/clear_the_menu", tags=["chefbot"])
def clear_the_table():
    """Delete the dishes in the local."""
    for file in os.listdir(markdown_file_path):
        os.remove(os.path.join(markdown_file_path, file))
    return {200: "Table cleared!"}