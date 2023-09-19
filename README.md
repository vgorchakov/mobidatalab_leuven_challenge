# MCA-AHP + Discrete Optimization Approach for placing new multi-modal mobility hubs

Deployed app: https://leuven-mobility.streamlit.app/ 

Github repository: https://github.com/vgorchakov/mobidatalab_leuven_challenge 

The approach is designed and developed as a part of [MobiDataLab Mobility Hackathon](https://mobidatalab.eu/living-labs/hackathon/)  [Paris, France]
  The key idea of the proposed solution is to combine the power of Multi-Criteria Analysis and Discrete Optimization Power. We apply Multi-Criteria Analysis (MCA) with Analytics Hierarchy Process (AHP) procedure to socio and demographic data available in the hackathon. The result of these procedures - an indicator of neighbourhood that measures potential of a new mobility hub in this neighbourhood. We take into account the distribution of the current mobility hubs that are already incorporated in the city and weight this indicator with the number of opened hubs to assess the score of potential to place extra hubs in this neighbourhood. The output of this layer is a score per neighbourhood that we are going to use during the main step - Discrete Optimization Model. The heart of the solution is to use the power of discrete optimization modelling. 
  First of all, why mathematical optimization modelling? 
1) direct optimization of distance/operational cost with multi-objective
2) easy to incorporate new business constraints
3) fast to resolve with new input data The discrete optimization modelling requires a node-based approach.

  We need to make a smooth transit from the first step, since socio and demographic data, demand and supply and our computed indicator are based on neighbourhood level. To do this, we compute a centroid of each neighbourhood and associate all neighbourhood parameters with the centroid. To set up an optimization model, we need to define two main components: objectives and constraints. 
  
  Objective: free and commercial solvers allows to solve the optimization model with multiple objectives. In our case the first objective will be minimization of total duration time of all potential mobility hubs users. We will use a weighted sum and multiplicator to this duration time will be defined as (Neighbourhood Car Demand x Neighbourhood Attractiveness Indicator) where Neighbourhood Car Demand is taken from demand/supply data and Neighbourhood Attractiveness Indicator is computed in 1st stage of solution. 
  
  So, Obj. 1: MIN(Total duration time x (Neighbourhood Car Demand x Neighbourhood Attractiveness Indicator)) Second objective can be defined as minimization of the operational opening cost of new hubs. This factor depends on how expensive it is to build a new hub in a specific area. Obj. 2: MIN(Operational New Hubs Opening Cost) Optimization modelling allows us to consider different ways of objective prioritisation. We can take a weighted sum of these two objectives or indicate the prioritisation explicitly (first optimise Obj.1, then Obj.2) 
  
  Constraints: the real power of optimization model solution is an opportunity to add new business constraints after the first iterations of solving. Let's list the most obvious constraints that will arise during the process of industrialization of our solution: - number of new hubs is less then X - distance(hub, closest off-street parking) is less then Y - sum of hubs group capacity exceeds demand of local neighbourhoods - X, Y - configurable parameters The solving process can be done with free to use solvers such as CBC, GLPK or commercial solvers XPRESS, CPLEX. Gurobi The output of an optimization model - locations of extra multimodal mobility hubs. 
  
  Incorporation of new mobility hubs into the real life requires several practical next steps: - gather full list of existing operational constraints - incorporate into solution - work on a user-friendly app with integration to other services: - bike sharing companies, city official websites, etc. 
  
  The solution is designed and prepared by OREH team.
