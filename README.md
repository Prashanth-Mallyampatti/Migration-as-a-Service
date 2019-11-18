# Migration-as-a-Service

## ABSTRACT

Being aware of the need for migration services in any cloud-based solutions and the understanding of migration services provided by different cloud vendors, our project aims to provide migration as a service in a multi-cloud environment offering instance and subnet migrations across multiple clouds. The migration of instances involves moving of user-specified VMs from one cloud to another within the same subnet. The migration of subnets involves moving of user-specified subnet and all the VMs within the same subnet from one cloud to another.

The migration of instances and subnets constitute the functional features of our project. Additional features must be added to make our service a marketable solution. Management features would operate on top of the core services and provide various aspects of cloud computing. Some of them include Fault management, configuration, accounting level, performance level, and security management. Our project aims to provide configuration and accounting management features. There are three ways to provide configuration management features, namely - CLI, API, and GUI. Our project incorporates CLI method to receive inputs from tenants to build the infrastructure and migrate instances and/or subnets. Thorough logging of user and system events offer accounting features. We have incorporated three levels of accounting - INFO, ERROR, and WARNING. There is a clear demarcation of user-visible and system logs that track the entire service. This feature enables efficient debugging of the service. With these management features, we believe that our Migration-as-a-Service would enable us to target a wide range of stakeholders in cloud computing domains.


## SYSTEM DESIGN

The system emulates a model-based controller similar to open Daylight. The model controller architecture provides two models, namely - data and configuration models. The system comprises 3 major components - Northbound, Logical Component, and Southbound.

### The model supports the following CRUD operations:
1. Create, update and delete tenant
2. Create, update and delete network
3. Create, update and delete an instance
4. Create, update and delete DNS/DHCP  

### The data models for the above objects are as follows:
1. Tenant: { name }
2. Network: { native cloud, subnet address }
3. Instance: { name, disk-size (GB), memory (GB), number of vCPUs }
4. DNS/DHCP Server: { tenant subnet address }

The tenant enters these details through file edit operation similar to libvirt. The tenant provides a YAML file with all the requirements. This structure forms the Northbound component of the system.

The Southbound component is responsible for creating the necessary infrastructure and communicates with the cloud/hypervisors. This component consists of shell scripts, python scripts, and Ansible playbooks. These enable ssh communication among multiple clouds and also create the master<->worker node correlation. This component is independent of any logic.

The process of translating tenant requirements into commands to create the infrastructure needs some logic and intelligence. 
### The logical component encapsulates this intelligence and is responsible for the following:
1. Validation of tenant input
2. Parsing of tenant input
3. The population of files provided as inputs to Ansible playbooks
4. Identify and create tunneling infrastructure
5. Event handling
6. Identify migration requirements
7. Migration logic

The runtime system model maintains the state of the system at any given point in time and is a superset of the configuration model. The accounting feature of our project provides specifics about the runtime model in terms of event handling and infrastructure state.

## EXECUTION
Run ```python Migration-as-a-Service/infra_init.py``` in a terminal
Run ```python Migration-as-a-Service/mig_init.py``` in another terminal

To requst for infrastructure: Create/Update/Delete yaml config files per tenant in Migration-as-a Service/ansible/config_files/infrastructure

To requst for infrastructure: Create/Update/Delete yaml config files per tenant in Migration-as-a-Service/ansible/config_files/migration

Logs are at Migration-as-a-Service/logs
