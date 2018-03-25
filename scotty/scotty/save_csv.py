import os
import json
from pandas.io.json import json_normalize

os.system("echo hi")

fileoutput = ""
for i in range(1, 81):
    f_data = open('./fixed_data_results/fixed_data_' + str(i) + '.json', 'r')
    if i == 1:
        fileoutput = fileoutput + f_data.read()
    if i > 1:
        fileoutput = fileoutput + ',' + f_data.read()

fileoutput = '[' + fileoutput + ']'
Parsed_data = json.loads(fileoutput)
nom_dataframe = json_normalize(Parsed_data)
nom_dataframe.to_csv('./combined_results/fixed_data_results.csv', sep=',')

fileoutput2 = ""
for i in range(1, 61):
    f_data = open('./fixed_MTU_results/fixed_MTU_' + str(i) + '.json', 'r')
    if i == 1:
        fileoutput2 = fileoutput2 + f_data.read()
    if i > 1:
        fileoutput2 = fileoutput2 + ',' + f_data.read()

fileoutput2 = '[' + fileoutput2 + ']'
Parsed_data2 = json.loads(fileoutput2)
nom_dataframe2 = json_normalize(Parsed_data2)
nom_dataframe2.to_csv('./combined_results/fixed_MTU_results.csv', sep=',')

fileoutput3 = ""
for i in range(1, 61):
    f_data = open('./fixed_MTU_Jumbo_results/fixed_MTU_Jumbo_' +
                  str(i) + '.json', 'r')
    if i == 1:
        fileoutput3 = fileoutput3 + f_data.read()
    if i > 1:
        fileoutput3 = fileoutput3 + ',' + f_data.read()

fileoutput3 = '[' + fileoutput3 + ']'
Parsed_data3 = json.loads(fileoutput3)
nom_dataframe3 = json_normalize(Parsed_data3)
nom_dataframe3.to_csv('./combined_results/fixed_MTU_Jumbo_results.csv', sep=',')

finalname='combined_results_$(date -d "today" +"%Y%m%d%H%M").tar.gz'
os.system(' tar -czvf '+finalname+' combined_results')
os.system('rsync -v -e ssh '+finalname+' vagrant@10.1.0.1:~')
