library(smpredict)

args <- commandArgs(trailingOnly = TRUE)

fileConn <- file("single.smi")
writeLines(c(args[1], "CC"), fileConn)
close(fileConn)

predictions <- PredictLogP(structures.file="single.smi", error.variance=FALSE, threads=1)
print(predictions$smLogP[1])