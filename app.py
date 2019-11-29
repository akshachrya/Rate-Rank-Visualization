from flask import Flask,render_template,request,jsonify
import pandas as pd 
import json
import numpy as np
import random
import string

def categoriesmaker(maxrate,types):
	if types=='rate':
		if maxrate==11:
			category=list(range(0,maxrate))
		if maxrate==5:
			category=list(range(1,maxrate+1))
		if maxrate==7:
			category=['Very Unsatisfied','Unsatisfied','Slightly Unsatisfied','Neutral','Slightly Satisfied','Satisfied','Very Satisfied']
		if maxrate==10:
			category=list(range(1,maxrate+1))
		if maxrate==6:
			category=list(range(1,maxrate+1))
	if types=='rank':
		category=list(range(1,maxrate+1))
	return category

def replacer(dfname,types,maxrate):
	if types=='rate':
		if maxrate==7:
			dfname=dfname.replace(['Very Unsatisfied','Unsatisfied','Slightly Unsatisfied','Neutral',
							'Slightly Satisfied','Satisfied','Very Satisfied'],[1,2,3,4,5,6,7])

	return dfname

def colorpicker(maxrate):
	###Color Code
	if maxrate==10:
		colors=['red','red','red','red','red','red','yellow','yellow','green','green']
	if maxrate==11:
		colors=['red','red','red','red','red','red','red','yellow','yellow','green','green']	
	if maxrate==5:
		colors=['red','red','red','yellow','green']
	if maxrate==7:
		colors=['red','red','red','yellow','yellow','green','green']
	if maxrate==6:
		colors=['red','red','red','yellow','green','green']
	

	return colors
	
def sumcount(dfname,elements,maxrate):
	number={}
	sum=[0]*maxrate
	a=dfname[elements].value_counts().index.tolist()
	b=dfname[elements].value_counts().tolist()
	for i in range(len(a)):
		number[str(int(a[i]))]=b[i]

	for i in range(maxrate):
		if number.get(str(i+1)) != None:
			sum[i]=number[str(i+1)]
		else:
			sum[i]=0
	return sum

def xaxis(categories,name):
	if categories==0:
		xaxis={"title":{"text":name}}
	else:
		xaxis={"categories":categories,"title":{"text":name}}
	return xaxis

def yaxis(a):
	if a==0:
		yaxis={"title":{"text":'Value'}}
		return yaxis
	else:
		yaxis={"title":{"text":'Value'},"max":a/1.25}
		# Max =length of total value /1.25 so the bar plot doesnt meet donut chart
		return yaxis


def titlemaker(df,index):
	if type(index)==int:
		title={"text":df.columns[index],"style":{"fontWeight":'bold',"fontSize":'16px',"color":'black'}}
		return title
	if type(index)==str:
		title={"text":index,"style":{"fontWeight":'bold',"fontSize":'16px',"color":'black'}}
		return title


def subtitleconstructor(df,indexnumber):
	value=nps_score(df[indexnumber])
	if value["NPS Score"]>=(-100) and value["NPS Score"]<0 :
		remarks='Remarks: Needs Improvement'
		color='red'

	if value["NPS Score"]>= 0 and value["NPS Score"]<30 :
		remarks='Remarks: Good'
		color='#CCCC00'

	if value["NPS Score"]>= 30 and value["NPS Score"]<70 :
		remarks='Remarks: Great'
		color='yellowgreen'
	
	if value["NPS Score"]>= 70 and value["NPS Score"]<=100 :
		remarks='Remarks: Excellent'
		color='green'
		
	subtitle= {"text":'NPS Score :'+str(value["NPS Score"])+'<br>'+str(remarks),"align":'center',"style":{"fontWeight":'bold',"fontSize":'14px',"color":color}}
	return subtitle

def ratelistmaker(elements,dfname,maxrate,types):
	list=[]
	# print(dfname)
	rate=categoriesmaker(maxrate,types)	
	counts= sumcount(dfname,elements,maxrate)
	for i in range(len(rate)):
		plotData=[]
		plotData.append(str(rate[i]))
	
		plotData.append(int(counts[i]))
		list.append(plotData)
	return list

def datamaker(dfname,elements,maxrate,types):
	data=[]
	for i in range(len(elements)):
		data.append(ratelistmaker(elements[i],dfname,maxrate,types))
	return data
	

def datameanmaker(dfname,elements):
	data=[]
	for i in range(len(elements)):
		rowcount=dfname[elements[i]].dropna().shape[0]
		sums=dfname[elements[i]].dropna().sum()
		data.append(sums/rowcount)
	return data

def seriesmaker(data,elements):
	series=[]
	for i in range(len(elements)):
		plotData={}
		plotData['name']=elements[i]
		plotData['data']=data[i]
		series.append(plotData)
	return series

def rankseriesmaker(data,elements,maxrate):
	series,weight,mulweight,slicer,sums,a=[],[],[],[],[],[]
	for i in range(maxrate):
		weight.append((i+1)*5)
	weight.sort(reverse = True)
	
	for i in range(len(elements)):
		for j in range(maxrate):
			mulweight.append(data[i][j][1]*weight[j])

	for i in range(len(elements)):
		slicer.append(mulweight[i*maxrate:(i+1)*maxrate])
		sums.append(sum(slicer[i]))
		a.append([elements[i],sums[i]])
	
	a.sort(key=lambda x: x[1],reverse=True)	
	maxo=len(elements)	
	for i in range(len(elements)):
		a[i][1]=maxo
		maxo=maxo-1
		
	plotData={}
	plotData['name']='rank'
	plotData['data']=a
	series.append(plotData)
	return series

# For Tab
def seriesnps(df,dfmain,indexnumber,dataset):
	value=nps_score(df[indexnumber])
	series= [{"type": 'bar',"name": dataset[indexnumber],"data": dfmain[indexnumber]},{"type": 'pie',"name": 'Value',"center": ['90%','10%'], "size":
		'40%',"innerSize":'60%',"data": [['Detractors',int(value["Detractors"])],['Passive',int(value["Passive"])],['Promoters',int(value["Promoters"])]]}]
	return series


# For Gauge
def gaugemeanseries(elements,dfname,name,target):
	meandata=datameanmaker(dfname,elements)
	roundmeandata=[round(x,2) for x in meandata]
	overallmean=round((sum(roundmeandata)/len(elements)),2)	
	data=[]	
	for i in range(len(elements)):
		series1=[]
		series1.append(elements[i])
		series1.append(roundmeandata[i])
		data.append(series1)

	series=[{"name":"target","data": [target],"type": 'gauge',"dial": {"baseLength": "100%","radius": "110%","rearLength": "-45%"}},
	{"name":name,"data": [overallmean],"dial": {"radius": '100%',"baseWidth": 1,"rearLength": '20%'}},{"type": 'pie',
				"name":'Value', "size":'100%',"innerSize":'70%',"data":data}]
	return series

# For scale
def scalemeanseries(elements,dfname,name):
	meandata=datameanmaker(dfname,elements)
	roundmeandata=[round(x,2) for x in meandata]
	overallmean=round((sum(roundmeandata)/len(elements)),2)	
	series=[{"name":name,"data": [overallmean]}]
	return series


def nps_score(score):
	length=len(score)
	if(length==10):
		nps_score=list(range(1,length+1))
		data={'NPS Score':nps_score,'No. of Respondents':score}
		df=pd.DataFrame(data)
		totalrespondents= df['No. of Respondents'].sum()
		if(totalrespondents==0):
			totalrespondents=1
		df['Percentage of Respondents']=round(df['No. of Respondents']*100/totalrespondents,2)
		promoters=df['No. of Respondents'][[8,9]].sum()
		detractors=df['No. of Respondents'][[0,1,2,3,4,5]].sum()
		passive=df['No. of Respondents'][[6,7]].sum()
		
	if(length==11):
		nps_score=list(range(0,length))
		data={'NPS Score':nps_score,'No. of Respondents':score}
		df=pd.DataFrame(data)
		totalrespondents= df['No. of Respondents'].sum()
		if(totalrespondents==0):
			totalrespondents=1
		df['Percentage of Respondents']=round(df['No. of Respondents']*100/totalrespondents,2)
		promoters=df['No. of Respondents'][[9,10]].sum()
		detractors=df['No. of Respondents'][[0,1,2,3,4,5,6]].sum()
		passive=df['No. of Respondents'][[7,8]].sum()
		
	if(length==5):
		nps_score=list(range(1,length+1))
		data={'NPS Score':nps_score,'No. of Respondents':score}
		df=pd.DataFrame(data)
		totalrespondents= df['No. of Respondents'].sum()
		if(totalrespondents==0):
			totalrespondents=1
		df['Percentage of Respondents']=round(df['No. of Respondents']*100/totalrespondents,2)
		promoters=df['No. of Respondents'][[4]].sum()
		detractors=df['No. of Respondents'][[0,1,2]].sum()
		passive=df['No. of Respondents'][[3]].sum()
	
	if(length==7):
		nps_score=list(range(1,length+1))
		data={'NPS Score':nps_score,'No. of Respondents':score}
		df=pd.DataFrame(data)
		totalrespondents= df['No. of Respondents'].sum()
		if(totalrespondents==0):
			totalrespondents=1
		df['Percentage of Respondents']=round(df['No. of Respondents']*100/totalrespondents,2)
		promoters=df['No. of Respondents'][[5,6]].sum()
		detractors=df['No. of Respondents'][[0,1,2]].sum()
		passive=df['No. of Respondents'][[3,4]].sum()
	
	if(length==6):
		nps_score=list(range(1,length+1))
		data={'NPS Score':nps_score,'No. of Respondents':score}
		df=pd.DataFrame(data)
		totalrespondents= df['No. of Respondents'].sum()
		if(totalrespondents==0):
			totalrespondents=1
		df['Percentage of Respondents']=round(df['No. of Respondents']*100/totalrespondents,2)
		promoters=df['No. of Respondents'][[4,5]].sum()
		detractors=df['No. of Respondents'][[0,1,2]].sum()
		passive=df['No. of Respondents'][[3]].sum()

	promotersper=round(promoters/totalrespondents*100,2)
	detractorsper=round(detractors/totalrespondents*100,2)
	passiveper=round(detractors/totalrespondents*100,2)
	NPSscore=round(promotersper-detractorsper,2)
	result={"NPS Score":NPSscore,"Detractors":detractors,"Passive":passive,"Promoters":promoters}
	return result

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def plot():
	if request.method=='POST':
		df =pd.read_csv("rank_Data.csv")
		rateFactors = df
		
		reqdata=request.data
		reqdata=json.loads(reqdata)
		rateFactors=rateFactors[reqdata['topic']]
		maxrate=10
		types='rank'

		columns=rateFactors.columns.str.replace('\d+', '')
		# Since id in js doesnt take number format so renaming it so removing digit from column names
		rateFactors=replacer(rateFactors,types,maxrate)
		data=datamaker(rateFactors,columns,maxrate,types)
		rowcount=rateFactors.shape[0]

		#Overall Rank
		if reqdata['rankplot']=='overallrank':
			categories=categoriesmaker(maxrate,types)
			series=seriesmaker(data,columns)
			title =titlemaker(rateFactors,"Overall Rank Analysis")
			xAxis=xaxis(categories,'Rankings')
			yAxis=yaxis(0)
			resultoverallrank={'series':series,'title':title,'xAxis':xAxis,'yAxis':yAxis}
			result={"resultoverallrank":resultoverallrank}
		

		#Priority
		if reqdata['rankplot']=='rankprior':
			series=rankseriesmaker(data,columns,maxrate)
			categories=list(columns)
			title =titlemaker(rateFactors,"Priority Rank Analysis")
			resultrankprior={'series':series,'title':title}
			result={"resultrankprior":resultrankprior}
		
		return jsonify(result)

	else:
		df =pd.read_csv("rank_Data.csv")
		rateFactors = df
		rateFactors.columns=rateFactors.columns.str.replace('\d+', '')
		# Since id in js doesnt take number format so renaming it so removing digit from column names
		columns=list(rateFactors.columns)
		return render_template('plot.html',columns=columns)

@app.route("/tab",methods=['GET','POST'])
def tab():
	if request.method=='POST':
		df =pd.read_csv("rate_Data.csv")
		rateFactors = df
		rateFactors.columns=rateFactors.columns.str.replace('\d+', '')
		# Since id in js doesnt take number format so renaming it so removing digit from column names

		reqdata=request.data
		reqdata=json.loads(reqdata)
		rateFactors=rateFactors[reqdata['topic']]	
		columns=list(rateFactors.columns)
		maxrate=10
		types='rate'

		rateFactors=replacer(rateFactors,types,maxrate)
		if maxrate<=6:
			mrate=maxrate-1
		else:
			mrate=maxrate-2
		
		#NPS Plot
		if reqdata['nps']=='npsplot':
			data=datamaker(rateFactors,columns,maxrate,types)
			categories=categoriesmaker(maxrate,types)
			rowcount=rateFactors.shape[0]
			subtitle,title,xAxis,yAxis,series=[],[],[],[],[]
			countdata=[]
			
			for i in range(len(columns)):
				counts= sumcount(rateFactors,columns[i],maxrate)
				countdata.append(counts)
				subtitle.append(subtitleconstructor(countdata,i))
				title.append(titlemaker(rateFactors,i))
				xAxis.append(xaxis(categories,types))
				series.append(seriesnps(countdata,data,i,columns))
				yAxis.append(yaxis(rowcount))	
			colors=colorpicker(maxrate)	
			resultnps={'series':series,'xAxis':xAxis,'yAxis':yAxis,'title':title,'subtitle':subtitle,'maxrate':maxrate,'colors':colors}
			result={"resultnps":resultnps}
		
	
		# Combined Mean Plot
		if reqdata['nps']=='ratemean':

			dict={"Combined Mean Value":{"cols":list(columns),"target":mrate,"max":maxrate,"min":0}}
			mainseries,target,min,max=[],[],[],[]

			for i in range(len(dict)):
				mainseries.append(gaugemeanseries(dict[list(dict.keys())[i]]['cols'],rateFactors,list(dict.keys())[i],dict[list(dict.keys())[i]]['target']))
				target.append(dict[list(dict.keys())[i]]['target'])
				min.append(dict[list(dict.keys())[i]]['min'])
				max.append(dict[list(dict.keys())[i]]['max'])
			resultmean={"mainseries":mainseries,"target":target,"max":max,"min":min}
			result={"resultmean":resultmean}
		
		return jsonify(result)
	else:
		df =pd.read_csv("rate_Data.csv")
		rateFactors = df
		rateFactors.columns=rateFactors.columns.str.replace('\d+', '')
		# Since id in js doesnt take number format so renaming it so removing digit from column names
		columns=list(rateFactors.columns)
		return render_template('tab.html',columns=columns)

@app.route("/mean")
def meanplot():
	df =pd.read_csv("rate_Data.csv")
	rateFactors = df
	rateFactors.columns=rateFactors.columns.str.replace('\d+', '')
	# Since id in js doesnt take number format so renaming it so removing digit from column names
	rateFactorsstr=rateFactors.dropna().astype(int)
	
	# User Input
	dict={"Sunday":{"cols":['power','mileage','style','weight'],"target":8,"max":10,"min":0},"JohnWick":{"cols":['power','style','weight'],"target":8,"max":10,"min":0},
		"Matrixe":{"cols":['power','mileage','style','advertisement'],"target":8,"max":10,"min":0},"Mate":{"cols":['power','mileage','style','resaleValue'],"target":8,"max":10,"min":0}}
	
	mainseries,target,min,max,cid=[],[],[],[],[]

	for i in range(len(dict)):
		mainseries.append(gaugemeanseries(dict[list(dict.keys())[i]]['cols'],rateFactorsstr,list(dict.keys())[i],dict[list(dict.keys())[i]]['target']))
		target.append(dict[list(dict.keys())[i]]['target'])
		min.append(dict[list(dict.keys())[i]]['min'])
		max.append(dict[list(dict.keys())[i]]['max'])
	
	return render_template("mean.html",mainseries=mainseries,target=target,max=max,min=min)

@app.route("/npsscale")
def npsscale():
	df =pd.read_csv("rate_Data.csv")
	rateFactors = df
	rateFactors.columns=rateFactors.columns.str.replace('\d+', '')
	# Since id in js doesnt take number format so renaming it so removing digit from column names
	rateFactorsstr=rateFactors.dropna().astype(int)
	maxrate=10
	types='rate'
	# User Input
	dict=['power','mileage','advertisement','resaleValue','lifecycleCost']
	series=[]

	for i in range(len(dict)):
		score=sumcount(rateFactorsstr,dict[i],maxrate)
		npsscore=nps_score(score)["NPS Score"]
		series.append([{"name":dict[i],"data": [npsscore]}])
		
	return render_template("npsscale.html",series=series)

@app.route("/meanscale")
def meanscale():
	df =pd.read_csv("rate_Data.csv")
	rateFactors = df
	rateFactors.columns=rateFactors.columns.str.replace('\d+', '')
	# Since id in js doesnt take number format so renaming it so removing digit from column names
	rateFactorsstr=rateFactors.dropna().astype(int)

	# User Input
	dict={"Matrix":{"cols":['power','mileage','style','weight'],"target":8,"max":10,"min":0},"Matrix":{"cols":['power','mileage'],"target":8,"max":10,"min":0},"JohnWick":{"cols":['power','style','weight'],"target":8,"max":10,"min":0},
		"Matrixe":{"cols":['power','mileage','style','advertisement'],"target":7.5,"max":10,"min":0},"Mate":{"cols":['power','mileage','style','resaleValue'],"target":8,"max":10,"min":0},"Mate1":{"cols":['power','mileage','style','resaleValue'],"target":8,"max":10,"min":0}}
	
	mainseries,target,min,max=[],[],[],[]

	for i in range(len(dict)):
		mainseries.append(scalemeanseries(dict[list(dict.keys())[i]]['cols'],rateFactorsstr,list(dict.keys())[i]))
		target.append(dict[list(dict.keys())[i]]['target'])
		min.append(dict[list(dict.keys())[i]]['min'])
		max.append(dict[list(dict.keys())[i]]['max'])
	
	return render_template("meanscale.html",mainseries=mainseries,target=target,max=max,min=min)

if __name__=="__main__":
    app.run(debug=True)
