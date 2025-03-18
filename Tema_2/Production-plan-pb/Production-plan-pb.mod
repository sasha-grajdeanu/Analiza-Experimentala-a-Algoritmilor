/*********************************************
 * OPL 22.1.2.0 Model
 * Author: user
 * Creation Date: Mar 18, 2025 at 1:09:35 PM
 *********************************************/
dvar float+ Gas;
dvar float+ Chloride;

maximize
	40 * Gas + 50 * Chloride;
	
subject to {
  ctMaxTotal:
  	Gas + Chloride <= 50;
  
  ctMaxTotal2:
  	3 * Gas + 4 * Chloride <= 180;
  
  ctMaxChloride:
  	Chloride <= 40;
}