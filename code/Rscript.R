library(sna)
library(igraph)

ARN = read.csv("../data/1-ARN.tsv", sep = '\t')
net <- graph_from_data_frame(d=ARN, directed=T) 
mat = as.matrix(as_adjacency_matrix(net))
gplot(mat)

ABAN = read.csv("../data/2-ABAN.tsv", sep = '\t')
net <- graph_from_data_frame(d=ABAN, directed=T) 
mat = as.matrix(as_adjacency_matrix(net))
gplot(mat)

CBEN = read.csv("../data/3-CBEN.tsv", sep = '\t')
net <- graph_from_data_frame(d=CBEN, directed=T) 
mat = as.matrix(as_adjacency_matrix(net))
gplot(mat)

VBEN = read.csv("../data/4-VBEN.tsv", sep = '\t')
net <- graph_from_data_frame(d=VBEN, directed=T) 
mat = as.matrix(as_adjacency_matrix(net))
gplot(mat)

VBEN2 = read.csv("../data/5-VBEN2.tsv", sep = '\t')
net <- graph_from_data_frame(d=VBEN2, directed=T) 
mat = as.matrix(as_adjacency_matrix(net))
gplot(mat)
