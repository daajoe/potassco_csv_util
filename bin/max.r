#!/usr/bin/Rscript 
zz <- file("r.log", open="wt")
sink(zz, type="message")
data<-read.csv(file("stdin"), header = TRUE, sep = ",", dec=".", stringsAsFactors=FALSE)
#bd<-data["bd"]
#data["bd"]<-NULL
#print(apply(data[2:7],2,mean))
min_<-round(as.numeric(apply(data, 2 , min)),4)
min_[1]<-"min"
max_<-round(as.numeric(apply(data, 2 , max)),4)
max_[1]<-"max"
mean_<-round(as.numeric(sapply(data, mean)),4)
mean_[1]<-"mean"
sd_ <-round(as.numeric(apply(data, 2, sd)), 4)
sd_[1] <-"sddev"
num<-ncol(data)
cmin<-which.min(as.numeric(mean_[3:(num-1)]))+2
x<-vector(mode="character", length=num)
x[cmin]<-'**'
#names(data)[cmin]<-paste(names(data)[cmin],"-")
x[1]<-"MIN"
res<-rbind(data,min_,max_,mean_,sd_)
res2<-data.frame(cbind(res[1],res[2],res[3],res[cmin],res[num]))
res2[,'bd'] = round(as.numeric(res2[,'bd']),2)
#head(res2,-1)
a <- data.frame(sapply(res2, as.numeric))
a[,'speedup']<-round(a[,3]/a[,4],2)
res2[,3]<-round(as.numeric(res2[,3]),4)
res2[,4]<-round(as.numeric(res2[,4]),4)
#a[nrow(a)+1,] <- ""
names(res2)[4]<-paste(names(res2)[4],"-")
names(res2)[5]<-paste(names(res2)[5],"in %")
res3<-cbind(res2,a[6])

#write.table(res,stdout(),row.names = F, quote = F, sep=",")
#write.table(res2,stdout(),row.names = F, quote = F, sep=",")
write.table(res3,stdout(),row.names = F, quote = F, sep=",")

