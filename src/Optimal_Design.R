library(AlgDesign) # generates Optimal Design DoE; chosen over skpr because this does not use repeats
library(rstudioapi)

# naming convention
# des: from design
# df: table of experiments
# DEFINE_ME: needs user input


#########################
# CREATE OPTIMAL DESIGN #
#########################

terms <- c('A','B','A:B','I(A^2)') # DEFINE_ME, define terms to be used in MLR model

# reformat model into equation
formula <- paste('~',terms[1])
for (t in terms[-1]){
  formula <- paste(formula,'+',t)
}
formula <- as.formula(formula)

# prepare df of candidates where optimal design will pick from
# can set manual levels (including categorical) by using A = c(0,1,2) or A = as.factor(c("High", "Med", "Low"))
# DEFINE_ME
df_candidates <- expand.grid(A = seq(40, 90, 5), # °C of elyte out of heater
                            B = seq(40, 160, 5) # °C of hotplate
                            )

extra_exp <- 1 # DEFINE_ME
criterion = 'I' # DEFINE_ME, I-optimal as default / recommended optimality
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
    cat("Error encountered with extra_exp =", extra_exp, ":", e$message, "\n")
    extra_exp <<- extra_exp + 1  # Use <<- to update extra_exp globally
    NULL
  })
}

# if getting the error "nTrials must be greater than or equal to the number of columns in expanded X"
# run model.matrix(formula,df_candidates) and check how many columns are in the matrix

# plot(des$design) # optional, show distribution of points
df_optim_des <- des$design # df of experiments

# export data
doc_context <- getActiveDocumentContext()
doc_path <- doc_context$path
doc_dir <- dirname(doc_path)

output_file <- file.path(doc_dir, "OptimalDesign.csv")
write.csv(df_optim_des, file = output_file)
