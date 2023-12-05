import pandas as pd
from io import StringIO

# Define a sample CSV data as a string to simulate reading from a file.
csv_data = """
Institution code (UKPRN),Institution name,Institution sort order,Main panel,Unit of assessment number,Unit of assessment name,Multiple submission letter,Multiple submission name,Joint submission,Profile,FTE of submitted staff,Total FTE of submitted staff for joint submission,% of eligible staff submitted,4*,3*,2*,1*,Unclassified,Latitude,Longitude,Score
10003270,Imperial College of Science Technology and Medicine,64,B,11,Computer Science and Informatics,,,,Environment,58.45,,100,1.0,0.0,0.0,0.0,0,51.4988,-0.1749,400.0
10007158,University of Southampton,127,B,11,Computer Science and Informatics,,,,Environment,47.26,,100,1.0,0.0,0.0,0.0,0,50.9357,-1.3966,400.0
10007798,The University of Manchester,88,B,11,Computer Science and Informatics,,,,Environment,53.1,,100,1.0,0.0,0.0,0.0,0,53.4668,-2.2339,400.0
10007790,University of Edinburgh,44,B,11,Computer Science and Informatics,,,,Environment,144.04,,100,1.0,0.0,0.0,0.0,0,55.9445,-3.1892,400.0
10007154,University of Nottingham,98,B,11,Computer Science and Informatics,,,,Environment,46.2,,100,1.0,0.0,0.0,0.0,0,52.9388,-1.1981,400.0
10007774,University of Oxford,100,B,11,Computer Science and Informatics,,,,Environment,73.65,,100,100.0,0.0,0.0,0.0,0,51.7548,-1.2544,400.0
10007788,University of Cambridge,25,B,11,Computer Science and Informatics,,,,Environment,80.8,,105,100.0,0.0,0.0,0.0,0,52.2054,0.1132,400.0
10007157,The University of Sheffield,123,B,11,Computer Science and Informatics,,,,Environment,56.75,,100,87.5,12.5,0.0,0.0,0,53.3814,-1.4884,387.5
10007167,University of York,157,B,11,Computer Science and Informatics,,,,Environment,44.4,,100,87.5,12.5,0.0,0.0,0,53.9461,-1.0518,387.5
10007784,University College London,146,B,11,Computer Science and Informatics,,,,Environment,100.2,,100,87.5,12.5,0.0,0.0,0,51.5246,-0.134,387.5
10006840,The University of Birmingham,14,B,11,Computer Science and Informatics,,,,Environment,42.7,,100,87.5,12.5,0.0,0.0,0,52.4508,-1.9305,387.5
10007786,University of Bristol,21,B,11,Computer Science and Informatics,,,,Environment,59.15,,100,75.0,25.0,0.0,0.0,0,51.4585,-2.6022,375.0
10007768,The University of Lancaster,71,B,11,Computer Science and Informatics,,,,Environment,49.45,,100,75.0,25.0,0.0,0.0,0,54.0104,-2.7877,375.0
10007795,The University of Leeds,72,B,11,Computer Science and Informatics,,,,Environment,34.25,,100,62.5,37.5,0.0,0.0,0,53.8067,-1.555,362.5
10003645,King's College London,69,B,11,Computer Science and Informatics,,,,Environment,48.5,,100,62.5,37.5,0.0,0.0,0,51.5115,-0.116,362.5
10007163,The University of Warwick,149,B,11,Computer Science and Informatics,,,,Environment,41.6,,100,62.5,37.5,0.0,0.0,0,52.3793,-1.5615,362.5
10005553,Royal Holloway and Bedford New College,118,B,11,Computer Science and Informatics,,,,Environment,38.1,,100,62.5,37.5,0.0,0.0,0,51.4232,-0.5593,362.5
10007794,University of Glasgow,49,B,11,Computer Science and Informatics,,,,Environment,46.6,,100,62.5,37.5,0.0,0.0,0,55.8724,-4.29,362.5
10006842,The University of Liverpool,78,B,11,Computer Science and Informatics,,,,Environment,40.75,,100,50.0,50.0,0.0,0.0,0,53.4048,-2.9653,350.0
10007775,Queen Mary University of London,105,B,11,Computer Science and Informatics,,,,Environment,68.8,,100,50.0,50.0,0.0,0.0,0,51.5241,-0.0404,350.0
10007799,University of Newcastle upon Tyne,92,B,11,Computer Science and Informatics,,,,Environment,49.8,,100,50.0,50.0,0.0,0.0,0,54.9792,-1.6147,350.0
10007850,The University of Bath,10,B,11,Computer Science and Informatics,,,,Environment,29.0,,100,37.5,62.5,0.0,0.0,0,51.3782,-2.3264,337.5
10007807,University of Ulster,145,B,11,Computer Science and Informatics,,,,Environment,69.6,,100,25.0,75.0,0.0,0.0,0,54.6046,-5.9291,325.0
10007773,The Open University,99,B,11,Computer Science and Informatics,,,,Environment,44.7,,55,25.0,75.0,0.0,0.0,0,52.0249,-0.7082,325.0
10007814,Cardiff University / Prifysgol Caerdydd,28,B,11,Computer Science and Informatics,,,,Environment,45.55,,100,25.0,75.0,0.0,0.0,0,51.4866,-3.1789,325.0
10007803,University of St Andrews,129,B,11,Computer Science and Informatics,,,,Environment,30.1,,100,12.5,87.5,0.0,0.0,0,56.3417,-2.7943,312.5
10007852,University of Dundee,39,B,11,Computer Science and Informatics,,,,Environment,13.5,,100,12.5,87.5,0.0,0.0,0,56.4582,-2.9821,312.5
10007806,University of Sussex,140,B,11,Computer Science and Informatics,,,,Environment,26.9,,100,12.5,87.5,0.0,0.0,0,50.8677,-0.0875,312.5
10007143,University of Durham,40,B,11,Computer Science and Informatics,,,,Environment,26.2,,100,12.5,87.5,0.0,0.0,0,54.765,-1.5782,312.5
10007160,The University of Surrey,139,B,11,Computer Science and Informatics,,,,Environment,22.5,,100,0.0,100.0,0.0,0.0,0,51.2431,-0.5895,300.0
10007764,Heriot-Watt University,59,B,11,Computer Science and Informatics,,,,Environment,31.7,,100,0.0,100.0,0.0,0.0,0,55.9095,-3.3206,300.0
10004113,Loughborough University,87,B,11,Computer Science and Informatics,,,,Environment,26.0,,100,12.5,62.5,25.0,0.0,0,52.765,-1.2321,287.5
10007855,Swansea University / Prifysgol Abertawe,141,B,11,Computer Science and Informatics,,,,Environment,32.9,,100,12.5,62.5,25.0,0.0,0,51.6092,-3.98,287.5
10007802,The University of Reading,108,B,11,Computer Science and Informatics,,,,Environment,10.4,,100,0.0,87.5,12.5,0.0,0,51.4403,-0.9421,287.5
10007783,University of Aberdeen,1,B,11,Computer Science and Informatics,,,,Environment,15.5,,100,0.0,87.5,12.5,0.0,0,57.1648,-2.1015,287.5
10007789,The University of East Anglia,41,B,11,Computer Science and Informatics,,,,Environment,28.3,,100,12.5,62.5,25.0,0.0,0,52.6221,1.2411,287.5
10001478,City University of London,32,B,11,Computer Science and Informatics,,,,Environment,36.2,,100,0.0,87.5,12.5,0.0,0,51.528,-0.1025,287.5
10007150,The University of Kent,68,B,11,Computer Science and Informatics,,,,Environment,34.7,,100,0.0,75.0,25.0,0.0,0,51.2967,1.063,275.0
10007151,University of Lincoln,77,B,11,Computer Science and Informatics,,,,Environment,28.8,,100,0.0,75.0,25.0,0.0,0,53.2285,-0.5478,275.0
10007801,University of Plymouth,102,B,11,Computer Science and Informatics,,,,Environment,14.62,,100,0.0,75.0,25.0,0.0,0,50.3759,-4.1396,275.0
10007147,University of Hertfordshire,60,B,11,Computer Science and Informatics,,,,Environment,31.21,,45,0.0,75.0,25.0,0.0,0,51.7517,-0.24,275.0
10003678,Kingston University,70,B,11,Computer Science and Informatics,,,,Environment,22.0,,55,0.0,62.5,37.5,0.0,0,51.4032,-0.3035,262.5
10007791,University of Essex,46,B,11,Computer Science and Informatics,,,,Environment,73.0,,100,0.0,62.5,37.5,0.0,0,51.8777,0.9472,262.5
10001282,University of Northumbria at Newcastle,95,B,11,Computer Science and Informatics,,,,Environment,64.41,,90,0.0,62.5,37.5,0.0,0,54.9765,-1.6071,262.5
10007792,University of Exeter,47,B,11,Computer Science and Informatics,,,,Environment,27.9,,100,0.0,62.5,37.5,0.0,0,50.7371,-3.5351,262.5
10001883,De Montfort University,37,B,11,Computer Science and Informatics,,,,Environment,53.3,,65,0.0,50.0,50.0,0.0,0,52.6298,-1.1399,250.0
10007856,Aberystwyth University / Prifysgol Aberystwyth,3,B,11,Computer Science and Informatics,,,,Environment,27.82,,100,0.0,50.0,50.0,0.0,0,52.4183,-4.0639,250.0
10007796,The University of Leicester,76,B,11,Computer Science and Informatics,,,,Environment,19.7,,100,0.0,50.0,50.0,0.0,0,52.6211,-1.1246,250.0
10007805,University of Strathclyde,136,B,11,Computer Science and Informatics,,,,Environment,31.8,,100,0.0,50.0,50.0,0.0,0,55.8621,-4.2424,250.0
10000961,Brunel University London,22,B,11,Computer Science and Informatics,,,,Environment,37.3,,100,0.0,50.0,50.0,0.0,0,51.5321,-0.4727,250.0
10007760,Birkbeck College,13,B,11,Computer Science and Informatics,,,,Environment,25.6,,100,0.0,50.0,50.0,0.0,0,51.5219,-0.1303,250.0
10007772,Edinburgh Napier University,45,B,11,Computer Science and Informatics,,,,Environment,39.4,,75,0.0,37.5,62.5,0.0,0,55.9332,-3.2142,237.5
10000886,University of Brighton,20,B,11,Computer Science and Informatics,,,,Environment,15.0,,40,0.0,37.5,62.5,0.0,0,50.8598,-0.0879,237.5
10002718,Goldsmiths' College,54,B,11,Computer Science and Informatics,,,,Environment,32.55,,100,0.0,50.0,37.5,12.5,0,51.4743,0.0354,237.5
10007800,University of the West of Scotland,152,B,11,Computer Science and Informatics,,,,Environment,25.0,,55,0.0,37.5,62.5,0.0,0,55.7782,-4.1041,237.5
10007804,University of Stirling,134,B,11,Computer Science and Informatics,,,,Environment,18.0,,100,0.0,25.0,75.0,0.0,0,56.1461,-3.9178,225.0
10007156,University of Salford,121,B,11,Computer Science and Informatics,,,,Environment,16.0,,60,0.0,25.0,75.0,0.0,0,53.4872,-2.2737,225.0
10007149,The University of Hull,63,B,11,Computer Science and Informatics,,,,Environment,11.0,,100,0.0,25.0,75.0,0.0,0,53.7731,-0.367,225.0
10005500,Robert Gordon University,109,B,11,Computer Science and Informatics,,,,Environment,10.0,,30,0.0,25.0,75.0,0.0,0,57.1189,-2.1379,225.0
10007165,The University of Westminster,153,B,11,Computer Science and Informatics,,,,Environment,21.4,,40,0.0,25.0,75.0,0.0,0,51.517,-0.1432,225.0
10003957,Liverpool John Moores University,80,B,11,Computer Science and Informatics,,,,Environment,42.0,,70,0.0,25.0,75.0,0.0,0,53.4033,-2.9731,225.0
10004797,Nottingham Trent University,97,B,11,Computer Science and Informatics,,,,Environment,15.4,,70,0.0,25.0,75.0,0.0,0,52.9581,-1.1542,225.0
10004351,Middlesex University,91,B,11,Computer Science and Informatics,,,,Environment,64.55,,70,0.0,25.0,75.0,0.0,0,51.5897,-0.2293,225.0
10007759,Aston University,8,B,11,Computer Science and Informatics,,,,Environment,34.0,,100,0.0,12.5,87.5,0.0,0,52.4867,-1.8882,212.5
10007155,University of Portsmouth,103,B,11,Computer Science and Informatics,,,,Environment,29.8,,45,0.0,12.5,87.5,0.0,0,50.7953,-1.0939,212.5
10004180,Manchester Metropolitan University,89,B,11,Computer Science and Informatics,,,,Environment,23.0,,40,0.0,12.5,87.5,0.0,0,53.4703,-2.2393,212.5
10007785,The University of Bradford,19,B,11,Computer Science and Informatics,,,,Environment,19.0,,65,0.0,12.5,75.0,12.5,0,53.7915,1.7661,200.0
10007159,University of Sunderland,138,B,11,Computer Science and Informatics,,,,Environment,6.7,,25,0.0,0.0,100.0,0.0,0,54.9096,-1.3838,200.0
10007767,University of Keele,67,B,11,Computer Science and Informatics,,,,Environment,15.0,,85,0.0,0.0,100.0,0.0,0,53.003,-2.2721,200.0
10000824,Bournemouth University,18,B,11,Computer Science and Informatics,,,,Environment,45.75,,80,0.0,12.5,75.0,12.5,0,50.722,-1.8667,200.0
10007164,University of the West of England Bristol,151,B,11,Computer Science and Informatics,,,,Environment,28.6,,35,0.0,12.5,75.0,12.5,0,51.5006,-2.5474,200.0
10005790,Sheffield Hallam University,124,B,11,Computer Science and Informatics,,,,Environment,25.6,,30,0.0,12.5,75.0,12.5,0,53.3784,-1.4663,200.0
10007140,Birmingham City University,15,B,11,Computer Science and Informatics,,,,Environment,30.0,,35,0.0,0.0,75.0,25.0,0,52.4864,-1.9175,175.0
10004930,Oxford Brookes University,101,B,11,Computer Science and Informatics,,,,Environment,17.3,,65,0.0,0.0,75.0,25.0,0,51.755,-1.2242,175.0
10007793,University of South Wales,126,B,11,Computer Science and Informatics,,,,Environment,13.7,,35,0.0,0.0,75.0,25.0,0,51.479,-3.1694,175.0
10007148,The University of Huddersfield,62,B,11,Computer Science and Informatics,,,,Environment,27.2,,85,0.0,0.0,75.0,25.0,0,53.6428,-1.7781,175.0
10007823,Edge Hill University,43,B,11,Computer Science and Informatics,,,,Environment,19.0,,95,0.0,0.0,75.0,25.0,0,53.5588,-2.8703,175.0
10007146,University of Greenwich,55,B,11,Computer Science and Informatics,,,,Environment,18.8,,35,0.0,0.0,62.5,37.5,0,51.483,-0.0064,162.5
10007141,University of Central Lancashire,29,B,11,Computer Science and Informatics,,,,Environment,14.0,,55,0.0,0.0,50.0,50.0,0,53.7645,-2.7083,150.0
10007851,University of Derby,38,B,11,Computer Science and Informatics,,,,Environment,17.0,,50,0.0,0.0,50.0,50.0,0,52.9379,-1.4972,150.0
10007144,University of East London,42,B,11,Computer Science and Informatics,,,,Environment,12.2,,60,0.0,0.0,50.0,50.0,0,51.5563,0.0655,150.0
10004048,London Metropolitan University,83,B,11,Computer Science and Informatics,,,,Environment,9.3,,100,0.0,0.0,50.0,50.0,0,51.5526,-0.1113,150.0
10007152,University of Bedfordshire,12,B,11,Computer Science and Informatics,,,,Environment,10.0,,45,0.0,0.0,50.0,50.0,0,51.8779,-0.4093,150.0
10006566,The University of West London,150,B,11,Computer Science and Informatics,,,,Environment,9.8,,70,0.0,0.0,50.0,50.0,0,51.5069,-0.3032,150.0
10007762,Glasgow Caledonian University,50,B,11,Computer Science and Informatics,,,,Environment,14.0,,25,0.0,0.0,50.0,50.0,0,55.8668,-4.25,150.0
10007166,University of Wolverhampton,155,B,11,Computer Science and Informatics,,,,Environment,11.0,,35,0.0,0.0,50.0,50.0,0,52.5881,-2.1275,150.0
10003956,Liverpool Hope University,79,B,11,Computer Science and Informatics,,,,Environment,13.5,,100,0.0,0.0,37.5,62.5,0,53.3908,-2.8923,137.5
10003861,Leeds Beckett University,74,B,11,Computer Science and Informatics,,,,Environment,10.8,,35,0.0,0.0,12.5,87.5,0,53.8035,-1.548,112.5
10007848,University of Chester,30,B,11,Computer Science and Informatics,,,,Environment,7.6,,50,0.0,0.0,0.0,100.0,0,53.2003,-2.8998,100.0
10007833,Wrexham Glyndŵr University,53,B,11,Computer Science and Informatics,,,,Environment,3.5,,30,0.0,0.0,0.0,75.0,25,53.0526,-3.0062,75.0
"""

# Use StringIO to simulate opening a file. In a real scenario, you would use open('path/to/file.csv').
# Read the CSV data into a DataFrame.
df = pd.read_csv(StringIO(csv_data))

# Divide the 'Score' by 100 for each record.
df['Score'] = df['Score'].apply(lambda x: x / 100)

# Save the modified DataFrame back to a CSV file. In a real scenario, you would use 'df.to_csv('path/to/output.csv')'.
# Here, we will just print it to the screen.
df.to_csv('../data/sorted_data.csv', index=False)
