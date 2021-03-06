# make sure R is in the proper working directory
# note that this will be a different path for every machine
setwd("C:/Users/Rachel/Desktop/Data Mining/")
# first include the relevant libraries
# note that a loading error might mean that you have to
# install the package into your R distribution.  From the
# command line, type install.packages("pixmap")
library(pixmap)

######################################################################(a)
#Load the views P00A+000E+00, P00A+005E+10, P00A+005E-10, and P00A+010E+00 for all subjects. 
#Convert each photo to a vector; store the collection as a matrix where each row is a photo.
# the list of pictures (note the absence of 14 means that 31 corresponds to yaleB32)
pic_list = c(1:38)
view_list = c( 'P00A+000E+00', 'P00A+005E+10', 'P00A+005E-10', 'P00A+010E+00')
dir_list_1 = dir(path="CroppedYale/",all.files=FALSE)

pic_data = vector("list",length(pic_list)*length(view_list)) # preallocate an empty list
pic_data_pgm = vector("list",length(pic_list)*length(view_list)) # preallocate an empty list to store the pgm for debugging

# Preallocate matrix to store picture vectors, store sizes for computations
this_face = read.pnm(file = "CroppedYale/yaleB01/yaleB01_P00A+010E+00.pgm")
this_face_matrix = getChannels(this_face)
original_size = dim(this_face_matrix)
pic_vector_length = prod(original_size)
pic_mat = mat.or.vec(length(pic_list)*length(view_list),pic_vector_length)


for ( i in 1:length(pic_list) ){
	for ( j in 1:length(view_list) ){
		# compile the correct file name
		this_filename = sprintf("CroppedYale/%s/%s_%s.pgm", dir_list_1[pic_list[i]] , dir_list_1[pic_list[i]] , view_list[j])
		this_face = read.pnm(file = this_filename)
		this_face_matrix = getChannels(this_face)

		# store pgm as element of the list
		pic_data_pgm[[(i-1)*length(view_list)+j]] = this_face
		# store matrix as element of the list
		pic_data[[(i-1)*length(view_list)+j]] = this_face_matrix
		# make the face into a vector and include in the data matrix
		pic_mat[(i-1)*length(view_list)+j,] =  as.vector(this_face_matrix)
	}	
}

pic_mat_size = dim(pic_mat)
print(sprintf('The matrix of all faces has size %d by %d' , pic_mat_size[1] , pic_mat_size[2] ))

######################################################################a(b)
#Compute a "mean face," which is the average for each pixel across all of the faces.
#Subtract this off each of the faces. Display the mean face as a photo in the original size and save a copy as .png.

# Find the mean face vector
mean_face = colMeans(pic_mat)
# Now print it as a picture
mean_face_matrix = mean_face
dim(mean_face_matrix) = original_size
mean_face_pix = pixmapGrey(mean_face_matrix)
plot(mean_face_pix)

#Subtract off the mean face
pic_mat_centered = mat.or.vec(pic_mat_size[1],pic_mat_size[2])

for (i in 1:pic_mat_size[1]){
	pic_mat_centered[i,] = pic_mat[i,] - mean_face
}
 
#####################################################################(c)
#Use prcomp() to find the principal components of your image matrix. 
#Plot the number of components on the x-axis against the proportion of the variance explained on the y-axis.
pic_pca = prcomp(pic_mat_centered)

# make a vector to store the variances captured by the components
n_comp = length(pic_pca$x[,1])
pca_var = mat.or.vec(n_comp,1)
for (i in 1:n_comp){
	if (i==1){
		pca_var[i] = pic_pca$sdev[i]^2
	}else{
		pca_var[i] = pca_var[i-1] + pic_pca$sdev[i]^2
	}
}

pca_var = pca_var/pca_var[n_comp]*100
# now plot it against the number of components
plot(pca_var,ylim=c(-2,102),xlab="Number of Components",ylab="Percentage of Variance Captured")
# add a line at 100 to show max level
abline(h=100,col="red")

#######################################################################(d)
#Each principal component is a picture, which are called "eigenfaces". 
#Display the first 9 eigenfaces in a 3-by-3 grid.
eigenface_mat = vector()
ind = 9

# loop through first 9 eigenfaces
this_face_row = vector()

for (i in 1:ind){
	# Make the eigenface vector into a matrix
	this_eigenface = pic_pca$rotation[,i]
	dim(this_eigenface) = original_size
	this_face_row = cbind(this_face_row,this_eigenface)
	if ((i %% 3)==0){
		# make a new row
		eigenface_mat = rbind(eigenface_mat,this_face_row)
		# clear row vector
		this_face_row = vector()
	}
}
# Plot the eigenfaces
eigenface_pgm = pixmapGrey((eigenface_mat-min(eigenface_mat))/(max(eigenface_mat)-min(eigenface_mat)))
plot(eigenface_pgm)


#################
# # End of Script
#################