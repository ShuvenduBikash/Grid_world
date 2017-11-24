# Reinforcement Learning algorithm simulation with Grid world

## Optimal value function

find the optimal value for each grid cell
![](images/f1.png)
### Deterministic 
![](images/ovf_de.png)

### Stochastic 
![](images/f2.png)
![](images/ovf_st.png)

## Q value iteration
![](images/f3.png)
Here we save the the value for each  state action pair.
Which is defining how good an action is by taking the action and how much we can get from the state we land in.
</br></br>
![](images/q_value.png)

## Policy evaluation
In this case instead of finding the max value over all action. we will take the value for the defined policy
</br>So the only difference in the equation is the absence of max()
![](images/f4.png)
        `python policy_evaluation.py`