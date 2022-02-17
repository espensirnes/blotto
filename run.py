import blotto
import numpy as np

def computer_strategy(n_battalions,n_fields):
    #put your code here to change strategy
    #The function needs to return a vector with as many elements as there are battlefields (n_fields)
    #The total numner of battalions employed should equal n_battalions

    #random strategy:
    mean_battalions=int(n_battalions/n_fields)+1
    battalions=[np.random.randint(mean_battalions+1)+1 for i in range(n_fields)]
    
    while True:
        #ensuring random sequence:
        for i in np.random.rand(n_fields).argsort():
            if sum(battalions)==n_battalions:
                return battalions
            elif sum(battalions)<n_battalions:
                battalions[i]+=1
            elif sum(battalions)>n_battalions and battalions[i]>0:
                battalions[i]-=1


    
   
w=blotto.window(6,26,  computer_strategy)

w.mainloop()