/*********************************************
 * OPL 22.1.2.0 Model
 * Author: user
 * Creation Date: Mar 18, 2025 at 12:54:35 PM
 *********************************************/
int NbItems = ...;
int NbResources = ...;
range Items = 1..NbItems;
range Resources = 1..NbResources;
int Capacity[Resources] = ...;
int Value[Items] = ...;
int Use[Resources][Items] = ...;
int MaxValue = max(r in Resources) Capacity[r];


dvar int Take[Items] in 0..MaxValue;

maximize
  sum(i in Items) Value[i] * Take[i];
  
subject to {
  forall( r in Resources )
    ct:
      sum( i in Items ) 
        Use[r][i] * Take[i] <= Capacity[r];
}