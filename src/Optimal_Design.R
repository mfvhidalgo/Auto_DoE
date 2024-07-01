library(AlgDesign) # generates Optimal Design DoE; chosen over skpr because this does not use repeats
library(plyr) # merge df together

# naming convention
# des: from design
# df: table of experiments
# DEFINE_ME: needs user input


#########################
# CREATE OPTIMAL DESIGN #
#########################

terms = c('A','B','A:B','I(A^2)') # DEFINE_ME, define terms to be used in MLR model

# reformat model into equation
formula = paste('~',terms[1])
for (t in terms[-1]){
  formula = paste(formula,'+',t)
}
formula = as.formula(formula)

extra_exp <- 1
des <- NULL

while (is.null(des)) {
  no_experiments <- ncol(model.matrix(formula, df_candidates)) + extra_exp
  
  # Attempt to generate the design and catch any errors
  des <- tryCatch({
    optFederov(formula,
               df_candidates,
               nTrials = no_experiments,
               criterion = criterion
    )
  }, error = function(e) {
    # Print an error message with extra_exp value
    cat("Error encountered with extra_exp =", extra_exp, ":", e$message, "\n")
    # Increment extra_exp
    extra_exp <<- extra_exp + 1  # Use <<- to update extra_exp globally
    # Return NULL to indicate failure
    NULL
  })
}

# if getting the error "nTrials must be greater than or equal to the number of columns in expanded X"
# run model.matrix(formula,df_candidates) and check how many columns are in the matrix

# plot(des$design) # optional, show distribution of points
df_optim_des = des$design # df of experiments

# export data
write.csv(df_optim_des,"OptimalDesign.csv")

