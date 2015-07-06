#!/usr/bin/python
import sys
import matplotlib.pyplot as plt


class parameter_parse(object):
    def __init__(self, parameters):
        # strain 1
        self.strain1_vmax = parameters[0]
        self.strain1_km = parameters[1]
        self.strain1_yield = parameters[2]
        self.strain1_starting = parameters[3]

        # strain 2

        self.strain2_vmax = parameters[4]
        self.strain2_km = parameters[5]
        self.strain2_yield = parameters[6]
        self.strain2_starting = parameters[7]

        # starting conditions

        self.flow_rate = parameters[8]
        self.volume = parameters[9]
        self.endtime = int(parameters[10])
        self.substrate_media = parameters[11]
        self.substrate_init = parameters[12]

###reading in starting parameters

parameters = list()

with open(sys.argv[1]) as param_file:
    for param in param_file:
        
        param = param.replace("\n" , "")

        if param[0] == "#":
            continue
        parameters.append(param.split(":")[1])

parameters = map(float, parameters)

sim_param = parameter_parse(parameters)

dilution=sim_param.flow_rate/sim_param.volume

###creating file for output

prop_out = open("simulation_results.tsv","w")
prop_out.write("Time\tNutr\tStrain1\tStrain2\tProp")

substrate = sim_param.substrate_init

strain1 = sim_param.strain1_starting
strain2 = sim_param.strain2_starting

### looping through simulation
plot_minutes = list()
plot_prop = list()

for minutes in range(0,sim_param.endtime):
    #print minutes
    

    if minutes < 10000:
        
        #calculating the change in nutrients
        nutr_flux = dilution*(sim_param.substrate_media-substrate) - (strain1/sim_param.strain1_yield)*((sim_param.strain1_vmax*substrate)/(sim_param.strain1_km+substrate))
        strain1_flux = ((sim_param.strain1_vmax*substrate)/(sim_param.strain1_km+substrate)-dilution)*strain1
        
    
        #recalculating substrate and strain1 count

        substrate = substrate+nutr_flux
        strain1 = strain1+strain1_flux

        if str(int(minutes)/int(250)).isdigit() == True:
            
            plot_minutes.append(minutes)
            plot_prop.append(0)

            prop_out.write(str(minutes) + "\t" + str(substrate) + "\t" + str(strain1) + "\t" + "0" + "\t0\n")

        continue

    if minutes >= 10000:
        #calculating the change in nutrients after 2 strains

        nutr_flux = dilution*(sim_param.substrate_media-substrate) - (strain1/sim_param.strain1_yield)*((sim_param.strain1_vmax*substrate)/(sim_param.strain1_km+substrate)) - (strain2/sim_param.strain2_yield)*((sim_param.strain2_vmax*substrate)/(sim_param.strain2_km+substrate))
        strain1_flux = ((sim_param.strain1_vmax*substrate)/(sim_param.strain1_km+substrate)-dilution)*strain1
        strain2_flux = ((sim_param.strain2_vmax*substrate)/(sim_param.strain2_km+substrate)-dilution)*strain2

    
        #recalculating substrate and strain1 count

        substrate = substrate+nutr_flux
        strain1 = strain1+strain1_flux
        strain2 = strain2+strain2_flux

        if str(minutes/250).isdigit() == True:
            proportion = strain2/(strain1+strain2)

            prop_out.write(str(minutes) + "\t" + str(substrate) + "\t" + str(strain1) + "\t" + str(strain2) + "\t" + str(proportion) + "\n")
            
            plot_minutes.append(minutes)
            plot_prop.append(proportion)

        continue


prop_out.close()

plt.plot(plot_minutes, plot_prop)
plt.show()



