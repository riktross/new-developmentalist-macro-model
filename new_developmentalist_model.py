from pysolve.model import Model

def create_model():
    model = Model()
    model.set_var_default(0)

    ####### VARIABLES #######################################################
    model.var('u', desc="Capacity utilization rate", default=0.7)
    model.var('gu', desc="Growth of capacity utilization rate")
    
    model.var('e', desc="Employment share dynamic", default=1) # Eq2
    model.var('ge', desc="Growth in employment share dynamic") # Eq2
    
    model.var('Y', desc='Output', default=100)
    model.var('gY', desc='Growth of Output')
    
    model.var('sigma', desc='Supermultiplier')
    
    model.var('h', desc='Propensity to invest I/Y (0<h<1)', default=0.2561)
    model.var('gh', desc='Growth in propensity to invest')
    
    model.var('y', desc='Productivity', default=1)
    model.var('gy', desc='Growth in productivity')
    
    model.var('gamma', desc='Share of manufacturing', default=0.25)
    model.var('ggamma', desc='Growth of share of manufacturing')
    
    model.var('X', desc='Exports', default=44.4)
    model.var('gX', desc='Growth rate of exports')
    
    model.var('p', desc='Price level', default=1)
    model.var('gp', desc='Inflation rate')
    
    model.var('z', desc='Mark-up')
    
    model.var('w', desc='Nominal wage', default=0.5)
    model.var('gw', desc='Growth in nominal wage')
    model.var('varpi', desc='Wage share')
    
    model.var('gp_e', desc='Expected inflation')
    model.param('gp_bar', desc='Inflation target', default=0.02)
    
    model.var('d', desc='Current account deficit')
    
    model.var('ca', desc='Capital account surplus')
    
    model.var('i', desc='Domestic interest rate', default=0.04)
    
    model.var('N', desc='Labor force', default=100)

    model.var('K', desc='Capital stock', default=100)
    model.var('gK', desc='Growth of capital stock')
    
    model.var('q_i', desc='Industrial equilibrium exchange rate')
    model.var('q_cab', desc='CAB equilibrium exchange rate')
    

    ####### PARAMETERS #######################################################
    model.param('vareps', desc="Optimal capital-output ratio", default=4.66)

    model.param('c', desc='Propensity to cosume', default=0.8)
    model.param('m', desc='Propensity to import', default=0.2)
    model.param('g', desc='Propensity to government spend', default=0.05)

    model.param('mu', desc='Response parameter of investment propensity', default=0.01)
    model.param('u_n', desc='Normal capacity utilization rate', default=0.7)

    model.param('alpha_0', desc='Autonomous grouth in productivity', default=0.005)
    model.param('alpha_1', desc='Capital intensity effect on productivity >0', default=0.5)
    model.param('alpha_2', desc='Labor market effect on productivity >0', default=0.03)

    model.param('beta_0', desc='Autonomous growth in manufacturing (<0)', default=-0.01)
    model.param('beta_1', desc='Real exchange rate effect in manufacturing growth(>0)', default=0.01)
    model.param('beta_2', desc='Tech. Gap effect in manufacturing growth(>0)', default=0.0875)
    model.param('Gap', desc='Tech. Gap effect in manufacturing growth (>0)', default=0.2)

    model.param('x_0', desc='Autonomous export component', default=0.015)
    model.param('x_1', desc='Export reaction to manufacturing share', default=0.1)

    model.param('xi_0', desc='Autonomous part of mark-up determination', default=0.5)
    model.param('xi_1', desc='Reaction of mark-up to real exchange rate', default=0.18)

    model.param('epsilon_1', desc='Effect of inflation expectations on wage growth (eps1 + eps2 < 1)', default=0.33)
    model.param('epsilon_2', desc='Effect of wage share targed deviation on wage growth', default=0.33)
    model.param('varpi_bar', desc='Target wage share', default=0.5)

    model.param('phi_0', desc='Autonomous part of deficit >0', default=0.275)
    model.param('phi_1', desc='Effect of real exchange rate on current account surplus >0', default=0.1)

    model.param('i_f', desc='Foreign interest rate', default=0.02)
    model.param('rho', desc='Country risk', default=0.02)
    model.param('psi', desc='Effect of interest differential on capital account (>0)', default=0.1)

    model.param('n', desc='Growth rate of labor force', default=0)
    
    model.param('q', desc='Real exchange rate')
    

    ####### EQUATIONS ########################################################
    
    model.add('u = vareps*(Y/K)', desc="Definition of utilization rate") # Eq2
    model.add('gu = (u - u(-1))/u(-1)', desc="u growth rate definition") # Helper
    
    model.add('e = Y /(y * N)', desc="Employment share dynamic") # Eq2
    model.add('ge = (e - e(-1))/e(-1)', desc="e growth rate definition") # Eq2
    
    model.add('Y = sigma*X', desc="Output definition") # Eq8
    model.add('gY = (Y - Y(-1))/Y(-1)', desc="Output growth definition")
    
    model.add('sigma = 1/(1-c+q*m-g-h)', desc='Harrod supermultiplier')
    
    
    model.add('gh = mu * (u - u_n)', desc='investment reaction function')
    model.add('h - h(-1) = gh * h(-1)', desc='h growth rate definition (backwards)')
    
     
    model.add('gy = (alpha_0 + alpha_2*e)/(1-alpha_1*gamma)', desc='Productivity growth function')
    model.add('y - y(-1) = gy * y(-1)', desc='y growth rate definition (backwards)')
    
    model.add('ggamma = beta_0 + beta_1*q - beta_2*Gap', desc='Manufacturing share growth')
    model.add('gamma - gamma(-1) = ggamma * gamma(-1)', desc='gamma growth rate definition (backwards)')
    
    model.add('gX = x_0 + x_1*gamma', desc='Export growth function')
    model.add('X - X(-1) = gX * X(-1)', desc='X growth rate definition (backwards)')
    
    model.add('p = (1+z) * w * (1/y)', desc='Pricing equation')
    model.add('gp = (p-p(-1))/p(-1)', desc="inflation rate definition")
    
    model.add('z = xi_0 + xi_1*q', desc='Mark-up determination')
    
    model.add('gw = epsilon_1*gp_e + epsilon_2*(varpi_bar - varpi) + (1-epsilon_1 - epsilon_2)*e', desc='Mark-up determination')
    model.add('w = (1+gw) * w(-1)', desc='w growth rate definition (backwards)')
    
    model.add('varpi = (w/p)/y', desc='Labor share of income')
    
    model.add('gp_e = gp_bar', desc='Inflation expectation')
    
    # 3.7 Balance-of-payments (dis)equilibrium and the exchange rate
    model.add('d=phi_0 - phi_1*q', desc='Current account deficit and RER')
    
    model.add('ca=d', desc='Capital account and current account identity')
    model.add('i=i_f + rho + (ca/psi)', desc='Domestic interest rate determination')
    
    #N as a exogenous growth rate
    model.add('N = (1+n) * N(-1)', desc='Exogenous growth of Labor force')
    
    # K is investment
    model.add('K - K(-1) = h*Y', desc='Capital gowth equation')
    model.add('gK = (K-K(-1))/K(-1)', desc='K Growth rate definition')

    #Helper vars
    model.add('q_i = (beta_2*Gap - beta_0)/beta_1', desc='Helper equation to show Eq. Exchange rate')
    model.add('q_cab = phi_0/phi_1', desc='Helper equation to show Eq. Exchange rate')
    return model