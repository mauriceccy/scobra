#%% [markdown]
## Testing your Scobra knowledge
#
# The following tutorial will test your knowledge of Scobra. It is important to have read 
# the documentation before you proceed with using this. This is not a graded exam, and you are free to consult
# the Scobra documentation when using this. 
# 
# If any errors come up, try your best to investigate the problem by consulting
# the documentation first, then searching google for the specific error. In the worst case, open the solution cell to see the answer.
# Understand the solution regardless if you got the question correct or wrong. If you have any questions about a specific topic here, feel free to
# approach your supervisor. 
# 
# Remember, this tutorial basically follows the documentation, from loading to modifying the model. Remember to check and read the documentation. Goodluck!
#%% [markdown]
#1.You will need to import scobra first for all of your projects. Then,create an empty model by initializing an instance of scobra.Model
#%%
import scobra
m=scobra.Model()
#uncomment the above two lines^
# m is the instance of scobra.Model

#%%[markdown]
# 2. Add a cell below this by clicking on this then clicking add cell on the top left of jupyter.
# Then, show the reactions present in the model. It should return a "[]" because it's an empty model. Remember to check your spelling and capitalization!
#%%[markdown]
# 3. Let's add some reactions! Recall the format of a adding reactions. (Page 11 of Documentation)
# Create a new reaction with the name 'R1' with metabolites 'A' and 'B', whose coefficients are 1, 0, respectively.
# Next, make another one named 'R2' with the same Metabolite names but whose coefficients are -2, 1, respectively.
# Create 'R3' with the same Metabolites with coefficients -1,0, respectively.
# Finally, make 'R4' with the same Metabolites with coefficients 0,-1, respectively.

# Models have hundreds of these, and we're only doing this to build a simple model.
%%latex
$$
R1\quad \rightarrow A \\
R2\quad 2A \rightarrow B\\ 
R3\quad A \rightarrow \\
R4\quad B \rightarrow 
$$
#%%
m.AddReaction('R1',{'A':1,'B':0})
m.AddReaction('R2',{'A':-2,'B':1})
m.AddReaction('R3',{'A':-1,'B':0})
m.AddReaction('R4',{'A':0,'B':-1})

#%%
#Run these four commands after your created them to see the difference
m.PrintReaction('R1')
m.PrintReaction('R2')
m.PrintReaction('R3')
m.PrintReaction('R4')

m.GetReaction('R1')
# You can see that 'R1' doesn't have an upper bound of 1000. This is the default constraint for reactions.
#%%
#%%[markdown]
# 4. Let's now set a constraint for 'R1'. To do so, follow 2.3.1 - 2.3.3 (pp. 18-19) in the Documentation. 
# Set the lower bound to 10, and upper bound to 10.
#Now set objective to 'R' and set the direction to maximization
#%%
m.SetConstraint('R1',10,10)
m.SetObjective(['R1'])
m.SetObjDirec('Max')

#%%[markdown]
# Now we're ready to solve the system. Run the solve function and GetSol to get a list of solution fluxes.
#%%
m.Solve()
m.GetSol()
# These should return 'optimal' and {'R1': 10.0, 'R3': 10.0}
# R2 and R4's optimal solutions are 0.
#%%[markdown]
# For the curious, this is represented by a Metabolites x Reactions matrix multiplied by a vector given by the objective function. Multiplying this matrix to this vector will give a single number (0).
# We're finding ou the values of x that satisfy this requirement.  
%%latex
\[
\begin{matrix}
A\\   
B\\
\end{matrix}
\begin{matrix}
R1\quad R2\quad R3\quad R4\\
\begin{pmatrix}
1 & -2 & -1 & 0\\
0 & 1 & 0 & -1\\
\end{pmatrix}
\end{matrix}
\times
\begin{pmatrix}
x_1\\
x_2\\
x_3\\
x_4\\
\end{pmatrix}
=0
\]
#%%[markdown]
# After solving it,
# x_1 = 10
# x_2= 0
# x_3=10
# x_4 =0
#%%