from firebase import firebase  
import pprint
import mysql.connector

#---------------READ THIS-----------------------------------
# There is a mistake in this code, the tools are misllabled
# cachestat_data_ms = [] AND cachestat_data_IO = [] is actually from IO_LATENCY TOOL
# io_latency_data = [] is actually from CACHESTAT tool
#-----------------------------------------------------------

# setting up prettyPrint: because the o/p is messy
pp = pprint.PrettyPrinter(indent=4)

# creating the connection
fb = firebase.FirebaseApplication('https://cdac-argus-default-rtdb.firebaseio.com/', None)  
result = fb.get('cdac-argus-default-rtdb/metrics', None)

# seperating data
cachestat_data_ms = []
cachestat_data_IO = [] 

# this is seperated from source so no need to seperate
io_latency_data = []

def get_data():
    for val in result.values():

        # easiest way to get the values since firebase adds its own key
        # nesting(complicating) the already awful dict structure
        metrics = (list(val.values()))

        # extracting metrics
        if (metrics[0].startswith("ms_range")):
            # cachestat_data.append(metrics[0])
            ms_range_metrics, IO_metrics = metrics[0].split("IO", 1)

            # A very hacky fix to remove ms_range attached to the list so the EVAL() works in the code beneath 
            garbage, ms_range_metrics = ms_range_metrics.split("ms_range")
            
            # storing cleaned and sorted data
            cachestat_data_ms.append(eval(ms_range_metrics))
            cachestat_data_IO.append(eval(IO_metrics))

        elif (metrics[0].startswith("{")):

            # storing cleaned and sorted data
            io_latency_data_cleaned = eval(metrics[0])
            io_latency_data.append(io_latency_data_cleaned)

    

    # print("-------------------------------------------------")
    # print("IO_LATENCY MS_RANGE DATA")
    # print("-------------------------------------------------")
    # pp.pprint(cachestat_data_ms)

    # print("-------------------------------------------------")
    # print("IO_LATENCY IO DATA")
    # print("-------------------------------------------------")
    # pp.pprint(cachestat_data_IO)

    # print("-------------------------------------------------")
    # print("CACHESTAT DATA")
    # print("-------------------------------------------------")
    # pp.pprint(io_latency_data)

get_data()

local_mysql_db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "12345",
        database = "cdac_argus"
    )

mycursor = local_mysql_db.cursor()

def insert_data_cachestat_mysql(values):
    query = "INSERT INTO cachestat (hits, misses, mbd, ratio, buffers_mb, cached_mb) VALUES (%s,%s,%s,%s,%s,%s)"
    # values = (65,1347,21502,27,0,100)

    mycursor.execute(query,values)
    local_mysql_db.commit()


# insert_data_cachestat_mysql()

# print(io_latency_data)

def print_data_mysql():
    query = "SELECT * FROM cachestat"
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    print(myresult)


for _ in io_latency_data:
    # clearing the list
    val_list = []

    for key, val in _.items():
        val_list.append(val)

    # directly inserting values into the mysql
    insert_data_cachestat_mysql(tuple(val_list)) 

#--------------------------------------------------------------
# MYSQL cachestat table (form argus_cdac database) -> structure
# CREATE TABLE cachestat( metric_id INT NOT NULL AUTO_INCREMENT, buffers_mb INT NOT NULL, cached_mb INT NOT NULL, hits INT NOT NULL, mbd INT NOT NULL, misses INT NOT NULL, ratio INT NOT NULL, PRIMARY KEY ( metric_id ) );
#--------------------------------------------------------------


# JSON STRUCTURE - DATABASE OUTLINE -> FOR BETTER UNDERSTANDING ON HOW THIS CODE WORKS

# {
#   "cdac-argus-default-rtdb" : {
#     "metrics" : {
#       "-MR3hEfRZF92DgLdvndf" : {
#         "2021-01-15_11:52:11dot701928" : "ms_range[('0', '1')]IO['16']"
#       },
#       "-MR3hjzQ_Ir5-c9Rd60_" : {
#         "2021-01-15_11:54:19dot081534" : "ms_range[('0', '1'), ('1', '2')]IO['19', '8']"
#       },
#       "-MR3hqGyZ6cJbLJA1kke" : {
#         "2021-01-15_11:54:44dot772003" : "ms_range[('0', '1')]IO['4']"
#       },
#       "-MR3hupcL_2tSM2IIOLm" : {
#         "2021-01-15_11:55:03dot501919" : "ms_range[('0', '1'), ('1', '2'), ('2', '4'), ('4', '8'), ('8', '16'), ('16', '32')]IO['3', '0', '0', '0', '0', '1']"
#       },
#       "-MR3jDs2R6T7Y6LYYki4" : {
#         "2021-01-15_12:00:52dot594892" : "{'hits': '21502', 'misses': '0', 'mbd': '27', 'ratio': '100', 'buffers_mb': '82', 'cached_mb': '1347'}"
#       },
#       "-MR3jF3j2dM_JwcNIlQx" : {
#         "2021-01-15_12:00:57dot625313" : "{'hits': '26084', 'misses': '0', 'mbd': '36', 'ratio': '100', 'buffers_mb': '82', 'cached_mb': '1344'}"
#       },
#       "-MR3jGI5BS6GQe0AYjAy" : {
#         "2021-01-15_12:01:02dot644831" : "{'hits': '18797', 'misses': '0', 'mbd': '12', 'ratio': '100', 'buffers_mb': '82', 'cached_mb': '1341'}"
#       }
#     }
#   }
# }
