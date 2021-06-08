Main (Run in this order):
1) DroneDataSync/DataSync.py
2) DroneRelativePosFix/PosFix.py
3) DroneCoordAvg/CoordAvg.py (optional)


1) DroneDataSync/DataSync.py - This script takes the drone logs and the receiver logs and syncs their data based on timestamps.
	To use: Rename drone logs to 'droneDat.csv' and rename receiver logs to 'sensorDat.csv'. Run DataSync.py

2) DroneRelativePosFix/PosFix.py - This script takes an input csv with columns "Timestamp,RSSI,Latitude,Longitude,Height" and a GPS position.
					It then calculates relative coordinates from the csv using the entered GPS position.
	To use: Execute 'PosFix.py <Latitude> <Longitude> <Input file> [Output file]' on the command line. "<...>" denote required, "[...]" denote optional.
		Note that the script only has a default value for the optional parameter, and as such will not run without those values being input.

3) DroneCoordAvg/CoordAvg.py - This script finds all RSSI values from the same GPS position and calculated the average RSSI value.
	To use: Execute 'CoordAvg.py <input file> <output file>' on the command line








Other:
1) DroneDataGenerator/DataGen.py
2) DroneDataGenerator/RandomRSSIDroneDat.py
3) DroneDataGenerator/DataGenGrid.py



1) DroneDataGenerator/DataGen.py - This script creates a specific number of randomized data points.
	To use: Execute 'DataGen.py [# of points]' on the command line. '[...]' denotes optional. Generates 'RandomGeneratedData.csv'
		[# of points] default = 10000

2) DroneDataGenerator/RandomRSSIDroneDat.py - This script was used to generate random RSSI values for all timestamps in the sample drone logs.
	To use: Execute the script. DO NOT DELETE 'droneDat.csv' FROM THIS DIRECTORY

3) DroneDataGenerator/DataGenGrid.py - This script was written to randomize points in a grid pattern. More closely represents our expected test plan.
	To use: Execute the script. Generates 'RandomGeneratedData2.csv'