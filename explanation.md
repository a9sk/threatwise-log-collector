# Threatwise

## Appliance

The main component is the Threatwise™'s Appliance, which hosts all of the traps and te NIS (Network Intelligence Sensor).
You can configure the Appliance to respond to intrusions/attacks based on your needs. 
The Appliance has to be somehow part of your network, connecting it to a Switch might as well do it.
For every single Appliance you can deploy maximum 512 traps on maximum 200 networks, if you want more than that (idk why you would but you never know), you'll need to deploy multiple Appliances.
For the NIS, you will need to connnect one interface to a network device such as a firewall.

## Full OS Traps

To have a more realistic interaction and attack monitoring, you might want to install a Full OS Trap on a full computer.
You can proxi the emulated services from emulation traps to a full OS trap, so the full OS trap's service will respond to the attacker, providing with better understanding of the attack.

## TSOC

The TSOC (ThreatWise Security Operations Console) manages OSs, Appliances and traps.
It serves a web user interface, through which you can administer the traps and monitor the events.
You can access all of this information via cloud in the TSOC's web interface.

## Deception Tokens

They are static records that should lure attackers to emulation traps, all of the communications between components will need to be secured.
If for any reason the deception tokens do not work, you paid for nothing.