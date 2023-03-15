# base defense (.mod file)

## sets and parameters
# set of nodes - bases
set V;

# base is a critical point (to defend) 0 Non - 1 Oui
param is_critical_point{V} binary;

# set of edges - one base can protect the other base
set E within {V,V};

# set of pairs of antiparallel arcs
set A := E union {u in V, v in V : (v,u) in E}; 

# neighbours
set N{u in V} := {v in V : (u,v) in A};

## decision variables

# Arm a base 0 Non - 1 Oui
var to_arm{V} binary;

## objective function
minimize total_cost: sum{v in V} to_arm[v];
 
## constraint
subject to critical_points_defended{v in V : is_critical_point[v] = 1}: to_arm[v] + sum{n in N[v]} to_arm[n] >= 1;
