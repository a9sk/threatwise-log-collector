# TSOC API

## Intro

The TSOC has a REST API that enables developing client scripts for integrating Threatwise with whatever thing you might want to integrate it into.

NOTE: This file only gives an overview of the calls that can be done to gather informations and manage th "High-Level Tasks" using the API. For a more compact understanding of the API Call Reference, visit this other [file](cheatsheet_API.md).

## Overview

### Call and Response Structure

The TSOC accepts calls at per-resource URLs. 
To obtain the address you should open the browser bar, copy the address and make some changes:
- before the first dot, add -apl
- exclude anything after .metallic.io
- after .metallic.io, add /api/v<version>/<resource>

You can also use the provided [script](address.py) to generate the address.

All tasks are performed via HTTP POST calls, even for retrivals.
Both the request payloads and responses are in JSON format.
Every call must include the TSOC's API key, in an *api_key* field.
The API key can be obtained from Commvault Cloud support.

### Asynchronous Calls

Most calls are blocking, however some calls, called asynchronous, send a response immediatly and a subsequent call can query for the task's status.
The response to the initial call includes a *request_id*, to be specified in the status queries.
All of the subsequent responses include the *request_id*.
To query for status, call async/status with the specific *request_id*, to cancel a task, call async/cancel and specify the *request_id*.

## High-Level tasks

There are five main security events you can use:
- **events/search**, request events with a filter, in a specified format (JSON or STIX2). If the response has:
    - a packet capture (PCAP file), it will be indicated by the *x_trapx_com_pcap* flag;
    - binary files, it will be indicated by the *x_trapx_com_binary* flag.
- **events/show**, pass the *search_id* to request the events of a specific page;
- **events/download** is used to request a specified file type (PCAP or binary), of a specified event (all files in the response's ZIP archive can be accessed with the password 'MALICIOUS');
- **events/cancel**, passing the *search_id* you can release cached results, and free the TSOC resources;
- **events/delete**, just delates security events from TSOC.

## Whitelisting Events

It is possible to manage event exceptions.

## Working with Appliances

You can manage Appliances and obtain information to use for managing networking.
In API calls you can referr to an Appliance by its *gid* (group ID) and its *uid* (unique ID).

On Appliances you can perform four different types of tasks:
- **appliance/list**, lists existing Appliances and Full OS traps with their details;
- **appliance/version**, obtain the software version and architecture;
- **appliance/initialize**, to initialize a newly-installed and setup Appliance or OS trap;
- **appliance/remove**, to remove an Appliance or Full OS trap from the TSOC.

## Network Interfaces for Traps

You can work with physical interfaces, subinterfaces, VLANs and VLANs' aliases.

The five tasks you can perform with interfaces are:
- **interface/create**, creating a new virtual interface including all of its properties;
- **interface/configure**, to reconfigure an existing interface's changeable properties;
- **interface/list**, to list existing interfaces and their properties;
- **interface/remove**, to remove an interface;
- **mwtrap/interface** to retrive interface names by their trap names.

## Emulation Traps

You can manage emulation traps on configured interfaces, one interface can only have a single emulation trap.
The trap uses a JSON object for the configuration, which includes the interface name, and emulation details (type, OS version, services and configurations).

The different operations you can do with emulated traps are:
- **mwtrap/create**, to enable a trap on an interafce;
- **mwtrap/clone**, to copy Full configuration; 
- **mwtrap/configure**, apply a modified version of the configuration, to get an object you can modify use:
    - **mwtrap/current**, retrives the configuration of an existing configured trap;
    - **mwtrap/supported**, to retrive a list of emulation types supported from the Appliance;
    - **mwtrap/template**, to retrive a specific Appliance's configuration template;
- **mwtrap/remove**, to remove a trap from an interface.

Configuration field values that are files must all be base64 encoded.

To be able to subsequently upload spin data for a relevant service of an emulation trap, use:
- **spindata/enable** to allow FTP access;
- **spindata/disable** to block FTP access;
- **spindata/status** to check current FTP status.

To gather informations or manage the traps you can use:
- **mwtrap/list**, to list an Appliance's configured traps by their trap name;
- **mwtrap/interface**, to find interfaces on which are configured traps by their trap name;
- **mwtrap/trap**, to find trap names by specified interfaces.

## Custom Emulation Types

It is possible to customize your emulation types, creating new emulations.
Templates for customization include a *base_operating_system_type* field and a customizable OS fingerprint field.
To obtain templates for customization use:
- **mwtrap/custom_templates**, then customize with:
    - change the *operating_system_type* to a better name;
    - set the OS fingerprint to a relevant one as defined in the [Nmap database](https://nmap.org/book/nmap-os-db.html);
    - set the options for OS version, hostname, domain, and services.

To manage the customizeed emulation types you can use:
- **mwtrap/custom_create**, to make it available for trap creation;
- **mwtrap/custom_delete**, to remove it.

## Deception Tokens

You can manage Deception Token assignment to campaigns.
All of the tokens have a token ID numer, you can retrive the details of a trap's token via per-trap token types and ID number.

## Full Linux OS

You can manage an Appliance's Full Linux OS for high-interaction SSH, the Full Linux OS can be enabled, disabled, or you can also query when it is enabled.
You can revert it to its original state. You can manage its credentials list by retrieving the current list or setting the list.

### Disclaimer

All of the information above is from the Commvault Cloud Threatwise™ TSOC guide for the REST API developing.