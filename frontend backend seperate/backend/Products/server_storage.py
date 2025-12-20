server_storage_products = [


#  SUPERMICRO SERVER


{
  "id": "mbd-supermicro-x13sae",
  "name": "Supermicro X13SAE Motherboard",
  "brand": "supermicro",
  "category_key": "server-storage",
  "category": "Server & Workstation Motherboard",
  "sub_category": "supermicro",
  "series": "motherboards",
  "application": "Workstation / Server / Enterprise PC",
  "status": "New",
  "description": "ATX motherboard based on Intel W680 chipset supporting 12th, 13th, and 14th Gen Intel Core processors, DDR5 memory, dual LAN, and multiple PCIe & M.2 expansion options.",

  "processor": "Socket V (LGA 1700) | Supports 12th / 13th / 14th Gen Intel Core i3/i5/i7/i9 | Up to 24 cores | Up to 150W TDP",

  "memory": "4 × DDR5 UDIMM slots | Up to 192 GB | Up to 4400 MT/s | Supported sizes: 8 GB / 16 GB / 24 GB / 32 GB / 48 GB",

  "chipset": "Intel W680",

  "storage": "8 × SATA 6Gb/s (RAID 0/1/5/10) | 3 × M.2 PCIe 4.0 x4 (M-Key 2280)",

  "network": "1 × 2.5 GbE (Intel i225V) + 1 × 1 GbE (Intel I219LM)",

  "ports": "USB 3.2 Gen2 / Gen1 / USB-C / USB 2.0 | DisplayPort | HDMI 2.0b | DVI-D | HD Audio (ALC888S)",

  "expansion": "2 × PCIe 5.0 x16 | 2 × PCIe 3.0 x4",

  "form_factor": "ATX (12 × 9.6 inches)",
  "image": "/static/images/SERVER2.webp",
  "price": 71313
},



{
  "id": "srv-supermicro-2024-2u-gpu",
  "name": "Supermicro 2024 2U GPU Server",
  "brand": "supermicro",
  "category_key": "server-storage",
  "category": "2U GPU Server",
  "sub_category": "supermicro",
  "series": "gpu-server",
  "application": "AI / Machine Learning / HPC / Enterprise",
  "description": "High-performance Supermicro 2024 2U GPU server with dual processors, scalable memory, multi-GPU support, and enterprise-class storage networking.",

  "status": "New",
  "processor": "Dual AMD EPYC 9004 / 7003 Series or Dual Intel Xeon Scalable (dependent on configuration)",
  
  "memory": "Up to 32 DDR5 ECC DIMM slots | Up to multiple terabytes (configurable)",
  
  "gpu_support": "Up to 4 x double-width or 8 x single-width GPUs (PCIe 4.0/5.0) depending on chassis and riser configuration",
  
  "storage": "Up to 24 × 2.5\" hot-swap NVMe/SATA/SAS drive bays | M.2 boot options",
  
  "network": "Multiple 10G/25G/100G Ethernet options via AIOM/OCP modules | Optional RDMA",
  
  "cooling": "Redundant high-static pressure server fans with optimized thermal design for GPUs",
  
  "power": "Dual hot-swap redundant power supplies (1600W+ Titanium level available)",
  
  "form_factor": "2U Rackmount",
  "image": "/static/images/SERVER2.webp",
  "price": 459990
},


{
  "id": "chassis-supermicro-ultra-4u",
  "name": "Supermicro Ultra 4U Chassis",
  "brand": "supermicro",
  "category_key": "server-storage",
  "category": "4U Rackmount Chassis",
  "sub_category": "supermicro",
  "series": "ultra-chassis",
  "application": "Enterprise Server / Storage / GPU Compute",
  "description": "Supermicro Ultra 4U rack chassis supporting dual processors, flexible storage configurations, and high-density expansion for enterprise or GPU workloads.",

  "status": "New",
  "processor_support": "Dual Intel Xeon Scalable or Dual AMD EPYC (dependent on motherboard choice)",
  
  "memory_support": "Up to 32 DDR5 ECC DIMM slots | Supports high density memory configurations",
  
  "drive_bays": "Up to 24 × 2.5\" hot-swap NVMe/SATA/SAS or 12 × 3.5\" LFF with RAID support",
  
  "network": "Flexible networking options via OCP 3.0 / AIOM modules supporting 10G/25G/100G+",
  
  "expansion_slots": "Multiple PCIe 4.0/5.0 x16 slots for GPUs, NICs and RAID cards",
  
  "cooling": "Front hot-swap fans with optimized airflow for heavy GPU and CPU components",
  
  "power": "Dual redundant power supplies (1600W+ Titanium level optional)",
  
  "form_factor": "4U Rackmount",
  "image": "/static/images/supermicro_ultra_4u_chassis.jpg",
  "price": 239990
},



# ASUS WORKSTATION

{
  "id": "srv-asus-rs700-rack",
  "name": "ASUS RS700 Rack Server",
  "brand": "asus",
  "category_key": "server-storage",
  "category": "Rack Server",
  "sub_category": "asus",
  "series": "server-barebone",
  "application": "Enterprise / Data Center / Virtualization",
  "description": "ASUS RS700 full-height 2U enterprise rack server platform designed for high uptime, large memory capacity, and flexible storage options for mission-critical workloads.",

  "status": "New",
  "processor": "Dual Intel Xeon Scalable Processors (3rd/4th Gen) supporting up to 40+ cores per socket",

  "memory": "16 DDR5 ECC RDIMM slots | Up to 4 TB DDR5 ECC memory",

  "storage": "8 × 2.5\" hot-swap SATA/SAS + optional NVMe backplane support",

  "network": "Dual 10GbE integrated + optional 25GbE / 100GbE NIC options",

  "raid": "Supports 12Gb/s hardware RAID (0/1/5/10/50/60)",

  "expansion": "Up to 7 × PCIe 4.0 x16 slots",

  "power": "Redundant 1600W Titanium Level PSUs",

  "form_factor": "2U Rackmount",
  "image": "/static/images/asus_rs700_rack.jpg",
  "price": 359990
},
{
  "id": "srv-asus-esc4000-g4",
  "name": "ASUS ESC4000 G4",
  "brand": "asus",
  "category_key": "server-storage",
  "category": "GPU Server",
  "sub_category": "asus",
  "series": "gpu-systems",
  "application": "AI / Deep Learning / HPC / GPU Compute",
  "description": "ASUS ESC4000 G4 GPU-optimized 4U rack server with support for multiple GPUs, dual CPUs, and high throughput storage for AI and HPC workloads.",

  "status": "New",
  "processor": "Dual Intel Xeon Scalable Processors (Cascade/Cooper Lake) supporting up to 28+ cores per socket",

  "memory": "32 DDR4 ECC RDIMM slots | Up to 8 TB memory support",

  "gpu_support": "Up to 8 × single-width GPUs (NVIDIA A100 / H100 class support depending on configuration)",

  "storage": "8 × 2.5\" hot-swap + 4 × rear NVMe mezzanine",

  "network": "OCP 3.0 / Dual 10GbE integrated with optional 25/40/100GbE",

  "cooling": "Optimized GPU airflow with high-capacity redundant fans",

  "power": "2 × Redundant 2000W Titanium PSUs",

  "form_factor": "4U Rackmount",
  "image": "/static/images/asus_esc4000_g4.jpg",
  "price": 679990
},






#  LENOVO SERVER

{
  "id": "srv-lenovo-thinksystem-sr650",
  "name": "Lenovo ThinkSystem SR650",
  "brand": "lenovo",
  "category_key": "server-storage",
  "category": "2U Rack Server",
  "sub_category": "lenovo",
  "series": "thinksystem",
  "application": "Enterprise / Virtualization / Database / AI Inference",
  "description": "Lenovo ThinkSystem SR650 is a versatile 2U rack server designed for enterprise workloads, virtualization, and database environments with up to dual processors and scalable memory.",
  
  "status": "New",
  "processor": "Up to Dual Intel Xeon Scalable 3rd/4th Gen processors (up to 40+ cores per socket)",

  "memory": "Up to 32 DDR5 ECC DIMM slots | Up to 4 TB capacity",

  "storage": "Support for up to 10 × 2.5\" hot-swap NVMe/SATA/SAS drives | Optional rear drive cage",

  "network": "Integrated 1GbE / 10GbE options | Optional 25GbE / 100GbE adapters",

  "raid": "Hardware RAID support (0/1/5/10/50/60)",

  "expansion": "Up to 7 PCIe 4.0 x16 slots (GPU/accelerator ready)",

  "power": "Redundant hot-swap PSUs (up to 1600W Platinum)",

  "form_factor": "2U Rackmount",
  "image": "/static/images/lenovo_thinksystem_sr650.jpg",
  "price": 329990
},


{
  "id": "srv-lenovo-thinksystem-st550",
  "name": "Lenovo ThinkSystem ST550",
  "brand": "lenovo",
  "category_key": "server-storage",
  "category": "Tower Server",
  "sub_category": "lenovo",
  "series": "thinksystem",
  "application": "Small Business / Edge / Enterprise Applications",
  "description": "Lenovo ThinkSystem ST550 is a powerful tower server ideal for small and medium enterprises, edge deployments, and business critical workloads with flexible expansion and high reliability.",
  
  "status": "New",
  "processor": "Up to Dual Intel Xeon Scalable 3rd/4th Gen processors (up to 40+ cores per socket)",

  "memory": "Up to 16 DDR5 ECC DIMM slots | Up to 2 TB capacity",

  "storage": "Up to 8 × 3.5\" hot-swap SATA/SAS or 16 × 2.5\" drives (mixed configs supported)",

  "network": "Integrated 2 × 10GbE ports | Optional 25GbE / 100GbE adapters",

  "raid": "Hardware RAID support (0/1/5/10/50/60)",

  "expansion": "PCIe 4.0 slots for GPU/NIC/RAID adapters",

  "power": "Redundant optional power supplies",

  "form_factor": "Tower / Rack convertible",
  "image": "/static/images/lenovo_thinksystem_st550.jpg",
  "price": 199990
}



]
