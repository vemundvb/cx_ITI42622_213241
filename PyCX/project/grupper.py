


from config import get_config



def get_risikogrupper():
    config = get_config()

    return { 
        "alder_80":                 {"n": 3,  "pc": config["pc"], 'c': '#03288a'},
        "alder65_79":               {"n": 6,  "pc": config["pc"], 'c': '#0c2e8a'},
        "kreft":                    {"n": 4,  "pc": config["pc"], 'c': '#1b3989'},
        "diabetes":                 {"n": 3,  "pc": config["pc"], 'c': '#132d75'},
        "fedme":                    {"n": 10,  "pc": config["pc"], 'c': '#1e49c1'},
        "nyresvikt":                {"n": 4,  "pc": config["pc"], 'c': '#3760d1'},
        "funksjonsnedsettelse":     {"n": 3,  "pc": config["pc"], 'c': '#1a4ddc'},
        "demens":                   {"n": 1,  "pc": config["pc"], 'c':'#0d41d3'},
        "psykisk_lidelse":          {"n": 1,  "pc": config["pc"], 'c': '#022178'},
        "downs":                    {"n": 1,  "pc": config["pc"], 'c': '#052a92'},
        
        "ingen_risiko":             {"n": 20,  "pc": config["pc_no"], 'c': '#021750'}
    }


def get_sum_n():
    return sum(v["n"] for v in get_risikogrupper().values())




