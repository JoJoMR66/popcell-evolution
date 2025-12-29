def simulation(b_max, s, d, pop_max, initial_A_proportion=.5, max_iterations=int(1e10), save_population=False):
    N_m = (1-d/b_max)*pop_max # nombre moyen autour duquel la population totale se situe
    N_i = int(.9*N_m)
   
    # INITIALIZATION
    NA_init = int(initial_A_proportion*N_i)
    NB_init = int((1-initial_A_proportion)*N_i)
    
    # Initialize list for better performances
    pop_over_time = np.zeros((2, save_population and max_iterations or 1), dtype=np.int32)
    time_list = np.zeros((save_population and max_iterations or 1), dtype=float) 

    step_number = 1
    current_t = 0

    # population
    nA = NA_init
    nB = NB_init

    if save_population: 
        pop_over_time[0,0] = nA
        pop_over_time[1,0] = nB
    
    def return_function():
        if save_population:
            return pop_over_time[:,:step_number], time_list[:step_number], step_number
        else:
            pop_over_time[:,-1] = [nA, nB]
            time_list[-1] = current_t
            return pop_over_time, time_list, step_number
    
    # birth coeff
    b1_max = b_max*(1+s)
    b2_max = b_max
    
    # death coeff
    dA = d
    dB = d
    
    # ITERATIONS
    while step_number<max_iterations:
        if nA == 0 or nB == 0:
            return return_function()

        # Change birth rate
        total_pop = nA + nB

        if total_pop >= pop_max:
            bA = 0
            bB = 0
        else:
            growth = 1 - total_pop/pop_max
            bA = b1_max * growth
            bB = b2_max * growth
        
        # New coefficient and dt computation
        a1b = nA*bA
        a1d = nA*dA
        a2b = nB*bB
        a2d = nB*dB
        
        a0 = a1b + a1d + a2b + a2d
        
        r1 = np.random.random()
        r2_a0 = np.random.random()*a0
        
        if r2_a0 < a1b:
            nA += 1
        elif r2_a0 < a1b+a1d:
            nA -= 1
        elif r2_a0 < a1b+a1d+a2b:
            nB += 1
        else:
            nB -= 1
            
        dt = -np.log(r1)/a0
        current_t += dt

        if save_population:
            pop_over_time[0, step_number] = nA
            pop_over_time[1, step_number] = nB
            time_list[step_number] = current_t
        
        step_number += 1

    return return_function()