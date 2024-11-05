import datatable
import numpy
#import time


# time start, for debug
#start_time = time.time()


def init_res_table():

      ################################################################
     #### 1. Construction of E24 table from 1.0 Ohms to 10 MOhms ####
    ################################################################

    serie=int(24)    #E24 series
    decades=int(7)   #from 1 Ohms to 10 MOhms
    total_size=int(serie*decades+1)



    #E24 values between 1 Ohms & 9.1 Ohms, time 10 to manage only integers
    starting_list = numpy.array([10,11,12,13,15,16,18,20,22,24,27,30,33,36,39,43,47,51,56,62,68,75,82,91],dtype='int16')


    #construction of the full set over 7 decades
    complete_list = numpy.empty(0,dtype='int16')

    for i in range(decades):
        for j in range(serie):
            complete_list=numpy.append(complete_list,starting_list[j]*pow(10,i))
            
    complete_list=numpy.append(complete_list,pow(10,decades+1))


      #############################################################################
     #### 2. Construction of numpy resistor table: triple nested loop => 1.4s ####
    #############################################################################

    # n° of combinations
    resTableSize=int(total_size*total_size*(total_size+1)/2)

    #direct fill of R2 column
    resTableR2 = numpy.repeat(complete_list,total_size*(total_size+1)/2)/10.0

    # initialization of columns
    resTableR1_a = numpy.empty([resTableSize],dtype='int16')
    resTableR1_b = numpy.empty([resTableSize],dtype='int16')

    # loop to fill-in index (from 0 to total_size-1)
    resTableIndex=int(0)

    for i in range(total_size):         
        for j in range(total_size):     #R1_a loop 
            for k in range(j+1):        #R1_b loop (R1_b <= R1_a)
                resTableR1_a[resTableIndex]=j
                resTableR1_b[resTableIndex]=k
                resTableIndex+=1         

    # conversion from index to resistances values
    resTableR1_a = complete_list[resTableR1_a]/10.0
    resTableR1_b = complete_list[resTableR1_b]/10.0


    # time end, for debug
    #end_time = time.time()
    #print(end_time-start_time)





    myData = datatable.Frame(R2=resTableR2,R1_a=resTableR1_a,R1_b=resTableR1_b)

    return myData

