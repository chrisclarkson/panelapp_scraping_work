import requests
import bs4
import re
import sys
import os

os.system('rm '+sys.argv[1])
headers=["PanelName","GeneSymbol","LevelOfConfidence","Penetrance","ModeOfInheritance","MutationType","CurrentVersion","DiseaseSubGroup","DiseaseGroup","RelevantDisorders","PanelTypes"]
with(open(sys.argv[1],'w')) as f:
	f.write('\t'.join(headers)+'\n')

index_url = 'https://panelapp.genomicsengland.co.uk/'
response = requests.get(index_url+'panels/')
soup = bs4.BeautifulSoup(response.text)
connect={}
idx = []

rows = soup.find_all('tr')
# print(rows)
for row in rows:
	description=row.text.encode('utf-8')
	# print(description)
	if ' Super Panel' in description and 'Component Of' not in description:
		# print('content')
		# relevant_disorders=row.find_all('br').text.encode('utf-8')
		# print(relevant_disorders)
		PanelName=row.find_all('h5', attrs={"class":"remove-bottom-margin"})[0].text.encode('utf-8').replace('\n','').strip()
		paragraphs=row.find_all('p')
		# print(paragraphs)
		rd_attained,pt_attained=False,False
		for p in paragraphs:
			text=p.text
			if 'Panel Types:' in text:
				panel_type=text.encode('utf-8').replace('Panel Types: ','').strip()
				pt_attained=True
			if 'Relevant disorders' in text:
				relevant_disorders=text.encode('utf-8').replace('Relevant disorders: ','').strip()
				relevant_disorders=relevant_disorders.split('\n')[0]
				rd_attained=True
		if rd_attained and pt_attained:
			print(panel_type,relevant_disorders)
			link = 'https://panelapp.genomicsengland.co.uk'+str(row.find('a').get('href'))
			print(link)
			soupling=bs4.BeautifulSoup(requests.get(link).text)
			# print(soupling)
			table=soupling.find_all('tbody')
			for tab in table:
				rows2=tab.find_all('tr')
				for row2 in rows2:
					columns=row2.find_all('td')
					columns_out=[col.text.replace('\n',' ').strip().encode('utf-8') for col in columns]
					color=columns_out[0].split(' ')[0]
					gene=columns_out[1].replace('\n','').lstrip()
					GeneSymbol=gene.split(' ')[0]
					if '_' in GeneSymbol:
						MutationType='STR'
					else:
						MutationType='gene'
					CurrentVersion=gene.split('v')[1]
					phenotype_col=columns_out[4]
					if 'Phenotypes' in phenotype_col:
						phenotypes=phenotype_col.split('Phenotypes')[1]
					else:
						phenotypes=''
					inheritance_cols=columns_out[3].split(',')
					if len(inheritance_cols)==3:
						mode_of_inheritance,penetrance,imprint=inheritance_cols
					elif len(inheritance_cols)==2:
						mode_of_inheritance,penetrance=inheritance_cols
					else:
						continue
					# print('eeee')
					if color=='Green':
						output=[PanelName,GeneSymbol,'HighEvidence',penetrance,mode_of_inheritance.lstrip(),MutationType,CurrentVersion,'',phenotypes,panel_type,relevant_disorders]
						# for o in output:
						# 	print(o)
						# 	print('dddd')
						file2=open(sys.argv[1],'a')
						file2.write('\t'.join(output)+'\n')
						file2.close()

headers=["PanelName","GeneSymbol","LevelOfConfidence","Penetrance","ModeOfInheritance","MutationType","CurrentVersion","DiseaseSubGroup","DiseaseGroup","RelevantDisorders","PanelTypes"]


