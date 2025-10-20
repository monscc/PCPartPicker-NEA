"""
PC Building Guide Tab - Comprehensive component education
"""
import tkinter as tk
from tkinter import ttk, font as tkfont
from typing import Dict, List, Tuple

class GuideTab(ttk.Frame):
    """Educational guide for PC building with component specifications"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the guide interface with expandable sections"""
        # Main container with scrollbar
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas for scrolling
        canvas = tk.Canvas(main_container, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        header = tk.Label(scrollable_frame, text="PC Building Guide", 
                         font=('Segoe UI', 20, 'bold'), bg='#f0f0f0')
        header.pack(pady=(0, 10))
        
        intro = tk.Label(scrollable_frame, 
                        text="Learn about PC components and how to choose the right parts for your build",
                        font=('Segoe UI', 10), bg='#f0f0f0', wraplength=700)
        intro.pack(pady=(0, 20))
        
        # Component sections
        self._create_section(scrollable_frame, "1. CPU (Processor)", self._get_cpu_content())
        self._create_section(scrollable_frame, "2. Motherboard", self._get_motherboard_content())
        self._create_section(scrollable_frame, "3. RAM (Memory)", self._get_ram_content())
        self._create_section(scrollable_frame, "4. GPU (Graphics Card)", self._get_gpu_content())
        self._create_section(scrollable_frame, "5. Storage", self._get_storage_content())
        self._create_section(scrollable_frame, "6. PSU (Power Supply)", self._get_psu_content())
        self._create_section(scrollable_frame, "7. Case", self._get_case_content())
        self._create_section(scrollable_frame, "8. CPU Cooler", self._get_cooler_content())
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def _create_section(self, parent, title: str, content: List[Tuple[str, str]]):
        """Create expandable section with title and content"""
        section_frame = ttk.LabelFrame(parent, text=title, padding=10)
        section_frame.pack(fill=tk.X, pady=5, padx=5)
        
        for subtitle, text in content:
            # Subtitle
            subtitle_label = tk.Label(section_frame, text=subtitle, 
                                     font=('Segoe UI', 10, 'bold'),
                                     bg='white', anchor='w')
            subtitle_label.pack(fill=tk.X, pady=(5, 2))
            
            # Content
            content_label = tk.Label(section_frame, text=text,
                                    font=('Segoe UI', 9),
                                    bg='white', anchor='w', justify='left',
                                    wraplength=680)
            content_label.pack(fill=tk.X, padx=10, pady=(0, 5))
    
    def _get_cpu_content(self) -> List[Tuple[str, str]]:
        """CPU specifications and explanations"""
        return [
            ("Clock Speed (GHz)", 
             "Measures how many cycles per second the CPU can execute. Higher is faster. "
             "Base clock is standard speed, Boost clock is maximum speed under load. "
             "Example: 3.6 GHz base / 4.9 GHz boost."),
            
            ("Cores & Threads",
             "Cores are physical processing units. Threads allow each core to handle multiple tasks. "
             "More cores = better multitasking. 6 cores for gaming, 8+ for content creation. "
             "SMT/Hyper-Threading doubles threads (8 cores = 16 threads)."),
            
            ("Cache (MB)",
             "Ultra-fast memory on the CPU chip. L1 (smallest, fastest) → L2 → L3 (largest). "
             "More cache = better performance. Modern CPUs have 16-96MB L3 cache."),
            
            ("TDP (Watts)",
             "Thermal Design Power - heat output and power consumption. "
             "65W = efficient, 125W+ = high performance. Match cooler to TDP rating."),
            
            ("Socket Type",
             "Physical connector - must match motherboard. Intel: LGA1700. AMD: AM5, AM4. "
             "Check compatibility before purchasing!")
        ]
    
    def _get_motherboard_content(self) -> List[Tuple[str, str]]:
        """Motherboard specifications"""
        return [
            ("Form Factor",
             "Physical size: ATX (standard, most features), Micro-ATX (smaller, fewer slots), "
             "Mini-ITX (compact builds). Must fit in your case!"),
            
            ("Socket",
             "Must match CPU socket. Intel LGA1700 for 12th/13th/14th gen. "
             "AMD AM5 for Ryzen 7000, AM4 for older Ryzen."),
            
            ("Chipset",
             "Controls features and overclocking. Intel: Z790 (OC), B760 (mainstream). "
             "AMD: X670E (high-end), B650 (value). Higher tier = more features."),
            
            ("RAM Slots & Speed",
             "Typically 2 or 4 slots. Check max capacity (128GB+). "
             "Support for DDR4 or DDR5, speeds up to 6000+ MHz. Faster = better performance."),
            
            ("PCIe Slots",
             "For GPU and expansion cards. PCIe 4.0 x16 for GPU (5.0 for newest). "
             "More slots = more upgrades. M.2 slots for NVMe SSDs (check Gen4 vs Gen3).")
        ]
    
    def _get_ram_content(self) -> List[Tuple[str, str]]:
        """RAM specifications"""
        return [
            ("Capacity (GB)",
             "How much data RAM can hold. 16GB minimum for gaming, 32GB for multitasking, "
             "64GB+ for content creation. More RAM = more programs open simultaneously."),
            
            ("Speed (MHz)",
             "How fast RAM transfers data. DDR4: 3200-3600 MHz ideal. DDR5: 5200-6000+ MHz. "
             "Faster speeds improve CPU performance, especially on Ryzen."),
            
            ("DDR Generation",
             "DDR4 (older, cheaper, compatible) vs DDR5 (newer, faster, expensive). "
             "Must match motherboard support. DDR5 is future-proof but costs more."),
            
            ("Latency (CL)",
             "Lower = faster response. CL16 is good for DDR4, CL30-36 for DDR5. "
             "Format: CL16-18-18-38. First number matters most."),
            
            ("Configuration",
             "Single stick vs Dual/Quad channel. 2x16GB is better than 1x32GB for speed. "
             "Use matched pairs for dual channel (2x or 4x sticks).")
        ]
    
    def _get_gpu_content(self) -> List[Tuple[str, str]]:
        """GPU specifications"""
        return [
            ("VRAM (GB)",
             "Video memory for textures/graphics. 8GB for 1080p, 12GB for 1440p, "
             "16GB+ for 4K gaming. More VRAM = higher resolutions and settings."),
            
            ("CUDA/Stream Processors",
             "Parallel processing cores. NVIDIA = CUDA cores, AMD = Stream processors. "
             "More cores = better performance. 4000-16000 cores in modern GPUs."),
            
            ("Clock Speed (MHz)",
             "Base and Boost clocks like CPU. 2000-3000 MHz typical. "
             "Higher boost = better gaming performance. Many GPUs auto-overclock."),
            
            ("Power (TDP)",
             "150-450W typical. High-end GPUs need 350W+. "
             "Check PSU wattage and required PCIe power connectors (6-pin, 8-pin, 12VHPWR)."),
            
            ("Architecture & Gen",
             "NVIDIA: RTX 40-series (Ada), 30-series (Ampere). AMD: RX 7000 (RDNA 3). "
             "Newer generations = better performance per watt and new features (ray tracing, DLSS).")
        ]
    
    def _get_storage_content(self) -> List[Tuple[str, str]]:
        """Storage specifications"""
        return [
            ("SSD vs HDD",
             "SSD: Fast (3000+ MB/s), no moving parts, expensive per GB. For OS and games. "
             "HDD: Slow (150 MB/s), cheap bulk storage. Use SSD for boot, HDD for files."),
            
            ("Interface Type",
             "NVMe M.2 (fastest, 3500-7000 MB/s), SATA SSD (560 MB/s), SATA HDD (150 MB/s). "
             "NVMe uses M.2 slot on motherboard. SATA uses cables."),
            
            ("Capacity",
             "500GB minimum for OS, 1TB+ recommended. Games need 50-150GB each. "
             "1TB NVMe for main drive + 2TB HDD for storage is common setup."),
            
            ("PCIe Generation",
             "Gen3 (3500 MB/s), Gen4 (7000 MB/s), Gen5 (14000 MB/s). "
             "Gen4 is sweet spot for gaming. Gen5 is overkill but future-proof."),
            
            ("Endurance (TBW)",
             "Terabytes Written - drive lifespan. 600 TBW = write 600TB before failure. "
             "More TBW = longer lasting. 300+ TBW is good for consumers.")
        ]
    
    def _get_psu_content(self) -> List[Tuple[str, str]]:
        """PSU specifications"""
        return [
            ("Wattage",
             "Total power output. Calculate: CPU + GPU + 150W overhead. "
             "650W for mid-range, 850W for high-end, 1000W+ for RTX 4090. "
             "Headroom = quieter operation and efficiency."),
            
            ("Efficiency Rating",
             "80+ Bronze (82%), Silver (85%), Gold (87%), Platinum (90%), Titanium (92%). "
             "Higher = less wasted electricity and heat. Gold is sweet spot."),
            
            ("Modularity",
             "Non-modular (all cables attached), Semi-modular (main cables fixed), "
             "Fully modular (all removable). Modular = cleaner builds, easier cable management."),
            
            ("Connectors",
             "24-pin ATX (motherboard), 8-pin EPS (CPU), PCIe 6+2 pin (GPU). "
             "Count matters! RTX 4080 needs 3x 8-pin or 1x 12VHPWR. Check GPU requirements."),
            
            ("Protection Features",
             "OVP (over-voltage), UVP (under-voltage), OCP (over-current), SCP (short-circuit). "
             "Good PSUs have all protections. Protects components from damage.")
        ]
    
    def _get_case_content(self) -> List[Tuple[str, str]]:
        """Case specifications"""
        return [
            ("Form Factor",
             "Must fit motherboard. Full Tower (E-ATX, huge), Mid Tower (ATX, standard), "
             "Micro-ATX (compact), Mini-ITX (small). Most use Mid Tower."),
            
            ("GPU Clearance",
             "Maximum GPU length. Measure in mm. Modern GPUs are 300-360mm long. "
             "Check case specs! Some cases support 420mm+ cards."),
            
            ("CPU Cooler Height",
             "Maximum cooler height in mm. Tower coolers are 150-165mm tall. "
             "Low-profile cases need small coolers. Check clearance!"),
            
            ("Airflow & Cooling",
             "Front intake + rear/top exhaust. More fans = better cooling. "
             "Mesh front panels = better airflow than solid. 3-6 fans typical."),
            
            ("Cable Management",
             "PSU shroud, cable routing holes, velcro straps. "
             "Good cases have space behind motherboard tray (20-30mm) for hiding cables.")
        ]
    
    def _get_cooler_content(self) -> List[Tuple[str, str]]:
        """CPU Cooler specifications"""
        return [
            ("Air vs AIO Liquid",
             "Air: Fan + heatsink, reliable, quiet, cheap ($30-100). "
             "AIO Liquid: Radiator + pump, better cooling, looks cool, expensive ($80-200+). "
             "Both work well. Air is simpler."),
            
            ("TDP Rating",
             "Cooling capacity in watts. Must exceed CPU TDP. "
             "65W CPU = basic cooler OK. 125W+ CPU = tower cooler or 240mm AIO needed."),
            
            ("Height/Size",
             "Tower coolers: 120mm (low), 155mm (standard), 165mm+ (tall). "
             "AIO radiators: 120mm, 240mm (common), 280mm, 360mm (best cooling). "
             "Check case compatibility!"),
            
            ("Socket Support",
             "Must support your CPU socket. LGA1700, AM5, AM4, etc. "
             "Many coolers include multiple mounting brackets. Check specs!"),
            
            ("Noise Level (dBA)",
             "20-25 dBA = silent, 30-35 dBA = quiet, 40+ dBA = audible. "
             "Larger fans spin slower = quieter. PWM fans adjust speed automatically.")
        ]
