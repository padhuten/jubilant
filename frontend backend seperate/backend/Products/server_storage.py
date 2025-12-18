server_storage_products = [


#  SUPERMICRO SERVER


{
  "id": "mbd-supermicro-x13sae",
  "name": "Supermicro X13SAE Motherboard",
  "brand": "Supermicro",
  "category_key": "server-storage",
  "category": "Server & Workstation Motherboard",
  "sub_category": "supermicro",
  "series": "motherboards",
  "application": "Workstation / Server / Enterprise PC",
  "description": "ATX motherboard based on Intel W680 chipset supporting 12th, 13th, and 14th Gen Intel Core processors, DDR5 memory, dual LAN, and multiple PCIe & M.2 expansion options.",
  
  "processor": {
    "socket": "Socket V0",
    "supported_cpus": "12th/13th/14th Gen Intel Core i3/i5/i7/i9",
    "max_cores": "Up to 24 cores",
    "tdp_support": "Up to 150W TDP"
  },

  "memory": {
    "slots": 4,
    "type": "DDR5 UDIMM",
    "max_capacity": "192 GB",
    "max_speed": "4400 MT/s",
    "supported_sizes": ["8 GB", "16 GB", "24 GB", "32 GB", "48 GB"]
  },

  "chipset": "Intel W680",

  "storage": {
    "sata": "8 × SATA 6Gb/s with RAID 0/1/5/10",
    "m2": "3 × M.2 PCIe 4.0 x4 (M-Key 2280)"
  },

  "network": {
    "lan": [
      "1 × 2.5 GbE (Intel i225V)",
      "1 × 1 GbE (Intel I219LM)"
    ]
  },

  "ports": {
    "usb": "USB 3.2 Gen2, Gen1, USB-C, USB 2.0 (rear + headers)",
    "display": "DisplayPort, HDMI 2.0b, DVI-D",
    "audio": "ALC888S HD Audio"
  },

  "expansion": {
    "pcie": [
      "2 × PCIe 5.0 x16",
      "2 × PCIe 3.0 x4"
    ]
  },

  "form_factor": "ATX (12 × 9.6 inches)",
  "image": "/static/images/SERVER2.webp",
  "price": 71313
},


{
  "id": "server-supermicro-2024-2u-gpu",
  "name": "Supermicro 2024 2U GPU Server",
  "brand": "Supermicro",
  "series": "gpu-server",
  "category_key": "server",
  "sub_category": "super-micro",
  "category": "High-Performance GPU Server",
  "application": "AI / Machine Learning / Deep Learning / HPC / Data Center",
  "description": "Powerful 2U rackmount GPU server supporting next-generation NVIDIA GPUs, dual 5th/4th Gen Intel Xeon Scalable processors, PCIe Gen5, and high-bandwidth networking — designed for AI training, inference, HPC, cloud, and enterprise GPU workloads.",

  "processor": {
    "socket": "Dual Socket E (LGA 4677)",
    "supported_cpus": "4th & 5th Gen Intel Xeon Scalable (Sapphire Rapids / Emerald Rapids)",
    "max_cores": "Up to 64 cores per CPU (128 cores total)",
    "tdp_support": "Up to 350W TDP depending on model"
  },

  "memory": {
    "slots": 32,
    "type": "DDR5 RDIMM",
    "max_capacity": "Up to 4 TB (with 128GB RDIMMs)",
    "max_speed": "Up to 5600 MT/s"
  },

  "chipset": "Intel C741 or proprietary Supermicro GPU-server platform (model-dependent)",

  "storage": {
    "nvme": "Up to 8 × NVMe Gen4/Gen5 bays (U.2 / E1.S depending on SKU)",
    "sata": "Optional 2.5\"/3.5\" SATA drive bays"
  },

  "network": {
    "lan": [
      "2 × 10GbE or 25GbE onboard NIC (varies by model)",
      "Optional OCP 3.0 card for 100/200/400GbE networking"
    ]
  },

  "gpu_support": {
    "max_gpus": "Up to 4 × Double-width GPUs",
    "supported_gpus": [
      "NVIDIA H100 PCIe",
      "NVIDIA L40S",
      "NVIDIA A100 PCIe",
      "NVIDIA RTX 6000 Ada"
    ],
    "interconnect": "PCIe Gen5 (x16 lanes per GPU)"
  },

  "expansion": {
    "pcie": [
      "Up to 6 × PCIe 5.0 x16 full-height slots",
      "OCP 3.0 networking slot"
    ]
  },

  "power_supply": {
    "redundant_psu": "2 × 2000W Titanium Level (1+1 Redundant)",
    "input": "100–240V AC"
  },

  "form_factor": "2U Rackmount Server",
  "image": "/static/images/SERVER2.webp",
  "price": 436000
},

{
  "id": "chassis-supermicro-ultra-4u",
  "name": "Supermicro Ultra 4U Chassis",
  "brand": "Supermicro",
  "series": "barebone",
  "category_key": "server",
  "sub_category": "super-micro",
  "category": "4U High-Performance Server Chassis",
  "application": "Enterprise Server / Data Center / Storage / Multi-GPU / Virtualization",
  "description": "4U server chassis from Supermicro’s Ultra series supporting high-performance servers, multiple PCIe expansion cards, redundant power supplies, advanced cooling, and large drive capacity. Ideal for enterprise workloads, storage servers, and multi-GPU configurations.",

  "processor": {
    "socket": "Depends on installed Ultra motherboard (supports Xeon Scalable platforms)",
    "supported_cpus": "Intel Xeon Scalable (varies by chassis + motherboard combo)",
    "max_cores": "Up to 64 cores per CPU (model-specific)",
    "tdp_support": "Up to 350W depending on cooling and CPU"
  },

  "chipset": "Depends on installed Ultra motherboard",

  "storage": {
    "drive_bays": "Up to 24 × 3.5\" or 36 × 2.5\" hot-swap drive bays (SAS/SATA/NVMe depending on model)",
    "backplane": "SAS3 / SATA / NVMe hybrid backplanes available"
  },

  "network": {
    "lan": "Networking depends on installed Ultra motherboard (1GbE / 10GbE / 25GbE options)"
  },

  "ports": {
    "usb": "Front & rear USB 3.0/3.2 ports (varies by model)",
    "display": "Video output via installed motherboard (VGA or HDMI)",
  },

  "expansion": {
    "pcie": "Supports multiple PCIe Gen4/Gen5 slots — ideal for storage controllers, GPUs, NICs"
  },

  "power_supply": {
    "redundant_psu": "Dual 1600W or 2000W Platinum/Titanium level PSUs",
    "cooling": "High-performance fans optimized for heavy server loads"
  },

  "form_factor": "4U Rackmount Chassis",
  "image": "/static/images/barebones.jpg",
  "price": 175000
},



# ASUS WORKSTATION

{
  "id": "server-asus-rs700-e11-rs12u",
  "name": "ASUS RS700 Rack Server",
  "brand": "ASUS",
  "category_key": "server",
  "sub_category": "asus",
  "series": "rack-server",
  "application": "Data Center / Virtualization / AI / HPC / Storage",
  "description": "1U enterprise rack server with dual Intel Xeon Scalable processors, up to 32 DIMMs DDR5 ECC memory, multiple NVMe hot-swap bays, flexible PCIe expansion, and optional GPU support — designed for high performance computing, storage and virtualization workloads.",

  "processor": {
    "socket": "Dual LGA 4677 sockets",
    "supported_cpus": "4th/5th Gen Intel Xeon Scalable processors",
    "max_cores": "Up to 64 cores per CPU (128 cores total)",
    "tdp_support": "Up to ~350W per processor"
  },

  "memory": {
    "slots": 32,
    "type": "DDR5 ECC RDIMM",
    "max_capacity": "Up to ~4 TB",
    "max_speed": "DDR5-4800 or DDR5-5600 (model dependent)"
  },

  "storage": {
    "nvme": "Up to 12 × 2.5\" hot-swap NVMe/SAS/SATA bays",
    "m2": "2 × M.2 PCIe 4.0 x4"
  },

  "network": {
    "lan": [
      "2 × 10 GbE (optional dual-port LAN module)",
      "1 × IPMI management port"
    ]
  },

  "ports": {
    "usb": "Rear USB 3.2 ports (typical)",
    "display": "VGA (via ASPEED AST2600 BMC)",
    "console": "1 × Management LAN (IPMI)"
  },

  "expansion": {
    "pcie": [
      "PCIe 5.0 slots (varies by board/risers, e.g., 4 × PCIe 5.0)",
      "OCP 3.0 slot for networking"
    ],
    "gpu_support": "Supports 1 × dual-slot GPU (e.g., NVIDIA A100 / Intel Data Center GPU Flex) in select configurations"
  },

  "power_supply": {
    "redundant_psu": "Dual 1600W+ redundant PSUs (80 PLUS Platinum/Titanium)",
    "cooling": "High-performance server fans"
  },

  "form_factor": "1U Rackmount Server",
  "image": "/static/images/asus_workstation.jpg",
  "price": 200000
},

{
  "id": "server-asus-esc4000-g4",
  "name": "ASUS ESC4000 G4",
  "brand": "ASUS",
  "series": "gpu-system",
  "category_key": "server",
  "sub_category": "asus",
  "category": "GPU Server / AI Compute Server",
  "application": "AI / Deep Learning / HPC / Data Center / GPU Rendering",
  "description": "2U high-performance GPU server supporting up to 4 high-end NVIDIA GPUs, dual Intel Xeon Scalable processors, large DDR4 memory capacity, multiple PCIe expansion slots, and redundant power — ideal for AI training, inference, HPC, simulation, and GPU-accelerated workloads.",

  "processor": {
    "socket": "Dual LGA 3647",
    "supported_cpus": "Intel Xeon Scalable (1st & 2nd Gen)",
    "max_cores": "Up to 56 cores per CPU (112 cores total)",
    "tdp_support": "Up to 205W per CPU"
  },

  "memory": {
    "slots": 16,
    "type": "DDR4 ECC RDIMM / LRDIMM",
    "max_capacity": "Up to 2 TB",
    "max_speed": "Up to 2933 MT/s"
  },

  "chipset": "Intel C621",

  "storage": {
    "sata": "8 × 3.5\" / 2.5\" SATA hot-swap bays",
    "nvme": "4 × NVMe supported (model dependent)"
  },

  "network": {
    "lan": [
      "2 × 10/100/1000 Mbps LAN ports",
      "1 × Dedicated IPMI remote management port"
    ]
  },

  "ports": {
    "usb": "USB 3.0, USB 2.0 (rear + internal)",
    "display": "VGA (via ASPEED AST2500 BMC)",
  },

  "expansion": {
    "pcie": [
      "7 × PCIe 3.0 slots",
      "Supports up to 4 × double-slot GPUs (NVIDIA Tesla / A-series / Quadro)"
    ]
  },

  "form_factor": "2U Rackmount Server",
  "image": "/static/images/asus_gpu.jpg",
  "price": 650000
},



#  LENOVO SERVER

{
  "id": "server-lenovo-thinksystem-sr650",
  "name": "Lenovo ThinkSystem SR650",
  "brand": "Lenovo",
  "series": "enterprise-storage",
  "category_key": "server",
  "sub_category": "lenovo",
  "category": "Enterprise Rack Server",
  "sub_category": "lenovo",
  "series": "thinksystem",
  "application": "Virtualization / Storage / Database / Cloud / Enterprise Workloads",
  "description": "A high-performance 2U enterprise server supporting dual Intel Xeon Scalable processors, large DDR4 memory capacity, flexible storage configurations, and multiple PCIe expansion options. Designed for virtualization, software-defined storage, cloud workloads, and enterprise data center environments.",

  "processor": {
    "socket": "Dual LGA 3647",
    "supported_cpus": "Intel Xeon Scalable (Silver, Gold, Platinum – 1st & 2nd Gen)",
    "max_cores": "Up to 28 cores per CPU (56 cores total)",
    "tdp_support": "Up to ~205W per CPU"
  },

  "memory": {
    "slots": 24,
    "type": "DDR4 ECC RDIMM / LRDIMM",
    "max_capacity": "Up to 3 TB (with LRDIMMs)",
    "max_speed": "Up to 2933 MT/s"
  },

  "chipset": "Intel C622",

  "storage": {
    "bays": "8, 16, or 24 × 2.5\" SAS/SATA/NVMe OR 4/8/12 × 3.5\" bays",
    "m2": "Optional dual M.2 boot module"
  },

  "network": {
    "lan": [
      "2 × 1 GbE standard (model dependent)",
      "Optional 10/25/40/100GbE via PCIe or LOM adapters"
    ]
  },

  "ports": {
    "usb": "Front & rear USB 3.0 / 2.0",
    "display": "VGA (via XClarity management controller)",
  },

  "expansion": {
    "pcie": [
      "Up to 6 × PCIe 3.0 slots",
      "Optional 2 × GPUs (NVIDIA T4-class) depending on configuration"
    ]
  },

  "form_factor": "2U Rackmount Server",
  "image": "/static/images/lenovo_enterprise.jpg",
  "price": 350000
},

{
  "id": "server-lenovo-thinksystem-st550",
  "name": "Lenovo ThinkSystem ST550",
  "category_key": "server",
  "sub_category": "lenovo",
  "brand": "Lenovo",
  "series": "enterprise-storage",
  "category": "Enterprise Tower Server",

  "sub_category": "lenovo",
  "series": "thinksystem",
  "brand": "Lenovo",
  "application": "Virtualization / Storage / Database / Branch Office / Enterprise Workloads",
  "description": "A powerful, scalable 4U tower server supporting dual Intel Xeon Scalable processors, high memory capacity, multiple PCIe expansion slots, and flexible storage options. Ideal for branch offices, enterprise workloads, virtualization, and scalable storage deployments.",

  "processor": {
    "socket": "Dual LGA 3647",
    "supported_cpus": "Intel Xeon Scalable (Silver, Gold, Platinum – 1st & 2nd Gen)",
    "max_cores": "Up to 28 cores per CPU (56 cores total)",
    "tdp_support": "Up to ~165W per CPU"
  },

  "memory": {
    "slots": 12,
    "type": "DDR4 ECC RDIMM / LRDIMM",
    "max_capacity": "Up to 768 GB (RDIMM) / 1.5 TB (LRDIMM)",
    "max_speed": "Up to 2666 MT/s"
  },

  "chipset": "Intel C622",

  "storage": {
    "drive_bays": "Up to 16 × 2.5\" SAS/SATA/NVMe or up to 8 × 3.5\" bays",
    "m2": "Optional dual-M.2 boot module"
  },

  "network": {
    "lan": [
      "2 × 1 GbE onboard LAN ports",
      "Optional 10/25 GbE via PCIe adapter"
    ]
  },

  "ports": {
    "usb": "USB 3.0 / 2.0 front + rear",
    "display": "VGA (via XClarity controller)",
  },

  "expansion": {
    "pcie": [
      "Up to 6 × PCIe 3.0 slots",
      "Support for 1 × low-profile GPU (e.g., NVIDIA T4)"
    ]
  },

  "form_factor": "Tower Server (convertible to 4U rackmount)",
  "image": "/static/images/lenovo_enterprise.jpg",
  "price": 250000
}


]
