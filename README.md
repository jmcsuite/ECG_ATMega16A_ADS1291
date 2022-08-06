# ECG_ATMega16A_ADS1291
Code to generate 1 lead ECG with the ATMega16A and a ADS1291 (and a bluetooth module or any serial connection)

An ECG is a way to measure electric impulses from the heart in order to detect anomalkies and diseases... More info on this topic is here https://www.ncbi.nlm.nih.gov/books/NBK536878/

This code is to generate 1 Lead ECGs using the Texas Instruments Chip ADS1291 https://www.ti.com/lit/ds/symlink/ads1292r.pdf?ts=1659697441166 an ATMega16A http://ww1.microchip.com/downloads/en/devicedoc/atmel-8154-8-bit-avr-atmega16a_datasheet.pdf and any computer with python and bluetooth.

THis works as following... using entries 1,2,3 from the ADS1291 connected to a person, the code generates an mp4 image of 10 seconds of measurements (repository includes examples). Additionally there is an extra project of machine learning inside this repo...it is related to the detection of R Peaks in ECG signals. This is done in Python using Hierirchal clustering, and the algorithm can be used to analyse the signal received from the microcontroller.

Any question you can directyly email me jmcsuite@hotmail.com
