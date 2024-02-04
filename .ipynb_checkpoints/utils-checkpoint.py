from pysolve.utils import is_close
from new_developmentalist_model import create_model

def rescale_solution(soln):
    """Rescale model solutions to keep level variables below infinity"""
    scaling_factor_output = (1/soln["Y"])*100
    scaling_factor_labor_force = (1/soln["N"])*100
    
    scaling_factor_price = (1/soln["p"])
    
    # Scale growing variables (WARNING: assumes n=0!)
    soln["Y"] *= scaling_factor_output
    soln["K"] *= scaling_factor_output
    soln["X"] *= scaling_factor_output
    soln["y"] *= scaling_factor_output/scaling_factor_labor_force
    soln["N"] *= scaling_factor_labor_force
    
    # Scaling w by output (i.e. productivity growth)
    soln["w"] *= scaling_factor_output*scaling_factor_price
    soln["p"] *= scaling_factor_price
    return soln


def run_model_to_convergence(starting_values=None):
    """Find stable starting values by running model until convergence"""
    mod = create_model()
    
    if starting_values:
        mod.set_values(starting_values)
    
    for i in range(5_000):
        mod.solve(iterations=1_000, threshold=1e-4)
        mod.solutions[-1] = rescale_solution(mod.solutions[-1])
        prev_soln = mod.solutions[-2]
        soln = mod.solutions[-1]
        stop = is_close(prev_soln, soln, rtol=1e-5)
        if stop:
            print(f"Stoppin in iteration {i}")
            break
    rounded_solution = {k:round(v, 4) for k, v in mod.solutions[-1].items()}
    return rounded_solution