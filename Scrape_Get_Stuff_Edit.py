#Imports and Installs
import requests as r
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd
import re 
from selenium.webdriver import Edge
import pandas as pd
import time
from selenium.webdriver.common.by import By

'''
This is used to convert the result to a csv file. Do it manually
and remember to update the range of the for loop run over so
there are no repeats

data.to_csv("Scrap(1-484)_Data_219" , encoding = "utf-8")
'''
count_runs = 0
key = 0
dict_results = {}
execute_break = False
for num in range(0,100):
	if execute_break:
		break
	try:
		driver = Edge()
		link = "https://dashfight.com/players/" + str(num)
		list_add=[]
		#get page and make soup
		driver.get(link)
		time.sleep(2)
		#Force browser to scroll down to load the data
		try:
			the_element = driver.find_element(By.CLASS_NAME , "MatchUpCardSkeleton_block__XMsCj")
			driver.execute_script("arguments[0].scrollIntoView();", the_element)
		except:
			driver.execute_script("window.scrollTo(0,2500)")
		#make soup
		time.sleep(4)
		soup = BeautifulSoup(driver.page_source,"html.parser")
		
		#get age and years playing
		try:
			years_playing = re.findall("Playing : \S*" , soup.select(".GeneralSideInfo_table__LbNsR")[0].get_text())[0]
		except:
			years_playing = "NaN"
	
		try:
			age = re.findall("Birthday : \w*\s\d\d,\s\d\d\d\d\s\S*" , soup.select(".GeneralSideInfo_table__LbNsR")[0].get_text())[0]
		except:
			age =  "NaN"
	
		#get tag
		try:
			tag = soup.select(".GeneralInfo_name__jiFXt")[0].text
		except:
			tag = "NaN"
	
		#get name clan and country
		temp = []
		try:
			temp = soup.select(".GeneralInfo_value__cbI5P")
		except:
			name = "NaN"
			clan = "NaN"
			local = "NaN"
			
		if len(temp) < 3:
			try:
				name = temp[0].text
			except:
				name = "NaN"
			try:
				local = temp[1].text
			except:
				local = "NaN"
			clan = "NaN"
		else:
			try:
				clan = temp[1].text
			except:
				clan = "NaN"	
			try:
				name = temp[0].text
			except:
				name = "NaN"
			try:
				local = temp[2].text
			except:
				local = "NaN"
	
		#get matches and win_rate
		try:
			temp = soup.select(".Statistic_value__akZNQ")
		except:
			matches = "NaN"
			win_rate = "NaN"
		try:
			matches = temp[0].text
		except:
			matches = "NaN"
		try:
			win_rate = temp[1].text
		except:
			win_rate = "NaN"
	
		#get bio
		try:
			bio = soup.body.div.select(".Bio_bioBlock__yrwwc")[0].get_text()
		except:
			bio = "NaN"
			
		#Get top char and the top char stats
		try:
			info = soup.body.select(".MatchUpList_block__PyQun")[0]
			string_result = info.select(".MatchUpCard_block__B67jP")[0].get_text()
			try:
				top_char = re.findall("\w*", string_result)[0]
			except:
				top_char = "NaN"
			try:
				stats = re.findall("\d*\s-\s\d*" , string_result)[0]
			except:
				stats = "NaN"
		except:
			top_char = "NaN"
			stats = "NaN"
		
		#info for 2022
		try:
			r.get(link + "/rankings?season=2022").raise_for_status()
			x = r.get(link + "/rankings?season=2022")
			soup = BeautifulSoup(x.text,"html.parser")
			DF_2022 = soup.select(".PlayerPoints_points__WyHGG")[1].get_text()
			Global_2022 = soup.select(".Rate_text__JN5Om")[0].get_text()
			NA_2022 = soup.select(".Rate_text__JN5Om")[1].get_text()
		except:
			DF_2022 = "NaN"
			Global_2022 = "NaN" 
			NA_2022 = "NaN"
			
		#info for 2023
		try:
			r.get(link + "/rankings?season=2023").raise_for_status()
			x = r.get(link + "/rankings?season=2023")
			soup = BeautifulSoup(x.text,"html.parser")
			DF_2023 = soup.select(".PlayerPoints_points__WyHGG")[0].get_text()
			Global_2023 = soup.select(".Rate_text__JN5Om")[0].get_text()
		except:
			DF_2023 = "NaN"
			Global_2023 = "NaN"
		
		
		
		#add  everything to the list
		list_add.append(age)
		list_add.append(name)
		list_add.append(years_playing)
		list_add.append(tag)
		list_add.append(clan)
		list_add.append(local)
		list_add.append(matches)
		list_add.append(win_rate)
		list_add.append(bio)
		list_add.append(top_char)
		list_add.append(stats)
		list_add.append(DF_2022)
		list_add.append(Global_2022)
		list_add.append(NA_2022)
		list_add.append(DF_2023)
		list_add.append(Global_2023)
		
		#quit the driver
		driver.quit()
		
		#Add to overall dict and make sure its not all NaN
		count_nan = 0
		for val in list_add:
			if "NaN" in val:
				count_nan+=1
		
		if count_nan != len(list_add):
			dict_results[key] = list_add
			key += 1
		else:
			pass
		count_runs += 1
	except KeyboardInterrupt:
		execute_break = True
	except:
		count_runs +=1
		pass
	
data = pd.DataFrame.from_dict(dict_results,orient='index', columns = ['age' , 'name', 'years_playing' , 'tag' , 'clan' , 'local' , 'matches' , 'win_rate' , 'bio' , 'top_character' , 'top_character_stats' , 'DF_2022' , 'Global_2022' , 'NA_2022' , 'Df_2023' , 'Global_2023'])











	
	


