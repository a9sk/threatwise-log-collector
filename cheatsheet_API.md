# CheatSheet for the API

## events/
- **events/search**, request events with a filter, in a specified format (JSON or STIX2). If the response has:
    - a packet capture (PCAP file), it will be indicated by the *x_trapx_com_pcap* flag;
    - binary files, it will be indicated by the *x_trapx_com_binary* flag.
- **events/show**, pass the *search_id* to request the eventss of a specific page;
- **events/download** is used to request of a specified file type (PCAP or binary), of a specified event (all files in the response's ZIP archive can be accessed with the password 'MALICIOUS');
- **events/cancel**, passing the *search_id* you can release cached results, and free the TSOC resources;
- **events/delete**, just delates security events from TSOC.

## appliance/
- **appliance/list**, list existing Appliances and Full OS traps and their details;
- **appliance/version**, obtain the software version and architecture;
- **appliance/initialize**, to initialize a newly-installed and setup Appliance or OS trap;
- **appliance/remove**, to remove an Appliance or full OS trap from the TSOC.

## interface/
- **interface/create**, creating a new virtual interface including all of its properties;
- **interface/configure**, to reconfigure an existing interface's changeable properties;
- **interface/list**, to list existing interfaces and tehir properties;
- **interface/remove**, to remove an interface;

## mwtrap/
- **mwtrap/create**, to enable a trap on an interafce;
- **mwtrap/clone**, to copy full configuration; 
- **mwtrap/configure**, apply a modified version of the configuration, to get an object you can modify use:
    - **mwtrap/current**, retrives the configuration of an existing configured trap;
    - **mwtrap/supported**, to retrive a list of emulation types supported from the Appliance;
    - **mwtrap/template**, to retrive a specific Appliance's configuration template;
- **mwtrap/remove**, to remove a trap from an interface.
- **mwtrap/list**, to list an Appliance's configured traps by their trap name;
- **mwtrap/interface**, to find interfaces on which are configured traps by their trap name;
- **mwtrap/trap**, to find trap names by sepcified interfaces.

## spindata/
- **spindata/enable** to allow FTP access;
- **spindata/disable** to block FTP access;
- **spindata/status** to check current FTP status.