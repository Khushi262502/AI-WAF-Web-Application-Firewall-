def generate_mutations(payload):
    mutations = []
    
    mutations.append(payload.upper())
    mutations.append(payload.lower())
    
    mutations.append(payload.replace("'" , '"'))
    
    mutations.append(payload + "--")
    
    mutations.append(payload.replace(" " , "%20"))
    
    mutations.append("(" + payload + ")")
    
    return list(set(mutations))
