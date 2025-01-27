from LDMX.Framework import ldmxcfg
p=ldmxcfg.Process("neutron")
p.libraries.append("libSimCore.so")
p.libraries.append("libHcal.so")
p.libraries.append("libEcal.so")

import argparse, sys
parser = argparse.ArgumentParser(f'ldmx fire {sys.argv[0]}')
parser.add_argument('energy',type=float)
arg = parser.parse_args()

nevents = 500 # number of events
energy = arg.energy

from LDMX.SimCore import simulator
from LDMX.SimCore import generators
sim = simulator.simulator("single_neutron")
sim.setDetector( 'ldmx-det-v12' , True )
p.run = 0
sim.description = "HCal neutron"
sim.beamSpotSmear = [20., 80., 0.] #mm
particle_gun = generators.gun( "single_neutron_upstream_hcal")
particle_gun.particle = 'neutron'
# position = 870.
position = 690.6 # back hcal
# position = 240.4 # ecal face
particle_gun.position = [ 0., 0., position ]  # mm
particle_gun.direction = [ 0., 0., 1]
particle_gun.energy = energy
myGen = particle_gun
print(myGen)
sim.generators.append(myGen)

p.outputFiles=['data/ngun_%.2fmm_%.2f_gev.root'%(position,energy)]
p.maxEvents = nevents
p.logFrequency = 100

p.sequence=[sim]

import LDMX.Ecal.digi as ecal_digi
import LDMX.Hcal.digi as hcal_digi

from LDMX.Ecal import EcalGeometry
geom = EcalGeometry.EcalGeometryProvider.getInstance()

from LDMX.Hcal import HcalGeometry
geom = HcalGeometry.HcalGeometryProvider.getInstance()

import LDMX.Hcal.hcal_hardcoded_conditions
digit = hcal_digi.HcalDigiProducer()
recon = hcal_digi.HcalRecProducer()

import LDMX.Ecal.ecal_hardcoded_conditions
p.sequence.extend([
    ecal_digi.EcalDigiProducer(),
    ecal_digi.EcalRecProducer(),
    digit,recon
])

