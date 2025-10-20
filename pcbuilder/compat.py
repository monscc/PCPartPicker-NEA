from typing import Dict, List, Tuple


def check_cpu_mobo(cpu: Dict, mobo: Dict) -> Tuple[bool, str]:
    if cpu is None or mobo is None:
        return True, "CPU or motherboard missing - cannot check socket"
    cpu_socket = cpu.get("attributes", {}).get("socket")
    mobo_socket = mobo.get("attributes", {}).get("socket")
    if cpu_socket != mobo_socket:
        return False, f"CPU socket {cpu_socket} does not match motherboard socket {mobo_socket}"
    return True, "CPU and motherboard sockets match"


def check_ram_mobo(ram: Dict, mobo: Dict) -> Tuple[bool, str]:
    if ram is None or mobo is None:
        return True, "RAM or motherboard missing - cannot check memory type"
    ram_type = ram.get("attributes", {}).get("memory_type")
    mobo_mem = mobo.get("attributes", {}).get("memory_type")
    if ram_type != mobo_mem:
        return False, f"RAM type {ram_type} does not match motherboard supported {mobo_mem}"
    # check slot count
    try:
        slots = int(mobo.get("attributes", {}).get("memory_slots", 0))
        sticks = int(ram.get("attributes", {}).get("sticks", 1))
        if sticks > slots:
            return False, f"RAM sticks ({sticks}) exceed motherboard slots ({slots})"
    except Exception:
        pass
    return True, "RAM appears compatible with motherboard"


def check_case_mobo_case_gpu(mobo: Dict, case: Dict, gpu: Dict) -> List[Tuple[bool, str]]:
    results = []
    # form factor
    if mobo and case:
        mobo_form = mobo.get("attributes", {}).get("form_factor")
        case_form = case.get("attributes", {}).get("supported_form_factors")
        if case_form and mobo_form not in case_form.split(","):
            results.append((False, f"Motherboard form factor {mobo_form} not supported by case ({case_form})"))
        else:
            results.append((True, "Motherboard fits case form factor"))
    # GPU length
    if gpu and case:
        try:
            gpu_len = int(gpu.get("attributes", {}).get("length_mm", 0))
            max_len = int(case.get("attributes", {}).get("max_gpu_length_mm", 0))
            if gpu_len > max_len:
                results.append((False, f"GPU length {gpu_len}mm exceeds case max {max_len}mm"))
            else:
                results.append((True, "GPU fits in case"))
        except Exception:
            results.append((True, "GPU / case length unknown - skipping check"))
    return results


def check_psu_wattage(parts: Dict[str, Dict], headroom: float = 1.25) -> Tuple[bool, str]:
    psu = parts.get("PSU")
    if psu is None:
        return False, "No PSU selected"
    try:
        psu_w = int(psu.get("attributes", {}).get("wattage", 0))
    except Exception:
        return False, "PSU wattage unknown"
    total_draw = 0
    for k, p in parts.items():
        if p is None:
            continue
        if k == "PSU":
            continue
        try:
            total_draw += int(p.get("attributes", {}).get("power_draw", 0))
        except Exception:
            pass
    required = int(total_draw * headroom)
    if psu_w < required:
        return False, f"PSU wattage {psu_w}W insufficient for estimated draw {total_draw}W (required with headroom: {required}W)"
    return True, "PSU wattage appears sufficient"


def run_full_check(parts: Dict[str, Dict]) -> List[Tuple[str, bool, str]]:
    results = []
    results.append(("cpu_socket",) + check_cpu_mobo(parts.get("CPU"), parts.get("Motherboard")))
    results.append(("ram_mobo",) + check_ram_mobo(parts.get("RAM"), parts.get("Motherboard")))
    for idx, res in enumerate(check_case_mobo_case_gpu(parts.get("Motherboard"), parts.get("Case"), parts.get("GPU"))):
        results.append((f"case_check_{idx}", res[0], res[1]))
    results.append(("psu_wattage",) + check_psu_wattage(parts))
    return results
