import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import os
from PIL import Image

developing_countries = [
    "afghanistan", "angola", "bangladesh", "benin", "bhutan", "burkina-faso", 
    "burundi", "cambodia", "cameroon", "central-african-republic", "comoros", 
    "democratic-republic-of-the-congo", "djibouti", "egypt", "eritrea", 
    "eswatini", "ethiopia", "the-gambia", "ghana", "guinea", "guinea-bissau", "haiti", 
    "honduras", "india", "indonesia", "cote-d-ivoire", "kenya", "lao-people-s-democratic-republic", "lesotho", 
    "liberia", "madagascar", "malawi", "mali", "mauritania", "mongolia", 
    "mozambique", "myanmar", "namibia", "nepal", "nicaragua", "niger", "nigeria", "pakistan", 
    "papua-new-guinea", "philippines", "rwanda", "senegal", "sierra-leone", "solomon-islands", "sri-lanka", "sudan", "suriname", "tanzania", "timor-leste", "togo", 
    "uganda", "uzbekistan", "vanuatu", "venezuela-bolivarian-republic-of", "yemen", "zambia", "zimbabwe", "turkmenistan", 
    "serbia", "kyrgyz-republic", "tajikistan", "armenia", "mongolia", "belarus", "malawi", "algeria", 
    "morocco", "sudan", "libya", "gabon", "chile", "colombia", "paraguay", "peru", "ecuador", "suriname"
]

develop_count_display = [
    "Select your country","afghanistan", "angola", "bangladesh", "benin", "bhutan", "burkina-faso", 
    "burundi", "cambodia", "cameroon", "central-african-republic", "comoros", 
    "democratic-republic-of-the-congo", "djibouti", "egypt", "eritrea", 
    "eswatini", "ethiopia", "the-gambia", "ghana", "guinea", "guinea-bissau", "haiti", 
    "honduras", "india", "indonesia", "cote-d-ivoire", "kenya", "lao-people-s-democratic-republic", "lesotho", 
    "liberia", "madagascar", "malawi", "mali", "mauritania", "mongolia", 
    "mozambique", "myanmar", "namibia", "nepal", "nicaragua", "niger", "nigeria", "pakistan", 
    "papua-new-guinea", "philippines", "rwanda", "senegal", "sierra-leone", "solomon-islands", "sri-lanka", "sudan", "suriname", "tanzania", "timor-leste", "togo", 
    "uganda", "uzbekistan", "vanuatu", "venezuela-bolivarian-republic-of", "yemen", "zambia", "zimbabwe", "turkmenistan", 
    "serbia", "kyrgyz-republic", "tajikistan", "armenia", "mongolia", "belarus", "malawi", "algeria", 
    "morocco", "sudan", "libya", "gabon", "chile", "colombia", "paraguay", "peru", "ecuador", "suriname"
]

img = Image.open("removebgverexpertexport.png").resize((50,65))
st.sidebar.image(img)
st.sidebar.title("Expert Exports")
sidebar = st.sidebar.radio("Pages", options=["Expert Exports", "Our Mission"])

if sidebar == "Expert Exports":
    for index, x in enumerate(develop_count_display):
        develop_count_display[index] = x.title()

    st.title("**Expert Exports**")
    country = st.selectbox("**Enter your country below**", options=develop_count_display, help= "Check to see if you have a valid country", index=0).lower()
    if country != "select your country":
        os.system("cls")
        data = pd.read_csv("expertexports.csv", index_col=0)
        ex = str(data.loc[country,"exports"][2:-2]).split(",")
        for ind, i in enumerate(ex):
            i = i.replace("'","")
            ex[ind] = i.strip()
        #print(ex,"\n",data.loc[country,"exports"])
        manual = st.multiselect("**Select specific exports search for (Optional)**", options=ex)
        if "".join(manual).strip() != "":
            ex = manual


        suggestions = []

        for j in ex:
            # loop through each export, make a nested for loop: fist a loop in range from (0,11) then loop through the developing countries list using .loc[country,"imports"]
            found = False
            indiv_suggest = []
            for num in range(0,11):
                if found == True:
                    break
                for state in developing_countries:
                    imps = str(data.loc[state,"imports"][2:-2]).split(",")
                    for ind, i in enumerate(imps):
                        i = i.replace("'","")
                        imps[ind] = i.strip()
                    try:
                        if imps[num] == j:
                            suggestions.append(state)
                            found = True
                    except:
                        break
        suggestions = list(set(suggestions))
        for inx, suggestion in enumerate(suggestions):
            suggestions[inx] = suggestion.title()
        st.markdown("**Based on your exports, here are countries that you could establish trade deals with.**")
        st.markdown(f"Like-minded nations: {", ".join(suggestions)}")   
        print(suggestions) 
        if "".join(suggestions).strip() == "":
            st.write("Looks like your exports do not allign with in demand goods from other developing countries. To be integrated into South-South trade, it is essential that you produce materials sought after by the developing world. It appears your country's goods are valued higher in industrialized, high-income markets.")
        os.system("cls")
elif sidebar == "Our Mission":
    st.title("Our Mission")
    st.header("The Problem")
    st.markdown("*The global economy is characterized by the uneven development of developed core states and developing peripheral states. Lingering colonial imprints can be predominantly seen in the continents of Asia, South America, and Africa. In the contemporary era, the world has seen the influence of neocolonialism—when core states, typically prior colonial powers, exploit the natural resources of the periphery. Consequently, peripheral states are heavily dependent on core states, often exporting crude, unprocessed materials to core states. Thus, developing states become increasingly dependent on core states; their overreliance on certain exports and cash crops such as coffee can lead to economic collapse after increased competition or changes in consumer tastes. Since underdeveloped states are more concerned about sustaining their population, international trade agreements are not made between two developing states—also known as South-South trade. In fact, in 2023, less than a quarter of global commerce was from South-South trade. Rather, peripheral states typically trade with core states, redistributing wealth to the privileged, developed world.*\n")
    st.header("The Solution")
    st.markdown("*To reduce the pervasive effects of neocolonialism, we propose to construct a website that aims to diversify the commercial portfolios of peripheral states, to prevent sudden economic upheaval. The website will utilize export and import data from countries in the developing world, to aid a country's decision making on exports, stimulating economic growth in once underdeveloped regions. This idea would address goal 8 and 17 of UN's 17 Sustainable Development Goals (https://sdgs.un.org/goals). Specifically, diverse agricultural portfolios would lead to economic growth and prosperity due to increased trade with other countries, eventually turning once underdeveloped regions into booming, cosmopolitan hubs.*")

def create_csv():
    csv_dict = {
        "imports": [],
        "exports": []
    }

    imps = []
    exps = []

    for country in developing_countries:
        url = f"https://ttd.wto.org/en/profiles/{country}"

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")


        imports = soup.find_all("div", class_ = "col-span-2")[0]
        exports = soup.find_all("div", class_ = "col-span-2")[1]

        # exports = soup.find("section")
        txt = imports.find_all("div", class_ = "self-center")
        import_products = []
        txt_2 = exports.find_all("div", class_ = "self-center")
        export_products = []


        for i in txt:
            element = i.get_text().strip()
            listver = list(element)
            del listver[0:6]
            while True:
                try:
                    listver.remove(",")
                except:
                    break
            element = "".join(listver).strip()
            import_products.append(element)
        del import_products[-1]
        imps.append(import_products)

        for j in txt_2:
            element = j.get_text().strip()
            listver = list(element)
            del listver[0:6]
            while True:
                try:
                    listver.remove(",")
                except:
                    break
            element = "".join(listver).strip()
            export_products.append(element)
        del export_products[-1]
        exps.append(export_products)

    csv_dict["imports"] = imps
    csv_dict["exports"] = exps
    df = pd.DataFrame(csv_dict)
    df.index = developing_countries
    df.to_csv("expertexports.csv",index=True)
